"""
Template Library Manager for Kroosybul AI
Manages project templates including custom, community, and battle-tested templates.
"""

import os
import json
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import zipfile
import tempfile


class TemplateLibrary:
    """Manages project templates"""

    def __init__(self, templates_dir: str = "templates_library"):
        """Initialize the template library

        Args:
            templates_dir: Directory to store templates
        """
        self.templates_dir = templates_dir
        self.custom_dir = os.path.join(templates_dir, "custom")
        self.community_dir = os.path.join(templates_dir, "community")
        self.builtin_dir = os.path.join(templates_dir, "builtin")

        # Create directories
        for directory in [self.custom_dir, self.community_dir, self.builtin_dir]:
            os.makedirs(directory, exist_ok=True)

        # Initialize builtin templates
        self._init_builtin_templates()

    def _init_builtin_templates(self):
        """Initialize builtin template definitions"""
        self.builtin_templates = {
            'web_app_full': {
                'id': 'web_app_full',
                'name': 'Full-Stack Web Application',
                'description': 'Complete web application with React frontend and Node.js/Express backend',
                'category': 'web',
                'tags': ['react', 'node', 'express', 'fullstack', 'api'],
                'languages': ['javascript', 'typescript'],
                'battle_tested': True,
                'structure': {
                    'frontend': {
                        'src': ['components', 'pages', 'hooks', 'utils', 'styles'],
                        'public': ['assets', 'images']
                    },
                    'backend': {
                        'src': ['controllers', 'models', 'routes', 'middleware', 'config'],
                        'tests': []
                    },
                    'shared': ['types', 'constants']
                },
                'dependencies': {
                    'frontend': ['react', 'react-dom', 'react-router-dom', 'axios'],
                    'backend': ['express', 'cors', 'dotenv', 'mongoose']
                }
            },
            'rest_api': {
                'id': 'rest_api',
                'name': 'RESTful API Server',
                'description': 'Production-ready REST API with authentication and database',
                'category': 'backend',
                'tags': ['api', 'rest', 'backend', 'authentication', 'database'],
                'languages': ['python', 'javascript', 'typescript'],
                'battle_tested': True,
                'structure': {
                    'src': ['api', 'models', 'schemas', 'middleware', 'utils'],
                    'tests': ['unit', 'integration'],
                    'config': []
                },
                'dependencies': {
                    'python': ['flask', 'flask-restful', 'flask-jwt-extended', 'sqlalchemy'],
                    'javascript': ['express', 'jsonwebtoken', 'bcrypt', 'joi']
                }
            },
            'microservice': {
                'id': 'microservice',
                'name': 'Microservice Template',
                'description': 'Containerized microservice with Docker and health checks',
                'category': 'backend',
                'tags': ['microservice', 'docker', 'api', 'cloud'],
                'languages': ['python', 'javascript', 'go'],
                'battle_tested': True,
                'structure': {
                    'src': ['handlers', 'services', 'models', 'config'],
                    'tests': [],
                    'deploy': ['docker', 'kubernetes']
                },
                'dependencies': {
                    'python': ['fastapi', 'uvicorn', 'pydantic'],
                    'javascript': ['express', 'helmet', 'compression'],
                    'go': ['gorilla/mux', 'prometheus/client_golang']
                }
            },
            'ml_project': {
                'id': 'ml_project',
                'name': 'Machine Learning Project',
                'description': 'ML project with data processing, training, and inference pipelines',
                'category': 'ml',
                'tags': ['machine-learning', 'data-science', 'ai', 'python'],
                'languages': ['python'],
                'battle_tested': True,
                'structure': {
                    'src': ['data', 'models', 'training', 'inference', 'utils'],
                    'notebooks': [],
                    'experiments': [],
                    'configs': []
                },
                'dependencies': {
                    'python': ['numpy', 'pandas', 'scikit-learn', 'matplotlib', 'jupyter']
                }
            },
            'cli_tool': {
                'id': 'cli_tool',
                'name': 'Command-Line Tool',
                'description': 'Professional CLI application with argument parsing and help',
                'category': 'tools',
                'tags': ['cli', 'tool', 'command-line'],
                'languages': ['python', 'rust', 'go'],
                'battle_tested': True,
                'structure': {
                    'src': ['commands', 'utils', 'config'],
                    'tests': []
                },
                'dependencies': {
                    'python': ['click', 'rich', 'pydantic'],
                    'rust': ['clap', 'serde'],
                    'go': ['cobra', 'viper']
                }
            },
            'game_2d': {
                'id': 'game_2d',
                'name': '2D Game Project',
                'description': '2D game with sprite rendering, physics, and input handling',
                'category': 'game',
                'tags': ['game', '2d', 'graphics', 'physics'],
                'languages': ['python', 'javascript'],
                'battle_tested': True,
                'structure': {
                    'src': ['entities', 'systems', 'assets', 'scenes', 'utils'],
                    'assets': ['sprites', 'sounds', 'fonts']
                },
                'dependencies': {
                    'python': ['pygame', 'pymunk'],
                    'javascript': ['phaser', 'matter-js']
                }
            },
            'desktop_app': {
                'id': 'desktop_app',
                'name': 'Desktop Application',
                'description': 'Cross-platform desktop application with modern UI',
                'category': 'desktop',
                'tags': ['desktop', 'gui', 'electron', 'cross-platform'],
                'languages': ['javascript', 'python'],
                'battle_tested': True,
                'structure': {
                    'src': ['main', 'renderer', 'components', 'utils'],
                    'assets': []
                },
                'dependencies': {
                    'javascript': ['electron', 'electron-builder'],
                    'python': ['PyQt5', 'pyinstaller']
                }
            },
            'data_pipeline': {
                'id': 'data_pipeline',
                'name': 'Data Processing Pipeline',
                'description': 'ETL pipeline for data extraction, transformation, and loading',
                'category': 'data',
                'tags': ['data', 'etl', 'pipeline', 'batch-processing'],
                'languages': ['python'],
                'battle_tested': True,
                'structure': {
                    'src': ['extractors', 'transformers', 'loaders', 'config'],
                    'pipelines': [],
                    'tests': []
                },
                'dependencies': {
                    'python': ['pandas', 'apache-airflow', 'sqlalchemy', 'pyyaml']
                }
            }
        }

    def get_template(self, template_id: str) -> Optional[Dict[str, Any]]:
        """Get a template by ID

        Args:
            template_id: Template identifier

        Returns:
            Template dictionary or None if not found
        """
        # Check builtin
        if template_id in self.builtin_templates:
            return self.builtin_templates[template_id]

        # Check custom
        custom_path = os.path.join(self.custom_dir, f"{template_id}.json")
        if os.path.exists(custom_path):
            with open(custom_path, 'r') as f:
                return json.load(f)

        # Check community
        community_path = os.path.join(self.community_dir, f"{template_id}.json")
        if os.path.exists(community_path):
            with open(community_path, 'r') as f:
                return json.load(f)

        return None

    def list_templates(self, category: Optional[str] = None,
                      language: Optional[str] = None,
                      battle_tested: bool = False) -> List[Dict[str, Any]]:
        """List all available templates

        Args:
            category: Filter by category
            language: Filter by language support
            battle_tested: Show only battle-tested templates

        Returns:
            List of template dictionaries
        """
        templates = []

        # Add builtin templates
        for template in self.builtin_templates.values():
            if self._matches_filters(template, category, language, battle_tested):
                templates.append(template)

        # Add custom templates
        for filename in os.listdir(self.custom_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.custom_dir, filename)
                with open(filepath, 'r') as f:
                    template = json.load(f)
                    if self._matches_filters(template, category, language, battle_tested):
                        template['source'] = 'custom'
                        templates.append(template)

        # Add community templates
        for filename in os.listdir(self.community_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.community_dir, filename)
                with open(filepath, 'r') as f:
                    template = json.load(f)
                    if self._matches_filters(template, category, language, battle_tested):
                        template['source'] = 'community'
                        templates.append(template)

        return templates

    def _matches_filters(self, template: Dict[str, Any], category: Optional[str],
                        language: Optional[str], battle_tested: bool) -> bool:
        """Check if template matches filters"""
        if category and template.get('category') != category:
            return False

        if language and language not in template.get('languages', []):
            return False

        if battle_tested and not template.get('battle_tested', False):
            return False

        return True

    def create_template(self, template_data: Dict[str, Any],
                       source: str = 'custom') -> Tuple[bool, str]:
        """Create a new template

        Args:
            template_data: Template configuration
            source: Template source ('custom' or 'community')

        Returns:
            Tuple of (success, message)
        """
        try:
            # Validate required fields
            required_fields = ['id', 'name', 'description', 'category', 'languages']
            for field in required_fields:
                if field not in template_data:
                    return False, f"Missing required field: {field}"

            # Add metadata
            template_data['created_at'] = datetime.now().isoformat()
            template_data['version'] = '1.0.0'

            # Determine directory
            if source == 'custom':
                directory = self.custom_dir
            elif source == 'community':
                directory = self.community_dir
            else:
                return False, f"Invalid source: {source}"

            # Save template
            filepath = os.path.join(directory, f"{template_data['id']}.json")
            with open(filepath, 'w') as f:
                json.dump(template_data, f, indent=2)

            return True, f"Template '{template_data['name']}' created successfully"
        except Exception as e:
            return False, f"Error creating template: {str(e)}"

    def delete_template(self, template_id: str) -> Tuple[bool, str]:
        """Delete a custom or community template

        Args:
            template_id: Template identifier

        Returns:
            Tuple of (success, message)
        """
        try:
            # Cannot delete builtin templates
            if template_id in self.builtin_templates:
                return False, "Cannot delete builtin templates"

            # Check custom
            custom_path = os.path.join(self.custom_dir, f"{template_id}.json")
            if os.path.exists(custom_path):
                os.remove(custom_path)
                return True, "Template deleted successfully"

            # Check community
            community_path = os.path.join(self.community_dir, f"{template_id}.json")
            if os.path.exists(community_path):
                os.remove(community_path)
                return True, "Template deleted successfully"

            return False, "Template not found"
        except Exception as e:
            return False, f"Error deleting template: {str(e)}"

    def export_template(self, template_id: str, output_path: str) -> Tuple[bool, str]:
        """Export a template to a file

        Args:
            template_id: Template identifier
            output_path: Path to save the exported template

        Returns:
            Tuple of (success, message)
        """
        try:
            template = self.get_template(template_id)
            if not template:
                return False, "Template not found"

            # Create a zip file with the template
            with zipfile.ZipFile(output_path, 'w') as zipf:
                # Add template definition
                template_json = json.dumps(template, indent=2)
                zipf.writestr('template.json', template_json)

                # Add README
                readme = f"""# {template['name']}

{template['description']}

## Category
{template['category']}

## Supported Languages
{', '.join(template['languages'])}

## Tags
{', '.join(template.get('tags', []))}

## Created
{template.get('created_at', 'Unknown')}

## Version
{template.get('version', '1.0.0')}
"""
                zipf.writestr('README.md', readme)

            return True, f"Template exported to {output_path}"
        except Exception as e:
            return False, f"Error exporting template: {str(e)}"

    def import_template(self, import_path: str, source: str = 'custom') -> Tuple[bool, str]:
        """Import a template from a file

        Args:
            import_path: Path to the template file (zip or json)
            source: Where to import the template ('custom' or 'community')

        Returns:
            Tuple of (success, message)
        """
        try:
            template_data = None

            # Handle zip files
            if import_path.endswith('.zip'):
                with zipfile.ZipFile(import_path, 'r') as zipf:
                    # Extract template.json
                    with zipf.open('template.json') as f:
                        template_data = json.load(f)

            # Handle JSON files
            elif import_path.endswith('.json'):
                with open(import_path, 'r') as f:
                    template_data = json.load(f)
            else:
                return False, "Invalid file format. Use .zip or .json"

            if not template_data:
                return False, "Failed to read template data"

            # Create the template
            return self.create_template(template_data, source)
        except Exception as e:
            return False, f"Error importing template: {str(e)}"

    def get_categories(self) -> List[str]:
        """Get all unique template categories

        Returns:
            List of category names
        """
        categories = set()

        # From builtin
        for template in self.builtin_templates.values():
            categories.add(template['category'])

        # From custom
        for filename in os.listdir(self.custom_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.custom_dir, filename)
                with open(filepath, 'r') as f:
                    template = json.load(f)
                    categories.add(template.get('category', 'other'))

        # From community
        for filename in os.listdir(self.community_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.community_dir, filename)
                with open(filepath, 'r') as f:
                    template = json.load(f)
                    categories.add(template.get('category', 'other'))

        return sorted(list(categories))

    def search_templates(self, query: str) -> List[Dict[str, Any]]:
        """Search templates by name, description, or tags

        Args:
            query: Search query

        Returns:
            List of matching templates
        """
        query = query.lower()
        results = []

        all_templates = self.list_templates()

        for template in all_templates:
            # Search in name
            if query in template['name'].lower():
                results.append(template)
                continue

            # Search in description
            if query in template['description'].lower():
                results.append(template)
                continue

            # Search in tags
            tags = template.get('tags', [])
            if any(query in tag.lower() for tag in tags):
                results.append(template)
                continue

        return results
