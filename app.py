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
from core.enhanced_features import MultiModelSupport, ReusableComponentLibrary
from core.game_engine import GameEngine, EntityComponentSystem, AssetManager
from core.game_ai_features import AILevelDesigner, NPCBehaviorGenerator, DialogueSystem, GameDesignDocGenerator

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
multi_model_support = MultiModelSupport()
component_library = ReusableComponentLibrary()

# Initialize game development components
game_engine = GameEngine()
ai_level_designer = AILevelDesigner(ai_engine)
npc_behavior_gen = NPCBehaviorGenerator(ai_engine)
dialogue_system = DialogueSystem()
gdd_generator = GameDesignDocGenerator(ai_engine)

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

        # Generate architecture diagram
        emit('status', {'message': 'Generating architecture diagram...', 'stage': 'planning'})
        try:
            architecture_diagram = ai_engine.generate_architecture_diagram(project_plan)
            emit('architecture_diagram', {'diagram': architecture_diagram, 'format': 'mermaid'})
        except Exception as e:
            logger.warning(f"Failed to generate architecture diagram: {e}")

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

        # Generate AI-powered test summary
        try:
            test_summary = ai_engine.generate_test_summary(test_results)
            emit('test_summary', {'summary': test_summary})
        except Exception as e:
            logger.warning(f"Failed to generate test summary: {e}")

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

            # Provide natural language explanations for errors
            if test_results.get('errors'):
                try:
                    for error in test_results['errors'][:3]:  # Explain top 3 errors
                        explanation = ai_engine.explain_error_naturally(
                            error,
                            {'language': project_result['language'], 'project_type': project_plan['project_type']}
                        )
                        emit('error_explanation', {'error': error, 'explanation': explanation})
                except Exception as e:
                    logger.warning(f"Failed to generate error explanations: {e}")

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


@app.route('/api/templates/category/<category>', methods=['GET'])
def get_templates_by_category(category):
    """Get templates filtered by category"""
    templates = project_generator.get_templates_by_category(category)
    return jsonify({'templates': templates, 'category': category})


@app.route('/api/models', methods=['GET'])
def get_available_models():
    """Get list of available AI models"""
    models = multi_model_support.get_available_models()
    return jsonify({'models': models})


@app.route('/api/components/search', methods=['POST'])
def search_components():
    """Search for reusable components"""
    data = request.get_json()
    query = data.get('query')
    language = data.get('language')
    tags = data.get('tags')

    results = component_library.search_components(query, language, tags)
    return jsonify({'components': results})


@app.route('/api/components/save', methods=['POST'])
def save_component():
    """Save a reusable component"""
    data = request.get_json()

    try:
        component_library.save_component(
            name=data['name'],
            code=data['code'],
            language=data['language'],
            description=data['description'],
            tags=data.get('tags', [])
        )
        return jsonify({'success': True, 'message': 'Component saved successfully'})
    except Exception as e:
        logger.error(f"Error saving component: {e}")
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/analyze/complexity', methods=['POST'])
def analyze_complexity():
    """Analyze code complexity"""
    data = request.get_json()
    code = data.get('code', '')
    language = data.get('language', 'python')

    try:
        complexity = ai_engine.estimate_complexity(code, language)
        return jsonify({'success': True, 'complexity': complexity})
    except Exception as e:
        logger.error(f"Error analyzing complexity: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/document/generate', methods=['POST'])
def generate_documentation():
    """Generate documentation for code"""
    data = request.get_json()
    code = data.get('code', '')
    language = data.get('language', 'python')

    try:
        documented_code = ai_engine.generate_documentation(code, language)
        return jsonify({'success': True, 'documented_code': documented_code})
    except Exception as e:
        logger.error(f"Error generating documentation: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@socketio.on('upload_file')
def handle_file_upload(data):
    """Handle file upload for context-based generation"""
    session_id = request.sid
    filename = data.get('filename', 'unknown')
    content = data.get('content', '')

    logger.info(f"File uploaded: {filename} from {session_id}")

    # Store uploaded file in session
    if session_id in active_sessions:
        if 'uploaded_files' not in active_sessions[session_id]:
            active_sessions[session_id]['uploaded_files'] = []

        active_sessions[session_id]['uploaded_files'].append({
            'filename': filename,
            'content': content
        })

        emit('file_uploaded', {
            'filename': filename,
            'status': 'success',
            'message': f'File {filename} uploaded successfully'
        })


# ============================================================
# GAME DEVELOPMENT API ENDPOINTS
# ============================================================

@app.route('/api/game/engines', methods=['GET'])
def get_game_engines():
    """Get list of supported game engines"""
    return jsonify({'engines': game_engine.supported_engines})


@app.route('/api/game/level/generate', methods=['POST'])
def generate_level():
    """Generate a game level using AI"""
    data = request.get_json()

    try:
        level_data = ai_level_designer.generate_level(data)
        return jsonify({'success': True, 'level': level_data})
    except Exception as e:
        logger.error(f"Error generating level: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/game/level/tilemap', methods=['POST'])
def generate_tilemap_code():
    """Generate tilemap rendering code"""
    data = request.get_json()
    level_data = data.get('level_data', {})
    engine = data.get('engine', 'pygame')

    try:
        tilemap_code = ai_level_designer.generate_tilemap_code(level_data, engine)
        return jsonify({'success': True, 'code': tilemap_code})
    except Exception as e:
        logger.error(f"Error generating tilemap code: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/game/npc/behavior', methods=['POST'])
def generate_npc_behavior():
    """Generate NPC AI behavior"""
    data = request.get_json()

    try:
        behavior_data = npc_behavior_gen.generate_behavior(data)
        return jsonify({'success': True, 'behavior': behavior_data})
    except Exception as e:
        logger.error(f"Error generating NPC behavior: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/game/npc/behavior/code', methods=['POST'])
def generate_behavior_code():
    """Generate code implementation of NPC behavior"""
    data = request.get_json()
    behavior_data = data.get('behavior_data', {})
    language = data.get('language', 'python')

    try:
        code = npc_behavior_gen.generate_behavior_code(behavior_data, language)
        return jsonify({'success': True, 'code': code})
    except Exception as e:
        logger.error(f"Error generating behavior code: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/game/dialogue/generate', methods=['POST'])
def generate_dialogue():
    """Generate NPC dialogue using AI"""
    data = request.get_json()

    try:
        dialogue_data = DialogueSystem.generate_dialogue_with_ai(ai_engine, data)
        return jsonify({'success': True, 'dialogue': dialogue_data})
    except Exception as e:
        logger.error(f"Error generating dialogue: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/game/dialogue/code', methods=['POST'])
def generate_dialogue_code():
    """Generate dialogue system code"""
    data = request.get_json()
    dialogue_tree = data.get('dialogue_tree', {})
    language = data.get('language', 'python')

    try:
        code = DialogueSystem.generate_dialogue_code(dialogue_tree, language)
        return jsonify({'success': True, 'code': code})
    except Exception as e:
        logger.error(f"Error generating dialogue code: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/game/scene/create', methods=['POST'])
def create_game_scene():
    """Create an ECS scene definition"""
    data = request.get_json()
    scene_name = data.get('scene_name', 'GameScene')
    entities = data.get('entities', [])

    try:
        scene = EntityComponentSystem.create_scene_definition(scene_name, entities)
        return jsonify({'success': True, 'scene': scene})
    except Exception as e:
        logger.error(f"Error creating scene: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/game/scene/code', methods=['POST'])
def generate_scene_code():
    """Generate ECS code from scene definition"""
    data = request.get_json()
    scene_data = data.get('scene', {})
    language = data.get('language', 'python')

    try:
        code = EntityComponentSystem.generate_ecs_code(scene_data, language)
        return jsonify({'success': True, 'code': code})
    except Exception as e:
        logger.error(f"Error generating scene code: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/game/loop/template', methods=['POST'])
def get_game_loop_template():
    """Get a game loop template for specific engine"""
    data = request.get_json()
    engine = data.get('engine', 'pygame')
    game_type = data.get('game_type', 'platformer')

    try:
        template_code = game_engine.create_game_loop_template(engine, game_type)
        return jsonify({'success': True, 'code': template_code})
    except Exception as e:
        logger.error(f"Error getting game loop template: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/game/gdd/generate', methods=['POST'])
def generate_game_design_doc():
    """Generate Game Design Document"""
    data = request.get_json()

    try:
        gdd = gdd_generator.generate_gdd(data)
        return jsonify({'success': True, 'gdd': gdd})
    except Exception as e:
        logger.error(f"Error generating GDD: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/game/assets/scan', methods=['POST'])
def scan_game_assets():
    """Scan project for game assets"""
    data = request.get_json()
    project_path = data.get('project_path')

    if not project_path:
        return jsonify({'success': False, 'error': 'Project path required'}), 400

    try:
        asset_manager = AssetManager(project_path)
        manifest = asset_manager.scan_assets()
        return jsonify({'success': True, 'assets': manifest})
    except Exception as e:
        logger.error(f"Error scanning assets: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/game/assets/loader', methods=['POST'])
def generate_asset_loader():
    """Generate asset loading code"""
    data = request.get_json()
    project_path = data.get('project_path')
    engine = data.get('engine', 'pygame')

    if not project_path:
        return jsonify({'success': False, 'error': 'Project path required'}), 400

    try:
        asset_manager = AssetManager(project_path)
        asset_manager.scan_assets()
        loader_code = asset_manager.generate_asset_loader(engine)
        return jsonify({'success': True, 'code': loader_code})
    except Exception as e:
        logger.error(f"Error generating asset loader: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    # Ensure required directories exist
    os.makedirs('generated_projects', exist_ok=True)
    os.makedirs('logs', exist_ok=True)

    # Run the application
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))

    logger.info(f"Starting CodeForge AI on {host}:{port}")
    socketio.run(app, host=host, port=port, debug=os.getenv('FLASK_DEBUG', 'False') == 'True')
