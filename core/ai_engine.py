"""
AI Engine - Handles AI interactions and code generation orchestration
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional
from anthropic import Anthropic

logger = logging.getLogger(__name__)


class AIEngine:
    """Orchestrates AI-powered code generation using Claude"""

    def __init__(self):
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")

        self.client = Anthropic(api_key=api_key)
        self.model = os.getenv('AI_MODEL', 'claude-sonnet-4-5-20250929')
        self.temperature = float(os.getenv('AI_TEMPERATURE', '0.7'))
        self.max_tokens = int(os.getenv('MAX_TOKENS', '8000'))

        # Initialize enhanced features (will be done lazily to avoid circular import)
        self.enhanced_features = None

    def analyze_project_request(self, user_message: str, conversation_history: List[Dict]) -> Dict[str, Any]:
        """
        Analyze the user's project request and create a detailed project plan

        Args:
            user_message: The user's project description
            conversation_history: Previous conversation messages

        Returns:
            Dictionary containing project plan details
        """
        logger.info("Analyzing project request...")

        prompt = f"""You are CodeForge AI, an expert software architect and developer.
A user wants to create a project. Analyze their request and create a detailed project plan.

User Request: {user_message}

Please provide a structured project plan in JSON format with the following fields:
{{
    "project_name": "suggested project name (lowercase, hyphens)",
    "description": "Brief description of the project",
    "language": "primary programming language (python, javascript, typescript, java, cpp, rust, go, etc.)",
    "project_type": "type (web_app, game, cli_tool, api, desktop_app, mobile_app, ml_project, etc.)",
    "frameworks": ["list of frameworks/libraries to use"],
    "features": ["key features to implement"],
    "files": [
        {{
            "path": "relative/path/to/file",
            "purpose": "what this file does",
            "priority": "high/medium/low"
        }}
    ],
    "dependencies": ["list of dependencies/packages"],
    "setup_instructions": "how to set up and run the project",
    "estimated_complexity": "simple/moderate/complex"
}}

Consider:
- What language and framework best suits this project
- What files and structure are needed
- What dependencies are required
- How to make it production-ready

Respond with ONLY the JSON object, no additional text."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            response_text = response.content[0].text.strip()

            # Extract JSON from response
            if '```json' in response_text:
                response_text = response_text.split('```json')[1].split('```')[0].strip()
            elif '```' in response_text:
                response_text = response_text.split('```')[1].split('```')[0].strip()

            project_plan = json.loads(response_text)
            logger.info(f"Project plan created: {project_plan['project_name']}")

            return project_plan

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse AI response as JSON: {e}")
            # Return a default plan
            return self._create_default_plan(user_message)
        except Exception as e:
            logger.error(f"Error in analyze_project_request: {e}", exc_info=True)
            raise

    def generate_file_content(self, file_info: Dict, project_context: Dict) -> str:
        """
        Generate content for a specific file

        Args:
            file_info: Information about the file to generate
            project_context: Overall project context

        Returns:
            Generated file content as string
        """
        logger.info(f"Generating content for: {file_info['path']}")

        prompt = f"""Generate complete, production-ready code for this file.

Project Context:
- Name: {project_context['project_name']}
- Language: {project_context['language']}
- Type: {project_context['project_type']}
- Description: {project_context['description']}
- Frameworks: {', '.join(project_context.get('frameworks', []))}
- Features: {', '.join(project_context.get('features', []))}

File to Generate:
- Path: {file_info['path']}
- Purpose: {file_info['purpose']}
- Priority: {file_info.get('priority', 'medium')}

Requirements:
1. Write complete, working code (no placeholders or TODOs)
2. Include proper error handling
3. Add comprehensive comments
4. Follow best practices for {project_context['language']}
5. Make it production-ready
6. Include imports/dependencies
7. Ensure code is secure and efficient

Generate ONLY the file content, no explanations or markdown formatting."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            content = response.content[0].text.strip()

            # Remove markdown code blocks if present
            if content.startswith('```'):
                lines = content.split('\n')
                lines = lines[1:-1] if lines[-1].strip() == '```' else lines[1:]
                content = '\n'.join(lines)

            return content

        except Exception as e:
            logger.error(f"Error generating file content: {e}", exc_info=True)
            return f"# Error generating content for {file_info['path']}\n# {str(e)}"

    def fix_code_issues(self, project_info: Dict, errors: List[str], conversation_history: List[Dict]) -> Dict[str, str]:
        """
        Generate fixes for code issues

        Args:
            project_info: Information about the project
            errors: List of error messages
            conversation_history: Previous messages

        Returns:
            Dictionary mapping file paths to fixed content
        """
        logger.info(f"Generating fixes for {len(errors)} errors")

        error_summary = '\n'.join(f"- {error}" for error in errors[:10])

        prompt = f"""A project has errors that need to be fixed.

Project: {project_info['name']}
Language: {project_info['language']}

Errors:
{error_summary}

Please provide fixes in JSON format:
{{
    "file_path": "updated file content",
    ...
}}

Provide complete file content for each file that needs changes. Focus on fixing the errors while maintaining functionality."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            response_text = response.content[0].text.strip()

            # Extract JSON
            if '```json' in response_text:
                response_text = response_text.split('```json')[1].split('```')[0].strip()
            elif '```' in response_text:
                response_text = response_text.split('```')[1].split('```')[0].strip()

            fixes = json.loads(response_text)
            return fixes

        except Exception as e:
            logger.error(f"Error generating fixes: {e}", exc_info=True)
            return {}

    def _create_default_plan(self, user_message: str) -> Dict[str, Any]:
        """Create a default project plan if AI parsing fails"""
        return {
            "project_name": "my-project",
            "description": user_message,
            "language": "python",
            "project_type": "cli_tool",
            "frameworks": [],
            "features": ["Basic functionality"],
            "files": [
                {"path": "main.py", "purpose": "Main application file", "priority": "high"},
                {"path": "README.md", "purpose": "Documentation", "priority": "high"}
            ],
            "dependencies": [],
            "setup_instructions": "Run with: python main.py",
            "estimated_complexity": "simple"
        }

    def enhance_project_idea(self, basic_idea: str) -> str:
        """
        Take a basic project idea and enhance it with suggestions

        Args:
            basic_idea: User's basic project description

        Returns:
            Enhanced description with suggestions
        """
        prompt = f"""A user has a project idea: "{basic_idea}"

Enhance this idea by suggesting:
1. Additional features that would make it better
2. Modern best practices to apply
3. Technologies that work well for this type of project
4. Edge cases to handle
5. User experience improvements

Keep it concise (3-5 sentences) and practical."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                temperature=0.8,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            return response.content[0].text.strip()

        except Exception as e:
            logger.error(f"Error enhancing project idea: {e}")
            return basic_idea

    def get_enhanced_features(self):
        """Lazy initialization of enhanced features"""
        if self.enhanced_features is None:
            from .enhanced_features import EnhancedAIFeatures
            self.enhanced_features = EnhancedAIFeatures(self)
        return self.enhanced_features

    def generate_architecture_diagram(self, project_plan: Dict[str, Any]) -> str:
        """Generate Mermaid.js architecture diagram"""
        return self.get_enhanced_features().generate_architecture_diagram(project_plan)

    def explain_error_naturally(self, error: str, project_context: Dict) -> str:
        """Provide natural-language error explanation"""
        return self.get_enhanced_features().explain_error_naturally(error, project_context)

    def generate_test_summary(self, test_results: Dict[str, Any]) -> str:
        """Generate AI-powered test summary"""
        return self.get_enhanced_features().generate_test_summary(test_results)

    def generate_documentation(self, code: str, language: str) -> str:
        """Generate documentation for code"""
        return self.get_enhanced_features().generate_documentation(code, language)

    def estimate_complexity(self, code: str, language: str) -> Dict[str, Any]:
        """Estimate algorithmic complexity"""
        return self.get_enhanced_features().estimate_complexity(code, language)
