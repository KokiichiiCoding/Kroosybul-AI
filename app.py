"""
Kroosybul AI - Main Flask Application
An intelligent code generation studio for creating complete projects
"""

import os
import json
from flask import Flask, render_template, request, jsonify, send_file
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from dotenv import load_dotenv
import logging
from datetime import datetime

from core.ai_engine import AIEngine
from core.project_generator import ProjectGenerator
from core.code_executor import CodeExecutor
from core.session_manager import SessionManager
from core.venv_manager import VenvManager
from core.git_manager import GitManager
from core.multi_model_engine import MultiModelEngine
from core.template_library import TemplateLibrary

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-me')
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize core components
ai_engine = AIEngine()
project_generator = ProjectGenerator()
code_executor = CodeExecutor()
session_manager = SessionManager()
venv_manager = VenvManager()
git_manager = GitManager()
multi_model_engine = MultiModelEngine()
template_library = TemplateLibrary()

# Store active sessions (in-memory cache)
active_sessions = {}


@app.route('/')
def index():
    """Render the main chat interface"""
    return render_template('index.html')


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    })


@app.route('/api/languages', methods=['GET'])
def get_supported_languages():
    """Get list of supported programming languages"""
    languages = os.getenv('SUPPORTED_LANGUAGES', 'python,javascript').split(',')
    return jsonify({
        'languages': languages,
        'templates': project_generator.get_available_templates()
    })


@socketio.on('connect')
def handle_connect():
    """Handle new WebSocket connection"""
    session_id = request.sid
    active_sessions[session_id] = {
        'created_at': datetime.utcnow(),
        'messages': [],
        'current_project': None
    }
    logger.info(f"New client connected: {session_id}")
    emit('connected', {'session_id': session_id})


@socketio.on('disconnect')
def handle_disconnect():
    """Handle WebSocket disconnection"""
    session_id = request.sid
    if session_id in active_sessions:
        # Save session before disconnect
        session_manager.save_session(session_id, active_sessions[session_id])
        del active_sessions[session_id]
    logger.info(f"Client disconnected: {session_id}")


@socketio.on('load_session')
def handle_load_session(data):
    """Load a previous session"""
    current_session_id = request.sid
    load_session_id = data.get('session_id')

    if not load_session_id:
        emit('error', {'message': 'Session ID required'})
        return

    # Load session from database
    session_data = session_manager.load_session(load_session_id)

    if not session_data:
        emit('error', {'message': 'Session not found'})
        return

    # Restore session to active sessions
    active_sessions[current_session_id] = session_data

    # Send session data to client
    emit('session_loaded', {
        'session_id': load_session_id,
        'messages': session_data.get('messages', []),
        'project': session_data.get('current_project'),
        'created_at': session_data.get('created_at'),
        'updated_at': session_data.get('updated_at')
    })

    logger.info(f"Session {load_session_id} loaded for client {current_session_id}")


@socketio.on('message')
def handle_message(data):
    """Handle incoming chat messages and generate code"""
    session_id = request.sid
    user_message = data.get('message', '')

    logger.info(f"Received message from {session_id}: {user_message}")

    # Store user message
    if session_id in active_sessions:
        active_sessions[session_id]['messages'].append({
            'role': 'user',
            'content': user_message,
            'timestamp': datetime.utcnow().isoformat()
        })

    # Emit acknowledgment
    emit('message_received', {'status': 'processing'})

    try:
        # Start project generation process
        emit('status', {'message': 'Analyzing your request...', 'stage': 'analysis'})

        # Use AI to understand the project requirements
        project_plan = ai_engine.analyze_project_request(
            user_message,
            active_sessions[session_id]['messages']
        )

        emit('status', {'message': 'Creating project structure...', 'stage': 'planning'})
        emit('ai_response', {'message': project_plan['description'], 'type': 'plan'})

        # Generate the project
        emit('status', {'message': 'Generating code...', 'stage': 'generation'})

        project_result = project_generator.generate_project(
            project_plan,
            progress_callback=lambda msg: emit('progress', {'message': msg})
        )

        # Store project info
        active_sessions[session_id]['current_project'] = project_result

        # Initialize Git repository
        emit('status', {'message': 'Initializing Git repository...', 'stage': 'git_init'})
        git_success, git_msg = git_manager.init_repository(
            project_result['path'],
            project_result['language']
        )
        if git_success:
            logger.info(f"Git initialized for {project_result['name']}: {git_msg}")
        else:
            logger.warning(f"Git initialization failed: {git_msg}")

        # Create virtual environment
        emit('status', {'message': 'Setting up virtual environment...', 'stage': 'venv_setup'})
        venv_success, venv_msg = venv_manager.create_venv(
            project_result['path'],
            project_result['language']
        )
        if venv_success:
            logger.info(f"Virtual environment created: {venv_msg}")
        else:
            logger.warning(f"Virtual environment setup: {venv_msg}")

        # Test the generated code
        emit('status', {'message': 'Testing generated code...', 'stage': 'testing'})

        test_results = code_executor.test_project(project_result['path'])

        # Iterative refinement if needed
        iteration = 0
        max_iterations = int(os.getenv('MAX_ITERATIONS', 10))

        while not test_results['success'] and iteration < max_iterations:
            iteration += 1
            emit('status', {
                'message': f'Refining code (iteration {iteration}/{max_iterations})...',
                'stage': 'refinement',
                'iteration': iteration
            })

            # Ask AI to fix the issues
            fixes = ai_engine.fix_code_issues(
                project_result,
                test_results['errors'],
                active_sessions[session_id]['messages']
            )

            # Apply fixes
            project_generator.apply_fixes(project_result['path'], fixes)

            # Commit iteration to Git
            if git_success:
                description = f"Fix issues found in testing: {', '.join(test_results['errors'][:3])}"
                git_manager.commit_iteration(
                    project_result['path'],
                    iteration,
                    description
                )

                # Save iteration to session
                session_manager.save_iteration(
                    session_id,
                    iteration,
                    description,
                    fixes
                )

            # Re-test
            test_results = code_executor.test_project(project_result['path'])

        # Send final results
        if test_results['success']:
            emit('status', {'message': 'Project completed successfully!', 'stage': 'complete'})
            emit('project_complete', {
                'project_path': project_result['path'],
                'project_name': project_result['name'],
                'files': project_result['files'],
                'download_url': f"/api/download/{session_id}",
                'test_results': test_results
            })

            response_message = f"""
✅ **Project Generated Successfully!**

**Project Name:** {project_result['name']}
**Language:** {project_result['language']}
**Files Created:** {len(project_result['files'])}

**Generated Files:**
{chr(10).join(f"- {f}" for f in project_result['files'][:10])}
{f"... and {len(project_result['files']) - 10} more files" if len(project_result['files']) > 10 else ""}

**Next Steps:**
1. Download your project using the button above
2. Follow the README.md for setup instructions
3. Run the project and start building!

The project has been tested and is ready to run. Enjoy coding! 🚀
            """
        else:
            emit('status', {'message': 'Project generated with warnings', 'stage': 'complete'})
            emit('project_complete', {
                'project_path': project_result['path'],
                'project_name': project_result['name'],
                'files': project_result['files'],
                'download_url': f"/api/download/{session_id}",
                'test_results': test_results,
                'warnings': True
            })

            response_message = f"""
⚠️ **Project Generated with Warnings**

**Project Name:** {project_result['name']}
**Language:** {project_result['language']}
**Files Created:** {len(project_result['files'])}

Some tests didn't pass, but the project structure is complete. You may need to:
- Review the error messages
- Install additional dependencies
- Adjust configurations for your environment

The project is still usable and can be manually refined. Download it and check the README.md for details.
            """

        emit('ai_response', {'message': response_message, 'type': 'result'})

        # Store AI response
        active_sessions[session_id]['messages'].append({
            'role': 'assistant',
            'content': response_message,
            'timestamp': datetime.utcnow().isoformat()
        })

        # Save session to database
        session_manager.save_session(session_id, active_sessions[session_id])
        logger.info(f"Session {session_id} saved to database")

    except Exception as e:
        logger.error(f"Error processing message: {str(e)}", exc_info=True)
        emit('error', {'message': f'An error occurred: {str(e)}'})
        emit('ai_response', {
            'message': f'Sorry, I encountered an error: {str(e)}. Please try again or rephrase your request.',
            'type': 'error'
        })


@app.route('/api/download/<session_id>', methods=['GET'])
def download_project(session_id):
    """Download generated project as ZIP file"""
    if session_id not in active_sessions or not active_sessions[session_id].get('current_project'):
        return jsonify({'error': 'Project not found'}), 404

    project = active_sessions[session_id]['current_project']
    zip_path = project_generator.create_zip(project['path'])

    return send_file(
        zip_path,
        mimetype='application/zip',
        as_attachment=True,
        download_name=f"{project['name']}.zip"
    )


@app.route('/api/templates', methods=['GET'])
def get_templates():
    """Get available project templates (legacy endpoint)"""
    templates = project_generator.get_available_templates()
    return jsonify({'templates': templates})


# ========== Session Management Endpoints ==========

@app.route('/api/sessions', methods=['GET'])
def list_sessions():
    """List all saved sessions"""
    limit = request.args.get('limit', 50, type=int)
    status = request.args.get('status', 'active')
    sessions = session_manager.list_sessions(limit=limit, status=status)
    return jsonify({'sessions': sessions})


@app.route('/api/sessions/<session_id>', methods=['GET'])
def get_session(session_id):
    """Load a specific session"""
    session_data = session_manager.load_session(session_id)
    if session_data:
        return jsonify({'session': session_data})
    else:
        return jsonify({'error': 'Session not found'}), 404


@app.route('/api/sessions/<session_id>', methods=['DELETE'])
def delete_session(session_id):
    """Delete a session"""
    success = session_manager.delete_session(session_id)
    if success:
        return jsonify({'message': 'Session deleted successfully'})
    else:
        return jsonify({'error': 'Failed to delete session'}), 500


@app.route('/api/sessions/<session_id>/status', methods=['PUT'])
def update_session_status(session_id):
    """Update session status"""
    data = request.get_json()
    status = data.get('status', 'active')
    success = session_manager.update_session_status(session_id, status)
    if success:
        return jsonify({'message': 'Session status updated'})
    else:
        return jsonify({'error': 'Failed to update session'}), 500


# ========== Model Management Endpoints ==========

@app.route('/api/models', methods=['GET'])
def get_models():
    """Get available AI models"""
    providers = multi_model_engine.get_available_providers()
    stats = multi_model_engine.get_usage_stats()
    return jsonify({
        'providers': providers,
        'current_provider': multi_model_engine.current_provider,
        'usage_stats': stats
    })


@app.route('/api/models/switch', methods=['POST'])
def switch_model():
    """Switch to a different AI model provider"""
    data = request.get_json()
    provider = data.get('provider')

    if not provider:
        return jsonify({'error': 'Provider name required'}), 400

    success = multi_model_engine.set_provider(provider)
    if success:
        return jsonify({
            'message': f'Switched to {provider}',
            'current_provider': multi_model_engine.current_provider
        })
    else:
        return jsonify({'error': f'Provider {provider} not available'}), 400


@app.route('/api/models/usage', methods=['GET'])
def get_usage_stats():
    """Get AI usage statistics and costs"""
    stats = multi_model_engine.get_usage_stats()
    return jsonify(stats)


# ========== Template Library Endpoints ==========

@app.route('/api/library/templates', methods=['GET'])
def get_library_templates():
    """Get templates from the library"""
    category = request.args.get('category')
    language = request.args.get('language')
    battle_tested = request.args.get('battle_tested', 'false').lower() == 'true'

    templates = template_library.list_templates(
        category=category,
        language=language,
        battle_tested=battle_tested
    )

    return jsonify({
        'templates': templates,
        'categories': template_library.get_categories()
    })


@app.route('/api/library/templates/<template_id>', methods=['GET'])
def get_template_detail(template_id):
    """Get detailed information about a template"""
    template = template_library.get_template(template_id)
    if template:
        return jsonify({'template': template})
    else:
        return jsonify({'error': 'Template not found'}), 404


@app.route('/api/library/templates', methods=['POST'])
def create_template():
    """Create a new custom template"""
    data = request.get_json()
    source = data.get('source', 'custom')

    success, message = template_library.create_template(data, source)
    if success:
        return jsonify({'message': message})
    else:
        return jsonify({'error': message}), 400


@app.route('/api/library/templates/<template_id>', methods=['DELETE'])
def delete_template(template_id):
    """Delete a custom template"""
    success, message = template_library.delete_template(template_id)
    if success:
        return jsonify({'message': message})
    else:
        return jsonify({'error': message}), 400


@app.route('/api/library/templates/<template_id>/export', methods=['GET'])
def export_template(template_id):
    """Export a template as a zip file"""
    import tempfile

    temp_path = tempfile.mktemp(suffix='.zip')
    success, message = template_library.export_template(template_id, temp_path)

    if success:
        return send_file(
            temp_path,
            mimetype='application/zip',
            as_attachment=True,
            download_name=f"{template_id}.zip"
        )
    else:
        return jsonify({'error': message}), 400


@app.route('/api/library/templates/import', methods=['POST'])
def import_template():
    """Import a template from a file"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    source = request.form.get('source', 'custom')

    import tempfile
    temp_path = tempfile.mktemp(suffix='.zip')
    file.save(temp_path)

    success, message = template_library.import_template(temp_path, source)

    os.remove(temp_path)

    if success:
        return jsonify({'message': message})
    else:
        return jsonify({'error': message}), 400


@app.route('/api/library/search', methods=['GET'])
def search_templates():
    """Search templates"""
    query = request.args.get('q', '')
    results = template_library.search_templates(query)
    return jsonify({'results': results})


# ========== Git Management Endpoints ==========

@app.route('/api/git/<session_id>/status', methods=['GET'])
def get_git_status(session_id):
    """Get Git repository status"""
    if session_id not in active_sessions or not active_sessions[session_id].get('current_project'):
        return jsonify({'error': 'Project not found'}), 404

    project_path = active_sessions[session_id]['current_project']['path']
    status = git_manager.get_status(project_path)
    return jsonify(status)


@app.route('/api/git/<session_id>/history', methods=['GET'])
def get_git_history(session_id):
    """Get Git commit history"""
    if session_id not in active_sessions or not active_sessions[session_id].get('current_project'):
        return jsonify({'error': 'Project not found'}), 404

    project_path = active_sessions[session_id]['current_project']['path']
    limit = request.args.get('limit', 10, type=int)
    history = git_manager.get_commit_history(project_path, limit)
    return jsonify({'commits': history})


@app.route('/api/git/<session_id>/rollback', methods=['POST'])
def rollback_git(session_id):
    """Rollback to a specific commit"""
    if session_id not in active_sessions or not active_sessions[session_id].get('current_project'):
        return jsonify({'error': 'Project not found'}), 404

    data = request.get_json()
    commit_hash = data.get('commit_hash')

    if not commit_hash:
        return jsonify({'error': 'Commit hash required'}), 400

    project_path = active_sessions[session_id]['current_project']['path']
    success, message = git_manager.rollback_to_commit(project_path, commit_hash)

    if success:
        return jsonify({'message': message})
    else:
        return jsonify({'error': message}), 400


if __name__ == '__main__':
    # Ensure required directories exist
    os.makedirs('generated_projects', exist_ok=True)
    os.makedirs('logs', exist_ok=True)

    # Run the application
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))

    logger.info(f"Starting Kroosybul AI on {host}:{port}")
    socketio.run(app, host=host, port=port, debug=os.getenv('FLASK_DEBUG', 'False') == 'True')
