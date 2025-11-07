"""
Enhanced Features - Advanced AI capabilities for Kroosybul AI
"""

import os
import re
import json
import logging
from typing import Dict, List, Any, Optional

try:
    from anthropic import Anthropic
except ImportError:
    Anthropic = None

logger = logging.getLogger(__name__)


class EnhancedAIFeatures:
    """Advanced AI features for project generation and analysis"""

    def __init__(self, ai_engine):
        self.ai_engine = ai_engine
        self.client = ai_engine.client
        self.model = ai_engine.model

    def generate_architecture_diagram(self, project_plan: Dict[str, Any]) -> str:
        """
        Generate a Mermaid.js architecture diagram for the project

        Args:
            project_plan: Project plan dictionary

        Returns:
            Mermaid.js diagram code
        """
        logger.info("Generating architecture diagram...")

        prompt = f"""Create a comprehensive Mermaid.js architecture diagram for this project:

Project: {project_plan['project_name']}
Language: {project_plan['language']}
Type: {project_plan['project_type']}
Description: {project_plan['description']}
Features: {', '.join(project_plan.get('features', []))}
Frameworks: {', '.join(project_plan.get('frameworks', []))}

Create a clear, hierarchical diagram showing:
1. Main components/modules
2. Data flow between components
3. External dependencies
4. Database/storage layers (if applicable)
5. API endpoints (if applicable)

Use Mermaid.js graph syntax. Respond with ONLY the Mermaid code starting with ```mermaid"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                temperature=0.5,
                messages=[{"role": "user", "content": prompt}]
            )

            diagram = response.content[0].text.strip()

            # Extract mermaid code
            if '```mermaid' in diagram:
                diagram = diagram.split('```mermaid')[1].split('```')[0].strip()
            elif '```' in diagram:
                diagram = diagram.split('```')[1].split('```')[0].strip()

            logger.info("Architecture diagram generated successfully")
            return diagram

        except Exception as e:
            logger.error(f"Error generating architecture diagram: {e}")
            return self._get_default_diagram(project_plan)

    def _get_default_diagram(self, project_plan: Dict) -> str:
        """Generate a simple default diagram"""
        return f"""graph TD
    A[{project_plan['project_name']}] --> B[Main Module]
    B --> C[Core Logic]
    B --> D[Configuration]
    C --> E[Output]"""

    def explain_error_naturally(self, error: str, project_context: Dict) -> str:
        """
        Provide natural-language explanation of an error

        Args:
            error: Error message
            project_context: Project information

        Returns:
            Human-friendly explanation with fix suggestions
        """
        logger.info("Generating natural language error explanation...")

        prompt = f"""Explain this error in simple, clear language and suggest how to fix it:

Error: {error}

Project Context:
- Language: {project_context.get('language')}
- Type: {project_context.get('project_type')}

Provide:
1. What the error means in plain English
2. Why it likely occurred
3. Step-by-step fix instructions
4. How to prevent it in the future

Keep it concise (3-5 sentences) and actionable."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                temperature=0.7,
                messages=[{"role": "user", "content": prompt}]
            )

            explanation = response.content[0].text.strip()
            logger.info("Error explanation generated")
            return explanation

        except Exception as e:
            logger.error(f"Error generating explanation: {e}")
            return f"Error occurred: {error}"

    def analyze_dependencies(self, file_content: str, language: str) -> List[str]:
        """
        Intelligently parse and extract dependencies from code

        Args:
            file_content: Source code content
            language: Programming language

        Returns:
            List of detected dependencies
        """
        logger.info(f"Analyzing dependencies for {language}...")

        dependencies = []

        if language == 'python':
            # Extract imports
            import_patterns = [
                r'^import\s+(\w+)',
                r'^from\s+(\w+)\s+import',
            ]
            for pattern in import_patterns:
                matches = re.findall(pattern, file_content, re.MULTILINE)
                dependencies.extend(matches)

        elif language in ['javascript', 'typescript']:
            # Extract requires and imports
            patterns = [
                r'require\([\'"]([^\'"\)]+)[\'"]\)',
                r'from\s+[\'"]([^\'"\)]+)[\'"]',
                r'import\s+[\'"]([^\'"\)]+)[\'"]',
            ]
            for pattern in patterns:
                matches = re.findall(pattern, file_content)
                dependencies.extend(matches)

        # Remove standard library imports
        dependencies = [d for d in dependencies if not d.startswith('.')]

        # Remove duplicates
        dependencies = list(set(dependencies))

        logger.info(f"Found {len(dependencies)} dependencies")
        return dependencies

    def generate_test_summary(self, test_results: Dict[str, Any]) -> str:
        """
        Generate AI-powered summary of test results

        Args:
            test_results: Test execution results

        Returns:
            Human-readable summary
        """
        logger.info("Generating test summary...")

        errors = test_results.get('errors', [])
        warnings = test_results.get('warnings', [])
        tested_files = test_results.get('tested_files', 0)
        success = test_results.get('success', False)

        prompt = f"""Summarize these test results in a clear, concise way:

Success: {success}
Files Tested: {tested_files}
Errors: {len(errors)}
Warnings: {len(warnings)}

Error Details:
{chr(10).join(errors[:5])}

Warning Details:
{chr(10).join(warnings[:5])}

Provide:
1. Overall status (1 sentence)
2. Key issues found (bullet points)
3. Recommended next steps (2-3 items)

Keep it professional but friendly."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=800,
                temperature=0.7,
                messages=[{"role": "user", "content": prompt}]
            )

            summary = response.content[0].text.strip()
            logger.info("Test summary generated")
            return summary

        except Exception as e:
            logger.error(f"Error generating test summary: {e}")
            status = "✅ All tests passed!" if success else "⚠️ Tests completed with issues"
            return f"{status}\n\nTested {tested_files} files. Found {len(errors)} errors and {len(warnings)} warnings."

    def generate_documentation(self, code: str, language: str) -> str:
        """
        Generate comprehensive comments and docstrings for code

        Args:
            code: Source code
            language: Programming language

        Returns:
            Documented code
        """
        logger.info("Generating documentation...")

        prompt = f"""Add comprehensive documentation to this {language} code:

{code}

Add:
1. Module/file-level docstring
2. Function/method docstrings
3. Inline comments for complex logic
4. Type hints (if applicable)

Follow {language} documentation best practices. Return ONLY the documented code."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                temperature=0.5,
                messages=[{"role": "user", "content": prompt}]
            )

            documented_code = response.content[0].text.strip()

            # Remove markdown code blocks if present
            if '```' in documented_code:
                lines = documented_code.split('\n')
                if lines[0].startswith('```'):
                    lines = lines[1:]
                if lines[-1].strip() == '```':
                    lines = lines[:-1]
                documented_code = '\n'.join(lines)

            logger.info("Documentation generated")
            return documented_code

        except Exception as e:
            logger.error(f"Error generating documentation: {e}")
            return code

    def estimate_complexity(self, code: str, language: str) -> Dict[str, Any]:
        """
        Estimate algorithmic complexity and performance metrics

        Args:
            code: Source code
            language: Programming language

        Returns:
            Dictionary with complexity analysis
        """
        logger.info("Estimating code complexity...")

        prompt = f"""Analyze the algorithmic complexity of this {language} code:

{code[:2000]}  # Limit code length

Provide a JSON response with:
{{
    "time_complexity": "O(n) notation",
    "space_complexity": "O(n) notation",
    "performance_rating": "excellent/good/fair/poor",
    "bottlenecks": ["list of potential performance issues"],
    "optimizations": ["list of suggested improvements"],
    "estimated_runtime": "description for typical input"
}}

Respond with ONLY the JSON object."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                temperature=0.5,
                messages=[{"role": "user", "content": prompt}]
            )

            response_text = response.content[0].text.strip()

            # Extract JSON
            if '```json' in response_text:
                response_text = response_text.split('```json')[1].split('```')[0].strip()
            elif '```' in response_text:
                response_text = response_text.split('```')[1].split('```')[0].strip()

            complexity = json.loads(response_text)
            logger.info("Complexity analysis complete")
            return complexity

        except Exception as e:
            logger.error(f"Error estimating complexity: {e}")
            return {
                "time_complexity": "Unknown",
                "space_complexity": "Unknown",
                "performance_rating": "not analyzed",
                "bottlenecks": [],
                "optimizations": [],
                "estimated_runtime": "Analysis unavailable"
            }

    def enhance_with_context(self, user_message: str, uploaded_files: List[Dict]) -> str:
        """
        Enhance user prompt with uploaded file context

        Args:
            user_message: Original user message
            uploaded_files: List of uploaded file data

        Returns:
            Enhanced prompt with file context
        """
        logger.info(f"Enhancing prompt with {len(uploaded_files)} uploaded files...")

        if not uploaded_files:
            return user_message

        context_parts = [user_message, "\n\n## Uploaded Files Context:\n"]

        for file_data in uploaded_files:
            filename = file_data.get('filename', 'unknown')
            content = file_data.get('content', '')

            context_parts.append(f"\n### File: {filename}")
            context_parts.append(f"```\n{content[:2000]}\n```")  # Limit content length

        enhanced_prompt = '\n'.join(context_parts)
        enhanced_prompt += "\n\nPlease build upon or extend this existing code."

        return enhanced_prompt


class MultiModelSupport:
    """Support for multiple AI models (Claude, GPT, Gemini)"""

    def __init__(self):
        self.anthropic_key = os.getenv('ANTHROPIC_API_KEY')
        self.openai_key = os.getenv('OPENAI_API_KEY')
        self.google_key = os.getenv('GOOGLE_API_KEY')

        self.available_models = []

        if self.anthropic_key:
            self.available_models.append({
                'provider': 'anthropic',
                'name': 'Claude Sonnet 4.5',
                'model_id': 'claude-sonnet-4-5-20250929',
                'max_tokens': 8000
            })

        if self.openai_key:
            self.available_models.extend([
                {
                    'provider': 'openai',
                    'name': 'GPT-4',
                    'model_id': 'gpt-4',
                    'max_tokens': 8000
                },
                {
                    'provider': 'openai',
                    'name': 'GPT-4 Turbo',
                    'model_id': 'gpt-4-turbo-preview',
                    'max_tokens': 4000
                }
            ])

        if self.google_key:
            self.available_models.append({
                'provider': 'google',
                'name': 'Gemini Pro',
                'model_id': 'gemini-pro',
                'max_tokens': 8000
            })

    def get_available_models(self) -> List[Dict[str, Any]]:
        """Return list of available AI models"""
        return self.available_models

    def create_client(self, provider: str):
        """Create appropriate client for the provider"""
        if provider == 'anthropic' and self.anthropic_key:
            if Anthropic:
                return Anthropic(api_key=self.anthropic_key)
            else:
                logger.warning("Anthropic package not installed")
                return None
        elif provider == 'openai' and self.openai_key:
            try:
                import openai
                return openai.OpenAI(api_key=self.openai_key)
            except ImportError:
                logger.warning("OpenAI package not installed")
                return None
        elif provider == 'google' and self.google_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.google_key)
                return genai
            except ImportError:
                logger.warning("Google AI package not installed")
                return None
        return None


class ReusableComponentLibrary:
    """Store and retrieve reusable code components"""

    def __init__(self, storage_path: str = "component_library"):
        self.storage_path = storage_path
        os.makedirs(storage_path, exist_ok=True)

    def save_component(self, name: str, code: str, language: str, description: str, tags: List[str] = None):
        """Save a reusable component"""
        component_data = {
            'name': name,
            'code': code,
            'language': language,
            'description': description,
            'tags': tags or [],
            'created_at': __import__('datetime').datetime.utcnow().isoformat()
        }

        filename = f"{name.lower().replace(' ', '_')}_{language}.json"
        filepath = os.path.join(self.storage_path, filename)

        with open(filepath, 'w') as f:
            json.dump(component_data, f, indent=2)

        logger.info(f"Saved component: {name}")

    def search_components(self, query: str = None, language: str = None, tags: List[str] = None) -> List[Dict]:
        """Search for components"""
        results = []

        for filename in os.listdir(self.storage_path):
            if filename.endswith('.json'):
                filepath = os.path.join(self.storage_path, filename)

                try:
                    with open(filepath, 'r') as f:
                        component = json.load(f)

                    # Filter by language
                    if language and component.get('language') != language:
                        continue

                    # Filter by tags
                    if tags and not any(tag in component.get('tags', []) for tag in tags):
                        continue

                    # Filter by query in name or description
                    if query:
                        query_lower = query.lower()
                        if query_lower not in component.get('name', '').lower() and \
                           query_lower not in component.get('description', '').lower():
                            continue

                    results.append(component)

                except Exception as e:
                    logger.error(f"Error reading component {filename}: {e}")

        return results

    def get_component(self, name: str, language: str) -> Optional[Dict]:
        """Get a specific component"""
        filename = f"{name.lower().replace(' ', '_')}_{language}.json"
        filepath = os.path.join(self.storage_path, filename)

        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return json.load(f)
        return None
