"""
Project Generator - Creates project structures and files
"""

import os
import shutil
import logging
import json
from pathlib import Path
from typing import Dict, List, Any, Callable, Optional
from datetime import datetime
import zipfile

from .ai_engine import AIEngine

logger = logging.getLogger(__name__)


class ProjectGenerator:
    """Generates complete project structures with AI-generated code"""

    def __init__(self):
        self.ai_engine = AIEngine()
        self.base_dir = Path(os.getenv('GENERATED_PROJECTS_DIR', 'generated_projects'))
        self.base_dir.mkdir(exist_ok=True)

        # Language-specific configurations
        self.language_configs = {
            'python': {
                'extensions': ['.py'],
                'main_file': 'main.py',
                'config_files': ['requirements.txt', 'setup.py', '.gitignore'],
                'test_command': 'python -m py_compile'
            },
            'javascript': {
                'extensions': ['.js'],
                'main_file': 'index.js',
                'config_files': ['package.json', '.gitignore'],
                'test_command': 'node --check'
            },
            'typescript': {
                'extensions': ['.ts'],
                'main_file': 'index.ts',
                'config_files': ['package.json', 'tsconfig.json', '.gitignore'],
                'test_command': 'tsc --noEmit'
            },
            'java': {
                'extensions': ['.java'],
                'main_file': 'Main.java',
                'config_files': ['pom.xml', '.gitignore'],
                'test_command': 'javac'
            },
            'cpp': {
                'extensions': ['.cpp', '.h'],
                'main_file': 'main.cpp',
                'config_files': ['CMakeLists.txt', '.gitignore'],
                'test_command': 'g++ -fsyntax-only'
            },
            'rust': {
                'extensions': ['.rs'],
                'main_file': 'main.rs',
                'config_files': ['Cargo.toml', '.gitignore'],
                'test_command': 'cargo check'
            },
            'go': {
                'extensions': ['.go'],
                'main_file': 'main.go',
                'config_files': ['go.mod', '.gitignore'],
                'test_command': 'go build'
            }
        }

    def generate_project(
        self,
        project_plan: Dict[str, Any],
        progress_callback: Optional[Callable[[str], None]] = None
    ) -> Dict[str, Any]:
        """
        Generate a complete project from a plan

        Args:
            project_plan: Project specification from AI
            progress_callback: Optional callback for progress updates

        Returns:
            Dictionary with project information
        """
        logger.info(f"Generating project: {project_plan['project_name']}")

        # Create project directory
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        project_name = f"{project_plan['project_name']}_{timestamp}"
        project_path = self.base_dir / project_name

        project_path.mkdir(parents=True, exist_ok=True)

        if progress_callback:
            progress_callback(f"Created project directory: {project_name}")

        # Generate files
        generated_files = []
        total_files = len(project_plan.get('files', []))

        for idx, file_info in enumerate(project_plan.get('files', []), 1):
            if progress_callback:
                progress_callback(f"Generating file {idx}/{total_files}: {file_info['path']}")

            try:
                file_content = self.ai_engine.generate_file_content(file_info, project_plan)
                file_path = project_path / file_info['path']

                # Create parent directories
                file_path.parent.mkdir(parents=True, exist_ok=True)

                # Write file
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(file_content)

                generated_files.append(file_info['path'])
                logger.info(f"Generated: {file_info['path']}")

            except Exception as e:
                logger.error(f"Error generating {file_info['path']}: {e}", exc_info=True)
                if progress_callback:
                    progress_callback(f"Warning: Failed to generate {file_info['path']}")

        # Generate language-specific config files
        self._generate_config_files(project_path, project_plan)

        # Generate comprehensive README
        self._generate_readme(project_path, project_plan)

        # Save project metadata
        metadata = {
            'name': project_plan['project_name'],
            'language': project_plan['language'],
            'project_type': project_plan['project_type'],
            'created_at': datetime.utcnow().isoformat(),
            'files': generated_files,
            'plan': project_plan
        }

        with open(project_path / '.kroosybul_metadata.json', 'w') as f:
            json.dump(metadata, f, indent=2)

        if progress_callback:
            progress_callback(f"Project generation complete! Created {len(generated_files)} files.")

        return {
            'name': project_name,
            'path': str(project_path),
            'language': project_plan['language'],
            'files': generated_files,
            'metadata': metadata
        }

    def _generate_config_files(self, project_path: Path, project_plan: Dict):
        """Generate language-specific configuration files"""
        language = project_plan['language'].lower()

        if language == 'python':
            # requirements.txt
            deps = project_plan.get('dependencies', [])
            if deps:
                with open(project_path / 'requirements.txt', 'w') as f:
                    f.write('\n'.join(deps))

            # .gitignore
            gitignore_content = """__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
.env
.venv
"""
            with open(project_path / '.gitignore', 'w') as f:
                f.write(gitignore_content)

        elif language == 'javascript' or language == 'typescript':
            # package.json
            package_json = {
                "name": project_plan['project_name'],
                "version": "1.0.0",
                "description": project_plan['description'],
                "main": "index.js" if language == 'javascript' else "dist/index.js",
                "scripts": {
                    "start": "node index.js" if language == 'javascript' else "ts-node index.ts",
                    "build": "tsc" if language == 'typescript' else "echo 'No build needed'",
                    "test": "echo 'Tests not configured'"
                },
                "dependencies": {}
            }

            # Add dependencies
            for dep in project_plan.get('dependencies', []):
                package_json['dependencies'][dep] = "latest"

            with open(project_path / 'package.json', 'w') as f:
                json.dump(package_json, f, indent=2)

            # TypeScript config
            if language == 'typescript':
                tsconfig = {
                    "compilerOptions": {
                        "target": "ES2020",
                        "module": "commonjs",
                        "outDir": "./dist",
                        "rootDir": "./",
                        "strict": True,
                        "esModuleInterop": True,
                        "skipLibCheck": True,
                        "forceConsistentCasingInFileNames": True
                    }
                }
                with open(project_path / 'tsconfig.json', 'w') as f:
                    json.dump(tsconfig, f, indent=2)

            # .gitignore
            gitignore_content = """node_modules/
dist/
.env
*.log
"""
            with open(project_path / '.gitignore', 'w') as f:
                f.write(gitignore_content)

        elif language == 'rust':
            # Cargo.toml
            cargo_toml = f"""[package]
name = "{project_plan['project_name']}"
version = "0.1.0"
edition = "2021"

[dependencies]
"""
            for dep in project_plan.get('dependencies', []):
                cargo_toml += f'{dep} = "latest"\n'

            with open(project_path / 'Cargo.toml', 'w') as f:
                f.write(cargo_toml)

        elif language == 'go':
            # go.mod
            go_mod = f"""module {project_plan['project_name']}

go 1.21

require (
)
"""
            with open(project_path / 'go.mod', 'w') as f:
                f.write(go_mod)

    def _generate_readme(self, project_path: Path, project_plan: Dict):
        """Generate comprehensive README file"""
        readme_content = f"""# {project_plan['project_name']}

{project_plan['description']}

## Features

{chr(10).join(f"- {feature}" for feature in project_plan.get('features', []))}

## Technology Stack

- **Language:** {project_plan['language']}
- **Frameworks:** {', '.join(project_plan.get('frameworks', [])) or 'None'}
- **Project Type:** {project_plan['project_type']}

## Setup Instructions

{project_plan.get('setup_instructions', 'See below for default setup instructions.')}

### Prerequisites

"""

        # Add language-specific setup
        language = project_plan['language'].lower()

        if language == 'python':
            readme_content += """- Python 3.8 or higher
- pip package manager

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Run the project
python main.py
```
"""
        elif language == 'javascript':
            readme_content += """- Node.js 14 or higher
- npm package manager

### Installation

```bash
# Install dependencies
npm install

# Run the project
npm start
```
"""
        elif language == 'typescript':
            readme_content += """- Node.js 14 or higher
- npm package manager

### Installation

```bash
# Install dependencies
npm install

# Build the project
npm run build

# Run the project
npm start
```
"""
        elif language == 'rust':
            readme_content += """- Rust 1.70 or higher
- Cargo package manager

### Installation

```bash
# Build and run
cargo run

# Build for release
cargo build --release
```
"""
        elif language == 'go':
            readme_content += """- Go 1.21 or higher

### Installation

```bash
# Build and run
go run main.go

# Build executable
go build
```
"""

        readme_content += f"""
## Project Structure

```
{project_plan['project_name']}/
"""

        for file_info in project_plan.get('files', []):
            readme_content += f"├── {file_info['path']:<30} # {file_info['purpose']}\n"

        readme_content += """```

## Dependencies

"""
        deps = project_plan.get('dependencies', [])
        if deps:
            readme_content += '\n'.join(f"- {dep}" for dep in deps)
        else:
            readme_content += "No external dependencies required."

        readme_content += """

## Usage

Follow the setup instructions above, then run the main file for your language.

## Contributing

Feel free to fork this project and submit pull requests for improvements!

## License

MIT License - Feel free to use this project however you'd like.

---

*Generated by Kroosybul AI - Your AI-Powered Project Generator*
"""

        with open(project_path / 'README.md', 'w') as f:
            f.write(readme_content)

    def apply_fixes(self, project_path: str, fixes: Dict[str, str]) -> None:
        """
        Apply code fixes to project files

        Args:
            project_path: Path to project directory
            fixes: Dictionary mapping file paths to new content
        """
        logger.info(f"Applying fixes to {len(fixes)} files")

        project_path = Path(project_path)

        for file_path, new_content in fixes.items():
            full_path = project_path / file_path

            try:
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                logger.info(f"Fixed: {file_path}")
            except Exception as e:
                logger.error(f"Error fixing {file_path}: {e}")

    def create_zip(self, project_path: str) -> str:
        """
        Create a ZIP file of the project

        Args:
            project_path: Path to project directory

        Returns:
            Path to created ZIP file
        """
        project_path = Path(project_path)
        zip_path = project_path.parent / f"{project_path.name}.zip"

        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in project_path.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(project_path.parent)
                    zipf.write(file_path, arcname)

        logger.info(f"Created ZIP: {zip_path}")
        return str(zip_path)

    def get_available_templates(self) -> List[Dict[str, str]]:
        """Get list of available project templates"""
        return [
            {
                'id': 'web_app',
                'name': 'Web Application',
                'description': 'Full-stack web application with frontend and backend',
                'languages': ['python', 'javascript', 'typescript']
            },
            {
                'id': 'game',
                'name': 'Game Project',
                'description': '2D or 3D game with game loop and rendering',
                'languages': ['python', 'javascript', 'cpp', 'rust']
            },
            {
                'id': 'api',
                'name': 'REST API',
                'description': 'RESTful API service with endpoints and database',
                'languages': ['python', 'javascript', 'typescript', 'go', 'rust']
            },
            {
                'id': 'cli_tool',
                'name': 'CLI Tool',
                'description': 'Command-line application',
                'languages': ['python', 'rust', 'go']
            },
            {
                'id': 'ml_project',
                'name': 'Machine Learning',
                'description': 'ML/AI project with data processing and model training',
                'languages': ['python']
            },
            {
                'id': 'desktop_app',
                'name': 'Desktop Application',
                'description': 'GUI desktop application',
                'languages': ['python', 'javascript', 'cpp']
            }
        ]
