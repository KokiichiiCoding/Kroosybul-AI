"""
Game AI Features - AI-powered game development tools
"""

import json
import logging
import random
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)


class AILevelDesigner:
    """AI-powered procedural level generation"""

    def __init__(self, ai_engine):
        self.ai_engine = ai_engine

    def generate_level(self, level_specs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a game level based on specifications

        Args:
            level_specs: Dictionary with level requirements
                - game_type: platformer, rpg, puzzle, etc.
                - theme: desert, forest, sci-fi, etc.
                - size: small, medium, large
                - difficulty: easy, medium, hard
                - features: list of required features

        Returns:
            Level data including tilemap, entity placements, etc.
        """
        logger.info(f"Generating {level_specs.get('theme', 'generic')} level...")

        prompt = f"""Design a {level_specs.get('game_type', 'game')} level with these specifications:

Theme: {level_specs.get('theme', 'generic')}
Size: {level_specs.get('size', 'medium')}
Difficulty: {level_specs.get('difficulty', 'medium')}
Features: {', '.join(level_specs.get('features', []))}

Provide a JSON response with:
{{
    "name": "level name",
    "description": "level description",
    "tilemap": {{
        "width": width_in_tiles,
        "height": height_in_tiles,
        "tiles": "2D array or description"
    }},
    "entities": [
        {{
            "type": "enemy/item/obstacle",
            "position": [x, y],
            "properties": {{}},
        }}
    ],
    "spawn_points": {{
        "player": [x, y],
        "enemies": [[x1, y1], [x2, y2]]
    }},
    "objectives": ["objective descriptions"],
    "layout_description": "textual description of the level layout"
}}

Respond with ONLY the JSON object."""

        try:
            response = self.ai_engine.client.messages.create(
                model=self.ai_engine.model,
                max_tokens=3000,
                temperature=0.8,
                messages=[{"role": "user", "content": prompt}]
            )

            response_text = response.content[0].text.strip()

            # Extract JSON
            if '```json' in response_text:
                response_text = response_text.split('```json')[1].split('```')[0].strip()
            elif '```' in response_text:
                response_text = response_text.split('```')[1].split('```')[0].strip()

            level_data = json.loads(response_text)
            logger.info(f"Level generated: {level_data.get('name', 'Unnamed')}")

            return level_data

        except Exception as e:
            logger.error(f"Error generating level: {e}")
            return self._generate_fallback_level(level_specs)

    def _generate_fallback_level(self, specs: Dict) -> Dict:
        """Generate a simple fallback level"""

        return {
            "name": f"{specs.get('theme', 'Generic')} Level",
            "description": "A procedurally generated level",
            "tilemap": {
                "width": 20,
                "height": 15,
                "tiles": "Auto-generated tilemap"
            },
            "entities": [
                {"type": "enemy", "position": [10, 5], "properties": {}},
                {"type": "item", "position": [15, 8], "properties": {"item_type": "coin"}},
            ],
            "spawn_points": {
                "player": [2, 2],
                "enemies": [[10, 5], [15, 10]]
            },
            "objectives": ["Reach the exit", "Collect all items"],
            "layout_description": "A simple level layout"
        }

    def generate_tilemap_code(self, level_data: Dict, engine: str = "pygame") -> str:
        """Generate code to render the tilemap"""

        if engine == "pygame":
            return self._generate_pygame_tilemap(level_data)
        elif engine == "phaser":
            return self._generate_phaser_tilemap(level_data)
        else:
            return "# Tilemap code not implemented"

    def _generate_pygame_tilemap(self, level_data: Dict) -> str:
        """Generate Pygame tilemap code"""

        return f'''"""
Tilemap Renderer - {level_data.get('name', 'Level')}
"""
import pygame

class Tilemap:
    def __init__(self, tile_size=32):
        self.tile_size = tile_size
        self.width = {level_data['tilemap']['width']}
        self.height = {level_data['tilemap']['height']}
        self.tiles = self.generate_tilemap()

    def generate_tilemap(self):
        """Generate or load tilemap data"""
        # TODO: Load actual tilemap data
        tilemap = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                # 0 = empty, 1 = ground, 2 = wall, etc.
                tile_type = 1 if y > self.height // 2 else 0
                row.append(tile_type)
            tilemap.append(row)
        return tilemap

    def get_tile(self, x, y):
        """Get tile at position"""
        if 0 <= y < len(self.tiles) and 0 <= x < len(self.tiles[0]):
            return self.tiles[y][x]
        return 0

    def render(self, screen, camera_offset=(0, 0)):
        """Render the tilemap"""
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                if tile == 0:
                    continue  # Empty tile

                # Calculate screen position
                screen_x = x * self.tile_size - camera_offset[0]
                screen_y = y * self.tile_size - camera_offset[1]

                # Tile colors (replace with sprites)
                colors = {{
                    1: (139, 69, 19),   # Brown (ground)
                    2: (128, 128, 128),  # Gray (wall)
                    3: (34, 139, 34),    # Green (grass)
                }}

                color = colors.get(tile, (255, 255, 255))
                rect = pygame.Rect(screen_x, screen_y, self.tile_size, self.tile_size)
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, (0, 0, 0), rect, 1)  # Border
'''

    def _generate_phaser_tilemap(self, level_data: Dict) -> str:
        """Generate Phaser tilemap code"""

        return f'''/**
 * Tilemap - {level_data.get('name', 'Level')}
 */

class Tilemap {{
    constructor(scene) {{
        this.scene = scene;
        this.tileSize = 32;
        this.width = {level_data['tilemap']['width']};
        this.height = {level_data['tilemap']['height']};

        this.create();
    }}

    create() {{
        // Create tilemap
        const map = this.scene.make.tilemap({{
            width: this.width,
            height: this.height,
            tileWidth: this.tileSize,
            tileHeight: this.tileSize
        }});

        // Add tileset
        const tiles = map.addTilesetImage('tiles');

        // Create layers
        const groundLayer = map.createBlankLayer('Ground', tiles);
        const wallLayer = map.createBlankLayer('Walls', tiles);

        // TODO: Fill in tilemap data
        // groundLayer.fill(1);  // Fill with ground tiles

        // Enable collisions
        wallLayer.setCollisionByExclusion([-1]);
    }}
}}

export default Tilemap;
'''


class NPCBehaviorGenerator:
    """Generate AI behaviors for NPCs"""

    def __init__(self, ai_engine):
        self.ai_engine = ai_engine

    def generate_behavior(self, npc_spec: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate NPC behavior logic

        Args:
            npc_spec: NPC specifications
                - npc_type: enemy, ally, neutral
                - behavior: patrol, chase, wander, static
                - properties: health, speed, detection_range

        Returns:
            Behavior tree or state machine definition
        """
        logger.info(f"Generating behavior for {npc_spec.get('npc_type', 'NPC')}...")

        prompt = f"""Create an NPC behavior system for a game with these specifications:

NPC Type: {npc_spec.get('npc_type', 'enemy')}
Behavior: {npc_spec.get('behavior', 'patrol')}
Properties: {json.dumps(npc_spec.get('properties', {}), indent=2)}

Provide a JSON response with:
{{
    "behavior_tree": {{
        "root": {{
            "type": "selector/sequence/parallel",
            "children": []
        }}
    }},
    "states": [
        {{
            "name": "idle/patrol/chase/attack",
            "conditions": ["condition descriptions"],
            "actions": ["action descriptions"],
            "transitions": {{"target_state": "condition"}}
        }}
    ],
    "parameters": {{
        "detection_range": value,
        "speed": value,
        "aggression": value
    }},
    "description": "plain English description of the behavior"
}}

Respond with ONLY the JSON object."""

        try:
            response = self.ai_engine.client.messages.create(
                model=self.ai_engine.model,
                max_tokens=2000,
                temperature=0.7,
                messages=[{"role": "user", "content": prompt}]
            )

            response_text = response.content[0].text.strip()

            # Extract JSON
            if '```json' in response_text:
                response_text = response_text.split('```json')[1].split('```')[0].strip()
            elif '```' in response_text:
                response_text = response_text.split('```')[1].split('```')[0].strip()

            behavior_data = json.loads(response_text)
            logger.info("NPC behavior generated successfully")

            return behavior_data

        except Exception as e:
            logger.error(f"Error generating NPC behavior: {e}")
            return self._generate_fallback_behavior(npc_spec)

    def _generate_fallback_behavior(self, spec: Dict) -> Dict:
        """Generate a simple fallback behavior"""

        behavior = spec.get('behavior', 'patrol')

        return {
            "behavior_tree": {
                "root": {
                    "type": "selector",
                    "children": [
                        {"type": "action", "name": behavior}
                    ]
                }
            },
            "states": [
                {
                    "name": "idle",
                    "conditions": ["no player detected"],
                    "actions": ["stand still", "look around"],
                    "transitions": {"patrol": "timer expired", "chase": "player detected"}
                },
                {
                    "name": "patrol",
                    "conditions": ["on patrol route"],
                    "actions": ["move along path", "check for player"],
                    "transitions": {"idle": "reached waypoint", "chase": "player detected"}
                },
                {
                    "name": "chase",
                    "conditions": ["player in range"],
                    "actions": ["move towards player", "prepare attack"],
                    "transitions": {"attack": "in attack range", "patrol": "lost sight"}
                }
            ],
            "parameters": {
                "detection_range": spec.get('properties', {}).get('detection_range', 100),
                "speed": spec.get('properties', {}).get('speed', 50),
                "aggression": 0.7
            },
            "description": f"Simple {behavior} behavior for NPC"
        }

    def generate_behavior_code(self, behavior_data: Dict, language: str = "python") -> str:
        """Generate code implementation of behavior"""

        if language == "python":
            return self._generate_python_behavior(behavior_data)
        elif language == "javascript":
            return self._generate_js_behavior(behavior_data)
        else:
            return "# Behavior code not implemented"

    def _generate_python_behavior(self, behavior_data: Dict) -> str:
        """Generate Python behavior code"""

        code = '''"""
NPC Behavior - Auto-generated AI behavior
"""
import math

class NPCBehavior:
    def __init__(self, npc):
        self.npc = npc
        self.current_state = "idle"
        self.parameters = ''' + json.dumps(behavior_data.get('parameters', {}), indent=8) + '''

        # Behavior states
        self.states = {}
        self.setup_states()

    def setup_states(self):
        """Initialize behavior states"""
'''

        for state in behavior_data.get('states', []):
            code += f'''
        # State: {state['name']}
        self.states['{state['name']}'] = {{
            'update': self.state_{state['name']},
            'enter': self.enter_{state['name']},
            'exit': self.exit_{state['name']}
        }}
'''

        code += '''
    def update(self, dt, game_world):
        """Update NPC behavior"""
        state_func = self.states.get(self.current_state, {}).get('update')
        if state_func:
            state_func(dt, game_world)

        self.check_transitions(game_world)

    def check_transitions(self, game_world):
        """Check for state transitions"""
        # TODO: Implement state transition logic
        pass

    def change_state(self, new_state):
        """Change to a new state"""
        if new_state == self.current_state:
            return

        # Exit current state
        exit_func = self.states.get(self.current_state, {}).get('exit')
        if exit_func:
            exit_func()

        # Enter new state
        self.current_state = new_state
        enter_func = self.states.get(new_state, {}).get('enter')
        if enter_func:
            enter_func()

'''

        # Generate state methods
        for state in behavior_data.get('states', []):
            state_name = state['name']
            code += f'''
    def state_{state_name}(self, dt, game_world):
        """State: {state_name}"""
        # Actions: {', '.join(state.get('actions', []))}
        pass

    def enter_{state_name}(self):
        """Enter {state_name} state"""
        pass

    def exit_{state_name}(self):
        """Exit {state_name} state"""
        pass
'''

        return code

    def _generate_js_behavior(self, behavior_data: Dict) -> str:
        """Generate JavaScript behavior code"""

        code = '''/**
 * NPC Behavior - Auto-generated AI behavior
 */

class NPCBehavior {
    constructor(npc) {
        this.npc = npc;
        this.currentState = 'idle';
        this.parameters = ''' + json.dumps(behavior_data.get('parameters', {}), indent=8) + ''';

        this.states = {};
        this.setupStates();
    }

    setupStates() {
        // Initialize behavior states
'''

        for state in behavior_data.get('states', []):
            code += f'''
        // State: {state['name']}
        this.states['{state['name']}'] = {{
            update: (dt, gameWorld) => this.state{state['name'].capitalize()}(dt, gameWorld),
            enter: () => this.enter{state['name'].capitalize()}(),
            exit: () => this.exit{state['name'].capitalize()}()
        }};
'''

        code += '''
    }

    update(dt, gameWorld) {
        const state = this.states[this.currentState];
        if (state && state.update) {
            state.update(dt, gameWorld);
        }

        this.checkTransitions(gameWorld);
    }

    checkTransitions(gameWorld) {
        // TODO: Implement state transition logic
    }

    changeState(newState) {
        if (newState === this.currentState) {
            return;
        }

        // Exit current state
        const currentState = this.states[this.currentState];
        if (currentState && currentState.exit) {
            currentState.exit();
        }

        // Enter new state
        this.currentState = newState;
        const nextState = this.states[newState];
        if (nextState && nextState.enter) {
            nextState.enter();
        }
    }

'''

        # Generate state methods
        for state in behavior_data.get('states', []):
            state_name = state['name'].capitalize()
            code += f'''
    state{state_name}(dt, gameWorld) {{
        // State: {state['name']}
        // Actions: {', '.join(state.get('actions', []))}
    }}

    enter{state_name}() {{
        // Enter {state['name']} state
    }}

    exit{state_name}() {{
        // Exit {state['name']} state
    }}
'''

        code += '''
}

export default NPCBehavior;
'''

        return code


class DialogueSystem:
    """Dialogue and quest system generator"""

    @staticmethod
    def create_dialogue_tree(character_name: str, dialogues: List[Dict]) -> Dict:
        """
        Create a dialogue tree structure

        Args:
            character_name: NPC name
            dialogues: List of dialogue nodes

        Returns:
            Dialogue tree JSON
        """

        return {
            "character": character_name,
            "dialogue_tree": {
                "root": "start",
                "nodes": {
                    node['id']: {
                        "text": node['text'],
                        "options": node.get('options', []),
                        "conditions": node.get('conditions', []),
                        "effects": node.get('effects', [])
                    }
                    for node in dialogues
                }
            }
        }

    @staticmethod
    def generate_dialogue_with_ai(ai_engine, character_info: Dict) -> Dict:
        """Use AI to generate character dialogue"""

        prompt = f"""Create dialogue for an NPC with these characteristics:

Name: {character_info.get('name', 'Character')}
Personality: {character_info.get('personality', 'friendly')}
Role: {character_info.get('role', 'quest giver')}
Context: {character_info.get('context', 'fantasy RPG')}

Generate a branching dialogue tree with at least 3 conversation paths.

Provide JSON format:
{{
    "dialogues": [
        {{
            "id": "start",
            "text": "dialogue text",
            "options": [
                {{"text": "option text", "next": "node_id"}},
            ]
        }}
    ]
}}

Respond with ONLY the JSON object."""

        try:
            response = ai_engine.client.messages.create(
                model=ai_engine.model,
                max_tokens=2000,
                temperature=0.8,
                messages=[{"role": "user", "content": prompt}]
            )

            response_text = response.content[0].text.strip()

            # Extract JSON
            if '```json' in response_text:
                response_text = response_text.split('```json')[1].split('```')[0].strip()
            elif '```' in response_text:
                response_text = response_text.split('```')[1].split('```')[0].strip()

            dialogue_data = json.loads(response_text)
            return dialogue_data

        except Exception as e:
            logger.error(f"Error generating dialogue: {e}")
            return {"dialogues": []}

    @staticmethod
    def generate_dialogue_code(dialogue_tree: Dict, language: str = "python") -> str:
        """Generate dialogue system code"""

        if language == "python":
            code = '''"""
Dialogue System
"""

class DialogueManager:
    def __init__(self):
        self.current_node = "start"
        self.dialogue_tree = ''' + json.dumps(dialogue_tree, indent=8) + '''

    def get_current_dialogue(self):
        """Get current dialogue node"""
        node = self.dialogue_tree['dialogue_tree']['nodes'].get(self.current_node)
        return node

    def choose_option(self, option_index):
        """Select a dialogue option"""
        node = self.get_current_dialogue()
        if node and 'options' in node:
            if 0 <= option_index < len(node['options']):
                selected = node['options'][option_index]
                self.current_node = selected.get('next', 'start')
                return True
        return False

    def reset(self):
        """Reset dialogue to start"""
        self.current_node = "start"
'''
            return code

        else:  # JavaScript
            code = '''/**
 * Dialogue System
 */

class DialogueManager {
    constructor() {
        this.currentNode = 'start';
        this.dialogueTree = ''' + json.dumps(dialogue_tree, indent=8) + ''';
    }

    getCurrentDialogue() {
        return this.dialogueTree.dialogue_tree.nodes[this.currentNode];
    }

    chooseOption(optionIndex) {
        const node = this.getCurrentDialogue();
        if (node && node.options && optionIndex < node.options.length) {
            const selected = node.options[optionIndex];
            this.currentNode = selected.next || 'start';
            return true;
        }
        return false;
    }

    reset() {
        this.currentNode = 'start';
    }
}

export default DialogueManager;
'''
            return code


class GameDesignDocGenerator:
    """Generate comprehensive game design documents"""

    def __init__(self, ai_engine):
        self.ai_engine = ai_engine

    def generate_gdd(self, project_info: Dict) -> str:
        """
        Generate a Game Design Document

        Args:
            project_info: Project metadata and files

        Returns:
            Markdown formatted GDD
        """
        logger.info("Generating Game Design Document...")

        prompt = f"""Create a comprehensive Game Design Document (GDD) for this project:

Project Name: {project_info.get('name', 'Game Project')}
Game Type: {project_info.get('project_type', 'game')}
Language: {project_info.get('language', 'python')}
Description: {project_info.get('description', 'A game project')}

Files in project: {len(project_info.get('files', []))}

Generate a professional GDD with these sections:

1. Game Overview
   - Title
   - Concept
   - Genre
   - Target Audience
   - Platform

2. Gameplay Mechanics
   - Core Loop
   - Controls
   - Player Progression

3. Game World
   - Setting
   - Levels/Stages
   - Characters/NPCs

4. Technical Specifications
   - Engine/Framework
   - System Requirements
   - Development Tools

5. Art and Audio
   - Visual Style
   - Sound Design
   - Music

6. Development Plan
   - Milestones
   - Team Roles
   - Timeline

Format as a professional markdown document."""

        try:
            response = self.ai_engine.client.messages.create(
                model=self.ai_engine.model,
                max_tokens=4000,
                temperature=0.7,
                messages=[{"role": "user", "content": prompt}]
            )

            gdd = response.content[0].text.strip()
            logger.info("GDD generated successfully")

            return gdd

        except Exception as e:
            logger.error(f"Error generating GDD: {e}")
            return self._generate_fallback_gdd(project_info)

    def _generate_fallback_gdd(self, project_info: Dict) -> str:
        """Generate a basic fallback GDD"""

        return f"""# Game Design Document

## {project_info.get('name', 'Game Project')}

### 1. Game Overview

**Title:** {project_info.get('name', 'Game Project')}

**Concept:** {project_info.get('description', 'A game project')}

**Genre:** {project_info.get('project_type', 'game')}

**Platform:** {project_info.get('language', 'python')}

### 2. Gameplay Mechanics

- Core gameplay loop
- Player controls
- Game objectives

### 3. Game World

- Setting and environment
- Levels and stages
- Characters and NPCs

### 4. Technical Specifications

**Engine/Framework:** Based on {project_info.get('language', 'python')}

**Files:** {len(project_info.get('files', []))} files generated

### 5. Development Plan

- Phase 1: Core mechanics
- Phase 2: Content creation
- Phase 3: Polish and testing
"""
