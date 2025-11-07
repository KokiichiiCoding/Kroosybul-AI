"""
Project Templates - Enhanced template definitions for various project types
"""

from typing import Dict, List, Any


class ProjectTemplates:
    """Comprehensive project template definitions"""

    @staticmethod
    def get_all_templates() -> List[Dict[str, Any]]:
        """Get all available project templates"""
        return [
            # Original templates
            {
                'id': 'web_app',
                'name': 'Web Application',
                'description': 'Full-stack web application with frontend and backend',
                'languages': ['python', 'javascript', 'typescript'],
                'category': 'web',
                'difficulty': 'intermediate'
            },
            {
                'id': 'game',
                'name': 'Game Project',
                'description': '2D or 3D game with game loop and rendering',
                'languages': ['python', 'javascript', 'cpp', 'rust'],
                'category': 'game',
                'difficulty': 'advanced'
            },
            {
                'id': 'api',
                'name': 'REST API',
                'description': 'RESTful API service with endpoints and database',
                'languages': ['python', 'javascript', 'typescript', 'go', 'rust'],
                'category': 'backend',
                'difficulty': 'intermediate'
            },
            {
                'id': 'cli_tool',
                'name': 'CLI Tool',
                'description': 'Command-line application',
                'languages': ['python', 'rust', 'go'],
                'category': 'utility',
                'difficulty': 'beginner'
            },
            {
                'id': 'ml_project',
                'name': 'Machine Learning',
                'description': 'ML/AI project with data processing and model training',
                'languages': ['python'],
                'category': 'ai',
                'difficulty': 'advanced'
            },
            {
                'id': 'desktop_app',
                'name': 'Desktop Application',
                'description': 'GUI desktop application',
                'languages': ['python', 'javascript', 'cpp'],
                'category': 'desktop',
                'difficulty': 'intermediate'
            },

            # NEW TEMPLATES
            {
                'id': 'discord_bot',
                'name': 'Discord Bot',
                'description': 'Feature-rich Discord bot with commands, events, and integrations',
                'languages': ['python', 'javascript', 'typescript'],
                'category': 'bot',
                'difficulty': 'intermediate',
                'frameworks': {
                    'python': ['discord.py', 'discord.py-interactions'],
                    'javascript': ['discord.js'],
                    'typescript': ['discord.js', '@discordjs/rest']
                },
                'features': [
                    'Command handling',
                    'Event listeners',
                    'Slash commands',
                    'Database integration',
                    'Error handling',
                    'Logging system'
                ]
            },
            {
                'id': 'flask_dashboard',
                'name': 'Flask Dashboard',
                'description': 'Interactive web dashboard with Flask backend and modern frontend',
                'languages': ['python'],
                'category': 'web',
                'difficulty': 'intermediate',
                'frameworks': {
                    'python': ['flask', 'flask-socketio', 'flask-sqlalchemy', 'flask-login']
                },
                'features': [
                    'User authentication',
                    'Real-time data updates',
                    'RESTful API endpoints',
                    'Database models',
                    'Admin panel',
                    'Responsive UI',
                    'Charts and visualizations'
                ]
            },
            {
                'id': 'nextjs_dashboard',
                'name': 'Next.js Dashboard',
                'description': 'Modern dashboard with Next.js, TypeScript, and server-side rendering',
                'languages': ['typescript', 'javascript'],
                'category': 'web',
                'difficulty': 'advanced',
                'frameworks': {
                    'typescript': ['next', 'react', 'tailwindcss', 'swr'],
                    'javascript': ['next', 'react', 'tailwindcss']
                },
                'features': [
                    'Server-side rendering',
                    'API routes',
                    'Authentication',
                    'Database integration',
                    'Responsive design',
                    'Dark mode',
                    'Data visualization'
                ]
            },
            {
                'id': 'ai_agent_langchain',
                'name': 'AI Agent (LangChain)',
                'description': 'Intelligent AI agent using LangChain framework',
                'languages': ['python'],
                'category': 'ai',
                'difficulty': 'advanced',
                'frameworks': {
                    'python': ['langchain', 'openai', 'chromadb', 'tiktoken']
                },
                'features': [
                    'LLM integration',
                    'Vector store for memory',
                    'Tool/function calling',
                    'Conversation management',
                    'Document processing',
                    'Chain of thought reasoning'
                ]
            },
            {
                'id': 'ai_agent_crewai',
                'name': 'AI Agent (CrewAI)',
                'description': 'Multi-agent system using CrewAI framework',
                'languages': ['python'],
                'category': 'ai',
                'difficulty': 'advanced',
                'frameworks': {
                    'python': ['crewai', 'langchain', 'openai']
                },
                'features': [
                    'Multiple AI agents',
                    'Agent collaboration',
                    'Task delegation',
                    'Role-based agents',
                    'Sequential workflows',
                    'Memory and context'
                ]
            },
            {
                'id': 'webgl_game',
                'name': 'WebGL Mini-Game',
                'description': '3D browser game using WebGL and Three.js',
                'languages': ['javascript', 'typescript'],
                'category': 'game',
                'difficulty': 'advanced',
                'frameworks': {
                    'javascript': ['three', 'cannon-es', 'gsap'],
                    'typescript': ['three', '@types/three', 'cannon-es']
                },
                'features': [
                    '3D rendering',
                    'Physics simulation',
                    'User input handling',
                    'Animation system',
                    'Asset loading',
                    'Score tracking',
                    'Game states'
                ]
            },
            {
                'id': 'telegram_bot',
                'name': 'Telegram Bot',
                'description': 'Interactive Telegram bot with commands and inline features',
                'languages': ['python', 'javascript', 'typescript'],
                'category': 'bot',
                'difficulty': 'intermediate',
                'frameworks': {
                    'python': ['python-telegram-bot'],
                    'javascript': ['node-telegram-bot-api'],
                    'typescript': ['node-telegram-bot-api', 'telegraf']
                },
                'features': [
                    'Command handlers',
                    'Inline keyboards',
                    'Media handling',
                    'Webhook support',
                    'Database integration',
                    'User session management'
                ]
            },
            {
                'id': 'fastapi_microservice',
                'name': 'FastAPI Microservice',
                'description': 'High-performance microservice with FastAPI',
                'languages': ['python'],
                'category': 'backend',
                'difficulty': 'intermediate',
                'frameworks': {
                    'python': ['fastapi', 'uvicorn', 'sqlalchemy', 'pydantic', 'redis']
                },
                'features': [
                    'Async API endpoints',
                    'Auto-generated OpenAPI docs',
                    'Database ORM',
                    'Caching layer',
                    'Authentication/JWT',
                    'Request validation',
                    'CORS middleware'
                ]
            },
            {
                'id': 'chrome_extension',
                'name': 'Chrome Extension',
                'description': 'Browser extension with popup, content scripts, and background workers',
                'languages': ['javascript', 'typescript'],
                'category': 'utility',
                'difficulty': 'intermediate',
                'frameworks': {
                    'javascript': [],
                    'typescript': ['@types/chrome']
                },
                'features': [
                    'Popup interface',
                    'Content scripts',
                    'Background service worker',
                    'Storage API',
                    'Message passing',
                    'Context menus',
                    'Permissions handling'
                ]
            },
            {
                'id': 'electron_app',
                'name': 'Electron Desktop App',
                'description': 'Cross-platform desktop application with Electron',
                'languages': ['javascript', 'typescript'],
                'category': 'desktop',
                'difficulty': 'advanced',
                'frameworks': {
                    'javascript': ['electron'],
                    'typescript': ['electron', '@types/node']
                },
                'features': [
                    'Main process',
                    'Renderer process',
                    'IPC communication',
                    'Native menus',
                    'File system access',
                    'Auto-updates',
                    'Tray icon'
                ]
            },

            # GAME DEVELOPMENT TEMPLATES
            {
                'id': '2d_platformer',
                'name': '2D Platformer Game',
                'description': 'Classic side-scrolling platformer with physics and collisions',
                'languages': ['python', 'javascript'],
                'category': 'game',
                'difficulty': 'intermediate',
                'frameworks': {
                    'python': ['pygame', 'pymunk'],
                    'javascript': ['phaser3', 'matter-js']
                },
                'features': [
                    'Player movement and jumping',
                    'Physics simulation',
                    'Collision detection',
                    'Enemy AI',
                    'Level system',
                    'Score tracking',
                    'Sound effects'
                ]
            },
            {
                'id': '2d_rpg',
                'name': 'Top-Down RPG',
                'description': 'Classic RPG with exploration, combat, and dialogue',
                'languages': ['python', 'javascript'],
                'category': 'game',
                'difficulty': 'advanced',
                'frameworks': {
                    'python': ['pygame', 'pytmx'],
                    'javascript': ['phaser3', 'tiled']
                },
                'features': [
                    'Top-down movement',
                    'Tile-based maps',
                    'NPC dialogue system',
                    'Turn-based combat',
                    'Inventory system',
                    'Quest tracking',
                    'Save/Load system'
                ]
            },
            {
                'id': 'visual_novel',
                'name': 'Visual Novel',
                'description': 'Interactive story game with branching dialogue',
                'languages': ['python'],
                'category': 'game',
                'difficulty': 'beginner',
                'frameworks': {
                    'python': ['renpy', 'pygame']
                },
                'features': [
                    'Dialogue system',
                    'Character sprites',
                    'Background scenes',
                    'Choice system',
                    'Save/Load',
                    'Skip and auto-play',
                    'Music and sound effects'
                ]
            },
            {
                'id': '3d_sandbox',
                'name': '3D Sandbox Game',
                'description': 'First-person 3D world exploration and building',
                'languages': ['python', 'javascript'],
                'category': 'game',
                'difficulty': 'advanced',
                'frameworks': {
                    'python': ['panda3d', 'ursina'],
                    'javascript': ['threejs', 'cannon-es']
                },
                'features': [
                    'First-person camera',
                    '3D voxel terrain',
                    'Block placement/destruction',
                    'Physics simulation',
                    'Procedural generation',
                    'Day/night cycle',
                    'Inventory system'
                ]
            },
            {
                'id': 'puzzle_game',
                'name': 'Puzzle Game',
                'description': 'Brain-teasing puzzle mechanics with levels',
                'languages': ['python', 'javascript'],
                'category': 'game',
                'difficulty': 'intermediate',
                'frameworks': {
                    'python': ['pygame'],
                    'javascript': ['pixijs', 'phaser3']
                },
                'features': [
                    'Grid-based gameplay',
                    'Level progression',
                    'Undo/Redo system',
                    'Move counter',
                    'Time challenge',
                    'Level editor',
                    'Achievement system'
                ]
            },
            {
                'id': 'arcade_shooter',
                'name': 'Arcade Shooter',
                'description': 'Fast-paced shooting game with waves of enemies',
                'languages': ['python', 'javascript'],
                'category': 'game',
                'difficulty': 'intermediate',
                'frameworks': {
                    'python': ['pygame'],
                    'javascript': ['phaser3', 'pixijs']
                },
                'features': [
                    'Player spaceship/character',
                    'Projectile system',
                    'Enemy waves',
                    'Power-ups',
                    'Particle effects',
                    'High score system',
                    'Progressive difficulty'
                ]
            },
            {
                'id': 'endless_runner',
                'name': 'Endless Runner',
                'description': 'Procedurally generated endless running game',
                'languages': ['python', 'javascript'],
                'category': 'game',
                'difficulty': 'intermediate',
                'frameworks': {
                    'python': ['pygame'],
                    'javascript': ['phaser3']
                },
                'features': [
                    'Auto-scrolling',
                    'Procedural generation',
                    'Obstacle avoidance',
                    'Power-ups',
                    'Distance tracking',
                    'Speed progression',
                    'Leaderboard'
                ]
            },
            {
                'id': 'card_game',
                'name': 'Card Game',
                'description': 'Turn-based card battle game',
                'languages': ['python', 'javascript'],
                'category': 'game',
                'difficulty': 'intermediate',
                'frameworks': {
                    'python': ['pygame'],
                    'javascript': ['phaser3', 'pixijs']
                },
                'features': [
                    'Deck building',
                    'Card drawing system',
                    'Turn-based combat',
                    'Mana/Resource system',
                    'AI opponent',
                    'Card effects',
                    'Collection system'
                ]
            },
            {
                'id': 'tower_defense',
                'name': 'Tower Defense',
                'description': 'Strategic tower placement defense game',
                'languages': ['python', 'javascript'],
                'category': 'game',
                'difficulty': 'advanced',
                'frameworks': {
                    'python': ['pygame'],
                    'javascript': ['phaser3']
                },
                'features': [
                    'Tower placement',
                    'Enemy pathfinding',
                    'Wave system',
                    'Upgrade system',
                    'Multiple tower types',
                    'Resource management',
                    'Map editor'
                ]
            },
            {
                'id': 'racing_game',
                'name': 'Racing Game',
                'description': '2D or 3D racing with multiple tracks',
                'languages': ['python', 'javascript'],
                'category': 'game',
                'difficulty': 'advanced',
                'frameworks': {
                    'python': ['pygame', 'pymunk'],
                    'javascript': ['threejs', 'phaser3']
                },
                'features': [
                    'Vehicle physics',
                    'Track system',
                    'Lap timing',
                    'Opponent AI',
                    'Boost/power-ups',
                    'Multiple vehicles',
                    'Time trial mode'
                ]
            }
        ]

    @staticmethod
    def get_template_by_id(template_id: str) -> Dict[str, Any]:
        """Get a specific template by ID"""
        templates = ProjectTemplates.get_all_templates()
        for template in templates:
            if template['id'] == template_id:
                return template
        return None

    @staticmethod
    def get_templates_by_category(category: str) -> List[Dict[str, Any]]:
        """Get templates filtered by category"""
        templates = ProjectTemplates.get_all_templates()
        return [t for t in templates if t.get('category') == category]

    @staticmethod
    def get_templates_by_language(language: str) -> List[Dict[str, Any]]:
        """Get templates that support a specific language"""
        templates = ProjectTemplates.get_all_templates()
        return [t for t in templates if language.lower() in [l.lower() for l in t.get('languages', [])]]
