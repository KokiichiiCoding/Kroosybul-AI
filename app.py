"""
CodeForge AI - Main Flask Application
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

# Store active sessions
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
        del active_sessions[session_id]
    logger.info(f"Client disconnected: {session_id}")


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
    """Get available project templates"""
    templates = project_generator.get_available_templates()
    return jsonify({'templates': templates})


if __name__ == '__main__':
    # Ensure required directories exist
    os.makedirs('generated_projects', exist_ok=True)
    os.makedirs('logs', exist_ok=True)

    # Run the application
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))

    logger.info(f"Starting CodeForge AI on {host}:{port}")
    socketio.run(app, host=host, port=port, debug=os.getenv('FLASK_DEBUG', 'False') == 'True')
