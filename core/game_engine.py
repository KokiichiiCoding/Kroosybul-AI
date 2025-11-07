"""
Game Engine - Game development tools and templates for Kroosybul AI
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class GameEngine:
    """Core game development functionality"""

    def __init__(self):
        self.supported_engines = {
            'pygame': {
                'language': 'python',
                'description': '2D game development',
                'physics': ['pymunk'],
                'suitable_for': ['platformer', '2d_rpg', 'puzzle', 'arcade']
            },
            'phaser': {
                'language': 'javascript',
                'description': 'HTML5 game framework',
                'physics': ['arcade', 'matter'],
                'suitable_for': ['platformer', 'rpg', 'shooter', 'puzzle']
            },
            'threejs': {
                'language': 'javascript',
                'description': '3D graphics library',
                'physics': ['cannon', 'ammo'],
                'suitable_for': ['3d_game', 'webgl', 'sandbox']
            },
            'godot': {
                'language': 'python',  # GDScript or Python
                'description': 'Full game engine',
                'physics': ['built-in'],
                'suitable_for': ['2d_game', '3d_game', 'rpg']
            },
            'renpy': {
                'language': 'python',
                'description': 'Visual novel engine',
                'physics': [],
                'suitable_for': ['visual_novel', 'dating_sim']
            },
            'pixijs': {
                'language': 'javascript',
                'description': '2D WebGL renderer',
                'physics': ['matter'],
                'suitable_for': ['2d_game', 'mobile', 'casual']
            }
        }

    def get_recommended_engine(self, game_type: str, language: str = None) -> str:
        """Recommend best game engine for project type"""

        recommendations = {
            '2d_platformer': 'pygame' if language == 'python' else 'phaser',
            '2d_rpg': 'pygame' if language == 'python' else 'phaser',
            'visual_novel': 'renpy',
            '3d_game': 'threejs',
            'webgl_game': 'threejs',
            'puzzle': 'pygame' if language == 'python' else 'pixijs',
            'arcade': 'pygame' if language == 'python' else 'phaser',
            'shooter': 'phaser',
            'sandbox': 'threejs'
        }

        return recommendations.get(game_type, 'pygame')

    def create_game_loop_template(self, engine: str, game_type: str) -> str:
        """Generate game loop code template"""

        if engine == 'pygame':
            return self._pygame_game_loop(game_type)
        elif engine == 'phaser':
            return self._phaser_game_loop(game_type)
        elif engine == 'threejs':
            return self._threejs_game_loop(game_type)
        elif engine == 'renpy':
            return self._renpy_game_loop(game_type)
        else:
            return self._generic_game_loop()

    def _pygame_game_loop(self, game_type: str) -> str:
        """Pygame game loop template"""
        return '''"""
Game Loop - Main game logic and update cycle
"""
import pygame
import sys

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("My Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.fps = 60

        # Game state
        self.entities = []
        self.player = None

        # Initialize game
        self.init_game()

    def init_game(self):
        """Initialize game objects and resources"""
        # Load assets
        # Create entities
        # Setup physics
        pass

    def handle_events(self):
        """Handle input events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)
            elif event.type == pygame.KEYUP:
                self.handle_keyup(event.key)

    def handle_keydown(self, key):
        """Handle key press"""
        pass

    def handle_keyup(self, key):
        """Handle key release"""
        pass

    def update(self, dt):
        """Update game state"""
        # Update entities
        for entity in self.entities:
            if hasattr(entity, 'update'):
                entity.update(dt)

        # Check collisions
        self.check_collisions()

        # Update physics
        self.update_physics(dt)

    def check_collisions(self):
        """Detect and handle collisions"""
        pass

    def update_physics(self, dt):
        """Update physics simulation"""
        pass

    def render(self):
        """Render game objects"""
        self.screen.fill((0, 0, 0))  # Clear screen

        # Render entities
        for entity in self.entities:
            if hasattr(entity, 'render'):
                entity.render(self.screen)

        pygame.display.flip()

    def run(self):
        """Main game loop"""
        while self.running:
            dt = self.clock.tick(self.fps) / 1000.0  # Delta time in seconds

            self.handle_events()
            self.update(dt)
            self.render()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
'''

    def _phaser_game_loop(self, game_type: str) -> str:
        """Phaser.js game loop template"""
        return '''// Game Configuration
const config = {
    type: Phaser.AUTO,
    width: 800,
    height: 600,
    physics: {
        default: 'arcade',
        arcade: {
            gravity: { y: 300 },
            debug: false
        }
    },
    scene: {
        preload: preload,
        create: create,
        update: update
    }
};

const game = new Phaser.Game(config);

// Asset loading
function preload() {
    // Load sprites
    // this.load.image('player', 'assets/player.png');
    // this.load.spritesheet('enemy', 'assets/enemy.png', { frameWidth: 32, frameHeight: 48 });
}

// Game initialization
function create() {
    // Create game objects
    // this.player = this.physics.add.sprite(100, 450, 'player');

    // Setup physics
    // this.player.setBounce(0.2);
    // this.player.setCollideWorldBounds(true);

    // Input handling
    this.cursors = this.input.keyboard.createCursorKeys();
}

// Game update loop
function update() {
    // Handle input
    if (this.cursors.left.isDown) {
        // Move left
    }
    else if (this.cursors.right.isDown) {
        // Move right
    }
    else {
        // Idle
    }

    // Jump
    if (this.cursors.up.isDown) {
        // Jump logic
    }

    // Update game logic
    // Check collisions
    // Update entities
}
'''

    def _threejs_game_loop(self, game_type: str) -> str:
        """Three.js game loop template"""
        return '''// Three.js Game Loop
import * as THREE from 'three';

class Game {
    constructor() {
        // Scene setup
        this.scene = new THREE.Scene();
        this.camera = new THREE.PerspectiveCamera(
            75,
            window.innerWidth / window.innerHeight,
            0.1,
            1000
        );

        this.renderer = new THREE.WebGLRenderer({ antialias: true });
        this.renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(this.renderer.domElement);

        // Game objects
        this.entities = [];
        this.clock = new THREE.Clock();

        // Initialize
        this.init();

        // Start game loop
        this.animate();
    }

    init() {
        // Setup lighting
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
        this.scene.add(ambientLight);

        const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
        directionalLight.position.set(10, 10, 5);
        this.scene.add(directionalLight);

        // Camera position
        this.camera.position.z = 5;

        // Load assets and create objects
        this.loadAssets();
        this.createEntities();

        // Event listeners
        window.addEventListener('resize', () => this.onWindowResize());
        document.addEventListener('keydown', (e) => this.onKeyDown(e));
    }

    loadAssets() {
        // Load 3D models, textures, etc.
    }

    createEntities() {
        // Create game entities
    }

    onKeyDown(event) {
        // Handle keyboard input
        switch(event.key) {
            case 'w':
            case 'ArrowUp':
                // Move forward
                break;
            case 's':
            case 'ArrowDown':
                // Move backward
                break;
            case 'a':
            case 'ArrowLeft':
                // Move left
                break;
            case 'd':
            case 'ArrowRight':
                // Move right
                break;
        }
    }

    update(deltaTime) {
        // Update entities
        this.entities.forEach(entity => {
            if (entity.update) {
                entity.update(deltaTime);
            }
        });

        // Update physics
        this.updatePhysics(deltaTime);

        // Check collisions
        this.checkCollisions();
    }

    updatePhysics(deltaTime) {
        // Physics simulation
    }

    checkCollisions() {
        // Collision detection
    }

    onWindowResize() {
        this.camera.aspect = window.innerWidth / window.innerHeight;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(window.innerWidth, window.innerHeight);
    }

    animate() {
        requestAnimationFrame(() => this.animate());

        const deltaTime = this.clock.getDelta();

        this.update(deltaTime);
        this.renderer.render(this.scene, this.camera);
    }
}

// Start game
const game = new Game();
'''

    def _renpy_game_loop(self, game_type: str) -> str:
        """Ren'Py visual novel template"""
        return '''# The script of the game goes in this file.

# Declare characters used by this game
define narrator = Character(None, kind=nvl)
define p = Character("Player", color="#c8ffc8")
define e = Character("Eileen", color="#c8c8ff")

# The game starts here
label start:
    # Show a background
    scene bg room

    # Show a character
    show eileen happy

    # Dialogue
    e "Welcome to my visual novel!"
    e "This is a template for creating interactive stories."

    # Player choice
    menu:
        "What would you like to do?"

        "Talk to Eileen":
            jump talk_to_eileen

        "Explore the room":
            jump explore_room

label talk_to_eileen:
    e "I'm glad you want to talk!"
    e "What would you like to know?"

    menu:
        "About the world":
            e "This world is full of mysteries..."
            jump continue_story

        "About you":
            e "I'm just a character in this story."
            jump continue_story

label explore_room:
    "You look around the room carefully."
    "There's a desk, a bookshelf, and a window."

    menu:
        "Check the desk":
            "You find an old journal."
            jump continue_story

        "Look at bookshelf":
            "The books are mostly about magic."
            jump continue_story

label continue_story:
    # Continue the story
    return
'''

    def _generic_game_loop(self) -> str:
        """Generic game loop pseudocode"""
        return '''"""
Generic Game Loop Template
"""

class Game:
    def __init__(self):
        self.running = True
        self.entities = []
        self.init()

    def init(self):
        """Initialize game resources"""
        # Load assets
        # Create entities
        # Setup systems
        pass

    def handle_input(self):
        """Process user input"""
        pass

    def update(self, delta_time):
        """Update game state"""
        # Update entities
        # Update physics
        # Check collisions
        # Update AI
        pass

    def render(self):
        """Render the game"""
        # Clear screen
        # Draw entities
        # Draw UI
        pass

    def run(self):
        """Main game loop"""
        while self.running:
            delta_time = self.get_delta_time()

            self.handle_input()
            self.update(delta_time)
            self.render()

if __name__ == "__main__":
    game = Game()
    game.run()
'''


class EntityComponentSystem:
    """Entity Component System for game objects"""

    @staticmethod
    def create_scene_definition(scene_name: str, entities: List[Dict] = None) -> Dict:
        """Create a scene definition JSON"""

        if entities is None:
            entities = []

        return {
            "scene_name": scene_name,
            "version": "1.0",
            "entities": entities,
            "systems": [
                "movement",
                "collision",
                "rendering",
                "input"
            ],
            "resources": {
                "sprites": [],
                "sounds": [],
                "tilemaps": []
            }
        }

    @staticmethod
    def create_entity(name: str, entity_type: str, **kwargs) -> Dict:
        """Create an entity definition"""

        entity = {
            "name": name,
            "type": entity_type,
            "components": {},
            "tags": []
        }

        # Add transform component
        entity["components"]["transform"] = {
            "position": kwargs.get("position", [0, 0]),
            "rotation": kwargs.get("rotation", 0),
            "scale": kwargs.get("scale", [1, 1])
        }

        # Add sprite component if sprite provided
        if "sprite" in kwargs:
            entity["components"]["sprite"] = {
                "texture": kwargs["sprite"],
                "width": kwargs.get("width", 32),
                "height": kwargs.get("height", 32),
                "layer": kwargs.get("layer", 0)
            }

        # Add physics component if needed
        if kwargs.get("physics", False):
            entity["components"]["physics"] = {
                "velocity": [0, 0],
                "acceleration": [0, 0],
                "mass": kwargs.get("mass", 1.0),
                "friction": kwargs.get("friction", 0.1)
            }

        # Add collision component
        if kwargs.get("collision", False):
            entity["components"]["collision"] = {
                "shape": kwargs.get("collision_shape", "box"),
                "size": kwargs.get("collision_size", [32, 32]),
                "is_trigger": kwargs.get("is_trigger", False)
            }

        # Add behavior component
        if "behavior" in kwargs:
            entity["components"]["behavior"] = {
                "type": kwargs["behavior"],
                "parameters": kwargs.get("behavior_params", {})
            }

        # Add custom components
        for key, value in kwargs.items():
            if key.startswith("component_"):
                component_name = key.replace("component_", "")
                entity["components"][component_name] = value

        return entity

    @staticmethod
    def generate_ecs_code(scene: Dict, language: str = "python") -> str:
        """Generate ECS implementation code from scene definition"""

        if language == "python":
            return EntityComponentSystem._generate_python_ecs(scene)
        elif language == "javascript":
            return EntityComponentSystem._generate_js_ecs(scene)
        else:
            return "# ECS code generation not implemented for this language"

    @staticmethod
    def _generate_python_ecs(scene: Dict) -> str:
        """Generate Python ECS code"""

        code = '''"""
Entity Component System - Auto-generated
"""

class Entity:
    def __init__(self, name, entity_type):
        self.name = name
        self.type = entity_type
        self.components = {}
        self.tags = []

    def add_component(self, component_name, component_data):
        self.components[component_name] = component_data

    def get_component(self, component_name):
        return self.components.get(component_name)

    def has_component(self, component_name):
        return component_name in self.components


class Scene:
    def __init__(self):
        self.entities = []
        self.systems = []

    def add_entity(self, entity):
        self.entities.append(entity)
        return entity

    def get_entities_with_component(self, component_name):
        return [e for e in self.entities if e.has_component(component_name)]

    def update(self, dt):
        for system in self.systems:
            system.update(self, dt)


# Create scene from definition
def create_scene():
    scene = Scene()

'''

        # Add entity creation code
        for entity_def in scene.get("entities", []):
            code += f'''
    # Create {entity_def['name']}
    {entity_def['name'].lower().replace(' ', '_')} = Entity("{entity_def['name']}", "{entity_def['type']}")
'''
            # Add components
            for comp_name, comp_data in entity_def.get("components", {}).items():
                code += f'    {entity_def["name"].lower().replace(" ", "_")}.add_component("{comp_name}", {comp_data})\n'

            code += f'    scene.add_entity({entity_def["name"].lower().replace(" ", "_")})\n'

        code += '''
    return scene


if __name__ == "__main__":
    scene = create_scene()
    print(f"Scene loaded with {len(scene.entities)} entities")
'''

        return code

    @staticmethod
    def _generate_js_ecs(scene: Dict) -> str:
        """Generate JavaScript ECS code"""

        code = '''/**
 * Entity Component System - Auto-generated
 */

class Entity {
    constructor(name, type) {
        this.name = name;
        this.type = type;
        this.components = new Map();
        this.tags = [];
    }

    addComponent(componentName, componentData) {
        this.components.set(componentName, componentData);
    }

    getComponent(componentName) {
        return this.components.get(componentName);
    }

    hasComponent(componentName) {
        return this.components.has(componentName);
    }
}

class Scene {
    constructor() {
        this.entities = [];
        this.systems = [];
    }

    addEntity(entity) {
        this.entities.push(entity);
        return entity;
    }

    getEntitiesWithComponent(componentName) {
        return this.entities.filter(e => e.hasComponent(componentName));
    }

    update(dt) {
        for (const system of this.systems) {
            system.update(this, dt);
        }
    }
}

// Create scene from definition
function createScene() {
    const scene = new Scene();

'''

        # Add entity creation code
        for entity_def in scene.get("entities", []):
            var_name = entity_def['name'].lower().replace(' ', '_')
            code += f'''
    // Create {entity_def['name']}
    const {var_name} = new Entity("{entity_def['name']}", "{entity_def['type']}");
'''
            # Add components
            for comp_name, comp_data in entity_def.get("components", {}).items():
                code += f'    {var_name}.addComponent("{comp_name}", {json.dumps(comp_data)});\n'

            code += f'    scene.addEntity({var_name});\n'

        code += '''
    return scene;
}

// Initialize
const scene = createScene();
console.log(`Scene loaded with ${scene.entities.length} entities`);

export { Entity, Scene, createScene };
'''

        return code


class AssetManager:
    """Game asset management"""

    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.asset_manifest = {
            "sprites": [],
            "sounds": [],
            "music": [],
            "fonts": [],
            "tilemaps": [],
            "scripts": []
        }

    def scan_assets(self) -> Dict[str, List[str]]:
        """Scan project directory for game assets"""

        asset_extensions = {
            "sprites": ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.bmp'],
            "sounds": ['.wav', '.mp3', '.ogg', '.flac'],
            "music": ['.mp3', '.ogg', '.wav', '.mid'],
            "fonts": ['.ttf', '.otf', '.woff', '.woff2'],
            "tilemaps": ['.tmx', '.json'],
            "scripts": ['.py', '.js', '.ts', '.lua']
        }

        for asset_type, extensions in asset_extensions.items():
            for ext in extensions:
                found_files = list(self.project_path.rglob(f'*{ext}'))
                self.asset_manifest[asset_type].extend([
                    str(f.relative_to(self.project_path)) for f in found_files
                ])

        logger.info(f"Found {sum(len(v) for v in self.asset_manifest.values())} assets")
        return self.asset_manifest

    def generate_asset_loader(self, engine: str = "pygame") -> str:
        """Generate asset loading code"""

        if engine == "pygame":
            return self._generate_pygame_loader()
        elif engine == "phaser":
            return self._generate_phaser_loader()
        else:
            return "# Asset loader not implemented for this engine"

    def _generate_pygame_loader(self) -> str:
        """Generate Pygame asset loader"""

        code = '''"""
Asset Manager - Auto-generated asset loader
"""
import pygame
import os

class AssetManager:
    def __init__(self):
        self.sprites = {}
        self.sounds = {}
        self.music = {}
        self.fonts = {}

    def load_all_assets(self):
        """Load all game assets"""
        self.load_sprites()
        self.load_sounds()
        self.load_music()
        self.load_fonts()

    def load_sprites(self):
        """Load sprite images"""
'''

        for sprite in self.asset_manifest.get("sprites", []):
            sprite_name = Path(sprite).stem
            code += f'''        self.sprites['{sprite_name}'] = pygame.image.load('{sprite}').convert_alpha()\n'''

        code += '''
    def load_sounds(self):
        """Load sound effects"""
'''

        for sound in self.asset_manifest.get("sounds", []):
            sound_name = Path(sound).stem
            code += f'''        self.sounds['{sound_name}'] = pygame.mixer.Sound('{sound}')\n'''

        code += '''
    def load_music(self):
        """Load music tracks"""
        # Music is loaded on-demand
        pass

    def load_fonts(self):
        """Load fonts"""
'''

        for font in self.asset_manifest.get("fonts", []):
            font_name = Path(font).stem
            code += f'''        self.fonts['{font_name}'] = pygame.font.Font('{font}', 24)\n'''

        code += '''
    def get_sprite(self, name):
        return self.sprites.get(name)

    def get_sound(self, name):
        return self.sounds.get(name)

    def get_font(self, name):
        return self.fonts.get(name)
'''

        return code

    def _generate_phaser_loader(self) -> str:
        """Generate Phaser asset loader"""

        code = '''/**
 * Asset Manager - Auto-generated asset loader
 */

class AssetManager {
    preload(scene) {
        // Load sprites
'''

        for sprite in self.asset_manifest.get("sprites", []):
            sprite_name = Path(sprite).stem
            code += f'''        scene.load.image('{sprite_name}', '{sprite}');\n'''

        code += '''
        // Load sounds
'''

        for sound in self.asset_manifest.get("sounds", []):
            sound_name = Path(sound).stem
            code += f'''        scene.load.audio('{sound_name}', '{sound}');\n'''

        code += '''
    }

    getSprite(scene, name) {
        return scene.textures.get(name);
    }

    playSound(scene, name) {
        scene.sound.play(name);
    }
}

export default AssetManager;
'''

        return code

    def save_manifest(self, output_path: str = None):
        """Save asset manifest to JSON"""

        if output_path is None:
            output_path = self.project_path / "assets_manifest.json"

        with open(output_path, 'w') as f:
            json.dump(self.asset_manifest, f, indent=2)

        logger.info(f"Asset manifest saved to {output_path}")
