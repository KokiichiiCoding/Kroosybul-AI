"""
Virtual Environment Manager for Kroosybul AI
Handles creation, management, and dependency installation in virtual environments.
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import re


class VenvManager:
    """Manages virtual environments and dependency installation"""

    def __init__(self):
        """Initialize the virtual environment manager"""
        self.venv_dir = ".venv"
        self.supported_managers = {
            'python': ['pip', 'poetry', 'pipenv'],
            'javascript': ['npm', 'yarn', 'pnpm'],
            'typescript': ['npm', 'yarn', 'pnpm'],
            'ruby': ['gem', 'bundler'],
            'php': ['composer'],
            'rust': ['cargo'],
            'go': ['go']
        }

    def create_venv(self, project_path: str, language: str) -> Tuple[bool, str]:
        """Create a virtual environment for a project

        Args:
            project_path: Path to the project directory
            language: Programming language

        Returns:
            Tuple of (success, message)
        """
        try:
            if language == 'python':
                return self._create_python_venv(project_path)
            elif language in ['javascript', 'typescript']:
                return self._create_node_venv(project_path)
            elif language == 'ruby':
                return self._create_ruby_venv(project_path)
            else:
                return True, f"No virtual environment needed for {language}"
        except Exception as e:
            return False, f"Error creating virtual environment: {str(e)}"

    def _create_python_venv(self, project_path: str) -> Tuple[bool, str]:
        """Create a Python virtual environment"""
        venv_path = os.path.join(project_path, self.venv_dir)

        # Check if venv already exists
        if os.path.exists(venv_path):
            return True, "Virtual environment already exists"

        # Create venv
        result = subprocess.run(
            [sys.executable, '-m', 'venv', venv_path],
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode == 0:
            return True, f"Python virtual environment created at {venv_path}"
        else:
            return False, f"Failed to create venv: {result.stderr}"

    def _create_node_venv(self, project_path: str) -> Tuple[bool, str]:
        """Initialize Node.js project (npm/yarn)"""
        # Node.js doesn't use traditional virtual environments
        # but we can initialize package.json if it doesn't exist
        package_json = os.path.join(project_path, 'package.json')

        if os.path.exists(package_json):
            return True, "Node.js project already initialized"

        # Create basic package.json
        result = subprocess.run(
            ['npm', 'init', '-y'],
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            return True, "Node.js project initialized"
        else:
            return False, f"Failed to initialize Node.js project: {result.stderr}"

    def _create_ruby_venv(self, project_path: str) -> Tuple[bool, str]:
        """Initialize Ruby project with Bundler"""
        gemfile = os.path.join(project_path, 'Gemfile')

        if os.path.exists(gemfile):
            return True, "Ruby project already initialized"

        return True, "Ruby project ready (use Bundler for dependency management)"

    def install_dependencies(self, project_path: str, language: str,
                            dependencies: Optional[List[str]] = None) -> Tuple[bool, str, List[str]]:
        """Install project dependencies

        Args:
            project_path: Path to the project directory
            language: Programming language
            dependencies: Optional list of dependencies to install

        Returns:
            Tuple of (success, message, installed_packages)
        """
        try:
            if language == 'python':
                return self._install_python_deps(project_path, dependencies)
            elif language in ['javascript', 'typescript']:
                return self._install_node_deps(project_path, dependencies)
            elif language == 'rust':
                return self._install_rust_deps(project_path)
            elif language == 'go':
                return self._install_go_deps(project_path)
            elif language == 'ruby':
                return self._install_ruby_deps(project_path)
            else:
                return True, f"No automatic dependency installation for {language}", []
        except Exception as e:
            return False, f"Error installing dependencies: {str(e)}", []

    def _install_python_deps(self, project_path: str,
                            dependencies: Optional[List[str]] = None) -> Tuple[bool, str, List[str]]:
        """Install Python dependencies"""
        req_file = os.path.join(project_path, 'requirements.txt')
        venv_path = os.path.join(project_path, self.venv_dir)

        # Determine pip executable
        if os.path.exists(venv_path):
            if sys.platform == 'win32':
                pip_exe = os.path.join(venv_path, 'Scripts', 'pip.exe')
            else:
                pip_exe = os.path.join(venv_path, 'bin', 'pip')
        else:
            pip_exe = 'pip'

        installed = []

        # Install from requirements.txt if it exists
        if os.path.exists(req_file):
            result = subprocess.run(
                [pip_exe, 'install', '-r', req_file],
                capture_output=True,
                text=True,
                timeout=300
            )

            if result.returncode == 0:
                installed = self._parse_pip_output(result.stdout)
                return True, f"Installed {len(installed)} packages from requirements.txt", installed
            else:
                return False, f"Failed to install dependencies: {result.stderr}", []

        # Install individual dependencies
        if dependencies:
            result = subprocess.run(
                [pip_exe, 'install'] + dependencies,
                capture_output=True,
                text=True,
                timeout=300
            )

            if result.returncode == 0:
                return True, f"Installed {len(dependencies)} packages", dependencies
            else:
                return False, f"Failed to install dependencies: {result.stderr}", []

        return True, "No dependencies to install", []

    def _install_node_deps(self, project_path: str,
                          dependencies: Optional[List[str]] = None) -> Tuple[bool, str, List[str]]:
        """Install Node.js dependencies"""
        package_json = os.path.join(project_path, 'package.json')

        if not os.path.exists(package_json):
            return False, "No package.json found", []

        # Detect package manager
        if os.path.exists(os.path.join(project_path, 'yarn.lock')):
            cmd = ['yarn', 'install']
        elif os.path.exists(os.path.join(project_path, 'pnpm-lock.yaml')):
            cmd = ['pnpm', 'install']
        else:
            cmd = ['npm', 'install']

        result = subprocess.run(
            cmd,
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=300
        )

        if result.returncode == 0:
            # Parse installed packages from package.json
            with open(package_json, 'r') as f:
                pkg_data = json.load(f)
                deps = list(pkg_data.get('dependencies', {}).keys())
                dev_deps = list(pkg_data.get('devDependencies', {}).keys())
                installed = deps + dev_deps

            return True, f"Installed {len(installed)} packages", installed
        else:
            return False, f"Failed to install dependencies: {result.stderr}", []

    def _install_rust_deps(self, project_path: str) -> Tuple[bool, str, List[str]]:
        """Install Rust dependencies"""
        cargo_toml = os.path.join(project_path, 'Cargo.toml')

        if not os.path.exists(cargo_toml):
            return False, "No Cargo.toml found", []

        result = subprocess.run(
            ['cargo', 'fetch'],
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=300
        )

        if result.returncode == 0:
            return True, "Rust dependencies fetched", []
        else:
            return False, f"Failed to fetch dependencies: {result.stderr}", []

    def _install_go_deps(self, project_path: str) -> Tuple[bool, str, List[str]]:
        """Install Go dependencies"""
        go_mod = os.path.join(project_path, 'go.mod')

        if not os.path.exists(go_mod):
            # Initialize go module
            result = subprocess.run(
                ['go', 'mod', 'init', os.path.basename(project_path)],
                cwd=project_path,
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode != 0:
                return False, f"Failed to initialize go module: {result.stderr}", []

        # Download dependencies
        result = subprocess.run(
            ['go', 'mod', 'download'],
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=300
        )

        if result.returncode == 0:
            return True, "Go dependencies downloaded", []
        else:
            return False, f"Failed to download dependencies: {result.stderr}", []

    def _install_ruby_deps(self, project_path: str) -> Tuple[bool, str, List[str]]:
        """Install Ruby dependencies"""
        gemfile = os.path.join(project_path, 'Gemfile')

        if not os.path.exists(gemfile):
            return False, "No Gemfile found", []

        result = subprocess.run(
            ['bundle', 'install'],
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=300
        )

        if result.returncode == 0:
            return True, "Ruby gems installed", []
        else:
            return False, f"Failed to install gems: {result.stderr}", []

    def _parse_pip_output(self, output: str) -> List[str]:
        """Parse pip install output to get list of installed packages"""
        installed = []
        lines = output.split('\n')

        for line in lines:
            # Look for "Successfully installed" line
            if 'Successfully installed' in line:
                # Extract package names
                parts = line.split('Successfully installed')[1].strip()
                packages = parts.split()
                installed.extend([pkg.split('-')[0] for pkg in packages])

        return installed

    def check_version_conflicts(self, project_path: str, language: str) -> Tuple[bool, List[str]]:
        """Check for dependency version conflicts

        Args:
            project_path: Path to the project directory
            language: Programming language

        Returns:
            Tuple of (has_conflicts, conflict_messages)
        """
        try:
            if language == 'python':
                return self._check_python_conflicts(project_path)
            elif language in ['javascript', 'typescript']:
                return self._check_node_conflicts(project_path)
            else:
                return False, []
        except Exception as e:
            return False, [f"Error checking conflicts: {str(e)}"]

    def _check_python_conflicts(self, project_path: str) -> Tuple[bool, List[str]]:
        """Check for Python dependency conflicts"""
        venv_path = os.path.join(project_path, self.venv_dir)

        if os.path.exists(venv_path):
            if sys.platform == 'win32':
                pip_exe = os.path.join(venv_path, 'Scripts', 'pip.exe')
            else:
                pip_exe = os.path.join(venv_path, 'bin', 'pip')
        else:
            pip_exe = 'pip'

        # Run pip check
        result = subprocess.run(
            [pip_exe, 'check'],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0 and not result.stdout.strip():
            return False, []
        else:
            conflicts = result.stdout.strip().split('\n')
            return True, conflicts

    def _check_node_conflicts(self, project_path: str) -> Tuple[bool, List[str]]:
        """Check for Node.js dependency conflicts"""
        # Detect package manager
        if os.path.exists(os.path.join(project_path, 'yarn.lock')):
            cmd = ['yarn', 'check']
        else:
            cmd = ['npm', 'audit']

        result = subprocess.run(
            cmd,
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=60
        )

        if 'vulnerabilities' in result.stdout.lower() or 'conflicts' in result.stdout.lower():
            return True, [result.stdout]
        else:
            return False, []

    def get_activation_command(self, project_path: str, language: str) -> Optional[str]:
        """Get the command to activate the virtual environment

        Args:
            project_path: Path to the project directory
            language: Programming language

        Returns:
            Activation command string or None
        """
        if language == 'python':
            venv_path = os.path.join(project_path, self.venv_dir)
            if sys.platform == 'win32':
                return f"{venv_path}\\Scripts\\activate.bat"
            else:
                return f"source {venv_path}/bin/activate"
        else:
            return None
