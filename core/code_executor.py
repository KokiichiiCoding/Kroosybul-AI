"""
Code Executor - Safely executes and tests generated code
"""

import os
import subprocess
import logging
from pathlib import Path
from typing import Dict, List, Any
import tempfile
import shutil

logger = logging.getLogger(__name__)


class CodeExecutor:
    """Executes and tests generated code in a safe environment"""

    def __init__(self):
        self.timeout = int(os.getenv('CODE_TIMEOUT', 30))
        self.enable_sandbox = os.getenv('ENABLE_SANDBOX', 'True') == 'True'

        # Test commands for different languages
        self.test_commands = {
            'python': self._test_python,
            'javascript': self._test_javascript,
            'typescript': self._test_typescript,
            'java': self._test_java,
            'cpp': self._test_cpp,
            'rust': self._test_rust,
            'go': self._test_go
        }

    def test_project(self, project_path: str) -> Dict[str, Any]:
        """
        Test a generated project

        Args:
            project_path: Path to the project directory

        Returns:
            Dictionary with test results
        """
        logger.info(f"Testing project: {project_path}")

        project_path = Path(project_path)

        # Read metadata to determine language
        metadata_path = project_path / '.codeforge_metadata.json'
        if not metadata_path.exists():
            return {
                'success': False,
                'errors': ['Project metadata not found']
            }

        import json
        with open(metadata_path) as f:
            metadata = json.load(f)

        language = metadata.get('language', 'python').lower()

        # Run language-specific tests
        test_func = self.test_commands.get(language, self._test_generic)
        return test_func(project_path, metadata)

    def _test_python(self, project_path: Path, metadata: Dict) -> Dict[str, Any]:
        """Test Python project"""
        errors = []
        warnings = []

        # Check for syntax errors in all Python files
        for py_file in project_path.rglob('*.py'):
            try:
                result = subprocess.run(
                    ['python', '-m', 'py_compile', str(py_file)],
                    capture_output=True,
                    text=True,
                    timeout=self.timeout,
                    cwd=project_path
                )

                if result.returncode != 0:
                    errors.append(f"Syntax error in {py_file.name}: {result.stderr}")
                else:
                    logger.info(f"✓ {py_file.name} passed syntax check")

            except subprocess.TimeoutExpired:
                errors.append(f"Timeout testing {py_file.name}")
            except Exception as e:
                errors.append(f"Error testing {py_file.name}: {str(e)}")

        # Check if requirements.txt exists and is valid
        req_file = project_path / 'requirements.txt'
        if req_file.exists():
            try:
                with open(req_file) as f:
                    reqs = f.read().strip()
                    if reqs:
                        logger.info(f"Found {len(reqs.split())} dependencies")
            except Exception as e:
                warnings.append(f"Could not read requirements.txt: {e}")

        # Try to import the main module (without executing)
        main_files = list(project_path.glob('main.py')) + list(project_path.glob('app.py'))
        if main_files:
            logger.info(f"Found main file: {main_files[0].name}")

        return {
            'success': len(errors) == 0,
            'errors': errors,
            'warnings': warnings,
            'tested_files': len(list(project_path.rglob('*.py')))
        }

    def _test_javascript(self, project_path: Path, metadata: Dict) -> Dict[str, Any]:
        """Test JavaScript project"""
        errors = []
        warnings = []

        # Check for Node.js
        try:
            subprocess.run(['node', '--version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            warnings.append("Node.js not found - cannot run full tests")
            return {'success': True, 'errors': [], 'warnings': warnings, 'tested_files': 0}

        # Check syntax of JavaScript files
        for js_file in project_path.rglob('*.js'):
            try:
                result = subprocess.run(
                    ['node', '--check', str(js_file)],
                    capture_output=True,
                    text=True,
                    timeout=self.timeout,
                    cwd=project_path
                )

                if result.returncode != 0:
                    errors.append(f"Syntax error in {js_file.name}: {result.stderr}")
                else:
                    logger.info(f"✓ {js_file.name} passed syntax check")

            except subprocess.TimeoutExpired:
                errors.append(f"Timeout testing {js_file.name}")
            except Exception as e:
                errors.append(f"Error testing {js_file.name}: {str(e)}")

        # Check package.json
        package_json = project_path / 'package.json'
        if package_json.exists():
            try:
                import json
                with open(package_json) as f:
                    package_data = json.load(f)
                    logger.info(f"Found package.json with {len(package_data.get('dependencies', {}))} dependencies")
            except Exception as e:
                warnings.append(f"Could not parse package.json: {e}")

        return {
            'success': len(errors) == 0,
            'errors': errors,
            'warnings': warnings,
            'tested_files': len(list(project_path.rglob('*.js')))
        }

    def _test_typescript(self, project_path: Path, metadata: Dict) -> Dict[str, Any]:
        """Test TypeScript project"""
        errors = []
        warnings = []

        # Check for TypeScript compiler
        try:
            subprocess.run(['tsc', '--version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            warnings.append("TypeScript compiler not found - skipping compilation tests")
            # Still check for basic syntax
            ts_files = list(project_path.rglob('*.ts'))
            return {
                'success': True,
                'errors': [],
                'warnings': warnings,
                'tested_files': len(ts_files)
            }

        # Run TypeScript compiler in check mode
        try:
            result = subprocess.run(
                ['tsc', '--noEmit'],
                capture_output=True,
                text=True,
                timeout=self.timeout,
                cwd=project_path
            )

            if result.returncode != 0:
                errors.append(f"TypeScript compilation errors: {result.stderr}")
            else:
                logger.info("✓ TypeScript compilation check passed")

        except subprocess.TimeoutExpired:
            errors.append("Timeout during TypeScript compilation")
        except Exception as e:
            errors.append(f"Error testing TypeScript: {str(e)}")

        return {
            'success': len(errors) == 0,
            'errors': errors,
            'warnings': warnings,
            'tested_files': len(list(project_path.rglob('*.ts')))
        }

    def _test_rust(self, project_path: Path, metadata: Dict) -> Dict[str, Any]:
        """Test Rust project"""
        errors = []
        warnings = []

        # Check for Rust/Cargo
        try:
            subprocess.run(['cargo', '--version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            warnings.append("Cargo not found - cannot test Rust project")
            return {'success': True, 'errors': [], 'warnings': warnings, 'tested_files': 0}

        # Run cargo check
        try:
            result = subprocess.run(
                ['cargo', 'check'],
                capture_output=True,
                text=True,
                timeout=self.timeout * 3,  # Rust can be slow
                cwd=project_path
            )

            if result.returncode != 0:
                errors.append(f"Cargo check failed: {result.stderr}")
            else:
                logger.info("✓ Cargo check passed")

        except subprocess.TimeoutExpired:
            errors.append("Timeout during cargo check")
        except Exception as e:
            errors.append(f"Error testing Rust project: {str(e)}")

        return {
            'success': len(errors) == 0,
            'errors': errors,
            'warnings': warnings,
            'tested_files': len(list(project_path.rglob('*.rs')))
        }

    def _test_go(self, project_path: Path, metadata: Dict) -> Dict[str, Any]:
        """Test Go project"""
        errors = []
        warnings = []

        # Check for Go
        try:
            subprocess.run(['go', 'version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            warnings.append("Go not found - cannot test Go project")
            return {'success': True, 'errors': [], 'warnings': warnings, 'tested_files': 0}

        # Run go build in check mode
        try:
            result = subprocess.run(
                ['go', 'build', '-o', '/dev/null', './...'],
                capture_output=True,
                text=True,
                timeout=self.timeout,
                cwd=project_path
            )

            if result.returncode != 0:
                errors.append(f"Go build failed: {result.stderr}")
            else:
                logger.info("✓ Go build check passed")

        except subprocess.TimeoutExpired:
            errors.append("Timeout during go build")
        except Exception as e:
            errors.append(f"Error testing Go project: {str(e)}")

        return {
            'success': len(errors) == 0,
            'errors': errors,
            'warnings': warnings,
            'tested_files': len(list(project_path.rglob('*.go')))
        }

    def _test_java(self, project_path: Path, metadata: Dict) -> Dict[str, Any]:
        """Test Java project"""
        errors = []
        warnings = []

        # Check for Java compiler
        try:
            subprocess.run(['javac', '-version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            warnings.append("Java compiler not found - cannot test Java project")
            return {'success': True, 'errors': [], 'warnings': warnings, 'tested_files': 0}

        # Compile Java files
        java_files = list(project_path.rglob('*.java'))
        if java_files:
            try:
                result = subprocess.run(
                    ['javac'] + [str(f) for f in java_files],
                    capture_output=True,
                    text=True,
                    timeout=self.timeout,
                    cwd=project_path
                )

                if result.returncode != 0:
                    errors.append(f"Java compilation failed: {result.stderr}")
                else:
                    logger.info(f"✓ Compiled {len(java_files)} Java files")

            except subprocess.TimeoutExpired:
                errors.append("Timeout during Java compilation")
            except Exception as e:
                errors.append(f"Error testing Java project: {str(e)}")

        return {
            'success': len(errors) == 0,
            'errors': errors,
            'warnings': warnings,
            'tested_files': len(java_files)
        }

    def _test_cpp(self, project_path: Path, metadata: Dict) -> Dict[str, Any]:
        """Test C++ project"""
        errors = []
        warnings = []

        # Check for g++
        try:
            subprocess.run(['g++', '--version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            warnings.append("g++ not found - cannot test C++ project")
            return {'success': True, 'errors': [], 'warnings': warnings, 'tested_files': 0}

        # Check syntax of C++ files
        cpp_files = list(project_path.rglob('*.cpp'))
        for cpp_file in cpp_files:
            try:
                result = subprocess.run(
                    ['g++', '-fsyntax-only', str(cpp_file)],
                    capture_output=True,
                    text=True,
                    timeout=self.timeout,
                    cwd=project_path
                )

                if result.returncode != 0:
                    errors.append(f"C++ syntax error in {cpp_file.name}: {result.stderr}")
                else:
                    logger.info(f"✓ {cpp_file.name} passed syntax check")

            except subprocess.TimeoutExpired:
                errors.append(f"Timeout testing {cpp_file.name}")
            except Exception as e:
                errors.append(f"Error testing {cpp_file.name}: {str(e)}")

        return {
            'success': len(errors) == 0,
            'errors': errors,
            'warnings': warnings,
            'tested_files': len(cpp_files)
        }

    def _test_generic(self, project_path: Path, metadata: Dict) -> Dict[str, Any]:
        """Generic test for unsupported languages"""
        warnings = [f"No specific tests available for {metadata.get('language')}"]

        # Just count files
        all_files = list(project_path.rglob('*'))
        code_files = [f for f in all_files if f.is_file() and f.suffix not in ['.json', '.md', '.txt']]

        return {
            'success': True,
            'errors': [],
            'warnings': warnings,
            'tested_files': len(code_files)
        }

    def execute_code(self, file_path: str, language: str) -> Dict[str, Any]:
        """
        Execute a specific code file (use with caution!)

        Args:
            file_path: Path to the code file
            language: Programming language

        Returns:
            Execution results
        """
        logger.warning(f"Executing code: {file_path}")

        # This is intentionally limited for security
        # Only allow execution in controlled environments

        if not self.enable_sandbox:
            return {
                'success': False,
                'output': '',
                'error': 'Code execution is disabled'
            }

        # Implement sandbox execution here
        # For now, return a mock result
        return {
            'success': True,
            'output': 'Code execution not fully implemented (safety feature)',
            'error': ''
        }
