"""
Multi-Model AI Engine for Kroosybul AI
Supports multiple AI backends: Claude, OpenAI GPT, Google Gemini, and local Ollama models.
"""

import os
import json
import requests
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from abc import ABC, abstractmethod


class ModelProvider(ABC):
    """Abstract base class for AI model providers"""

    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> Tuple[str, Dict[str, Any]]:
        """Generate a response from the model

        Args:
            prompt: The input prompt
            **kwargs: Additional provider-specific parameters

        Returns:
            Tuple of (response_text, metadata)
        """
        pass

    @abstractmethod
    def get_cost(self, input_tokens: int, output_tokens: int) -> float:
        """Calculate the cost of the API call

        Args:
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens

        Returns:
            Cost in USD
        """
        pass


class ClaudeProvider(ModelProvider):
    """Anthropic Claude API provider"""

    def __init__(self, api_key: str, model: str = "claude-sonnet-4-5-20250929"):
        """Initialize Claude provider

        Args:
            api_key: Anthropic API key
            model: Model identifier
        """
        try:
            from anthropic import Anthropic
            self.client = Anthropic(api_key=api_key)
            self.model = model
            self.pricing = {
                "claude-sonnet-4-5-20250929": {"input": 0.003, "output": 0.015},
                "claude-3-opus-20240229": {"input": 0.015, "output": 0.075},
                "claude-3-sonnet-20240229": {"input": 0.003, "output": 0.015},
                "claude-3-haiku-20240307": {"input": 0.00025, "output": 0.00125}
            }
        except ImportError:
            raise ImportError("anthropic package not installed. Run: pip install anthropic")

    def generate(self, prompt: str, **kwargs) -> Tuple[str, Dict[str, Any]]:
        """Generate a response using Claude"""
        temperature = kwargs.get('temperature', 0.7)
        max_tokens = kwargs.get('max_tokens', 8000)

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[{"role": "user", "content": prompt}]
            )

            # Extract text from response
            text = response.content[0].text

            # Get token usage
            input_tokens = response.usage.input_tokens
            output_tokens = response.usage.output_tokens

            metadata = {
                'provider': 'claude',
                'model': self.model,
                'input_tokens': input_tokens,
                'output_tokens': output_tokens,
                'cost': self.get_cost(input_tokens, output_tokens)
            }

            return text, metadata
        except Exception as e:
            raise Exception(f"Claude API error: {str(e)}")

    def get_cost(self, input_tokens: int, output_tokens: int) -> float:
        """Calculate cost for Claude API"""
        pricing = self.pricing.get(self.model, self.pricing["claude-sonnet-4-5-20250929"])
        input_cost = (input_tokens / 1_000_000) * pricing["input"]
        output_cost = (output_tokens / 1_000_000) * pricing["output"]
        return input_cost + output_cost


class OpenAIProvider(ModelProvider):
    """OpenAI GPT API provider"""

    def __init__(self, api_key: str, model: str = "gpt-4"):
        """Initialize OpenAI provider

        Args:
            api_key: OpenAI API key
            model: Model identifier
        """
        try:
            import openai
            self.client = openai.OpenAI(api_key=api_key)
            self.model = model
            self.pricing = {
                "gpt-4": {"input": 0.03, "output": 0.06},
                "gpt-4-turbo": {"input": 0.01, "output": 0.03},
                "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015},
                "gpt-4o": {"input": 0.005, "output": 0.015}
            }
        except ImportError:
            raise ImportError("openai package not installed. Run: pip install openai")

    def generate(self, prompt: str, **kwargs) -> Tuple[str, Dict[str, Any]]:
        """Generate a response using OpenAI"""
        temperature = kwargs.get('temperature', 0.7)
        max_tokens = kwargs.get('max_tokens', 8000)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens
            )

            text = response.choices[0].message.content

            # Get token usage
            input_tokens = response.usage.prompt_tokens
            output_tokens = response.usage.completion_tokens

            metadata = {
                'provider': 'openai',
                'model': self.model,
                'input_tokens': input_tokens,
                'output_tokens': output_tokens,
                'cost': self.get_cost(input_tokens, output_tokens)
            }

            return text, metadata
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")

    def get_cost(self, input_tokens: int, output_tokens: int) -> float:
        """Calculate cost for OpenAI API"""
        pricing = self.pricing.get(self.model, self.pricing["gpt-4"])
        input_cost = (input_tokens / 1_000_000) * pricing["input"]
        output_cost = (output_tokens / 1_000_000) * pricing["output"]
        return input_cost + output_cost


class GeminiProvider(ModelProvider):
    """Google Gemini API provider"""

    def __init__(self, api_key: str, model: str = "gemini-pro"):
        """Initialize Gemini provider

        Args:
            api_key: Google API key
            model: Model identifier
        """
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            self.model_name = model
            self.model = genai.GenerativeModel(model)
            self.pricing = {
                "gemini-pro": {"input": 0.000125, "output": 0.000375},
                "gemini-1.5-pro": {"input": 0.00125, "output": 0.00375}
            }
        except ImportError:
            raise ImportError("google-generativeai package not installed. Run: pip install google-generativeai")

    def generate(self, prompt: str, **kwargs) -> Tuple[str, Dict[str, Any]]:
        """Generate a response using Gemini"""
        temperature = kwargs.get('temperature', 0.7)
        max_tokens = kwargs.get('max_tokens', 8000)

        try:
            generation_config = {
                'temperature': temperature,
                'max_output_tokens': max_tokens,
            }

            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )

            text = response.text

            # Estimate token usage (Gemini doesn't always provide exact counts)
            input_tokens = len(prompt.split()) * 1.3  # Rough estimate
            output_tokens = len(text.split()) * 1.3

            metadata = {
                'provider': 'gemini',
                'model': self.model_name,
                'input_tokens': int(input_tokens),
                'output_tokens': int(output_tokens),
                'cost': self.get_cost(int(input_tokens), int(output_tokens))
            }

            return text, metadata
        except Exception as e:
            raise Exception(f"Gemini API error: {str(e)}")

    def get_cost(self, input_tokens: int, output_tokens: int) -> float:
        """Calculate cost for Gemini API"""
        pricing = self.pricing.get(self.model_name, self.pricing["gemini-pro"])
        input_cost = (input_tokens / 1_000_000) * pricing["input"]
        output_cost = (output_tokens / 1_000_000) * pricing["output"]
        return input_cost + output_cost


class OllamaProvider(ModelProvider):
    """Local Ollama model provider"""

    def __init__(self, model: str = "codellama", host: str = "http://localhost:11434"):
        """Initialize Ollama provider

        Args:
            model: Model name (e.g., codellama, mistral, llama2)
            host: Ollama server host
        """
        self.model = model
        self.host = host
        self.api_url = f"{host}/api/generate"

    def generate(self, prompt: str, **kwargs) -> Tuple[str, Dict[str, Any]]:
        """Generate a response using Ollama"""
        temperature = kwargs.get('temperature', 0.7)
        max_tokens = kwargs.get('max_tokens', 8000)

        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "temperature": temperature,
                "stream": False,
                "options": {
                    "num_predict": max_tokens
                }
            }

            response = requests.post(self.api_url, json=payload, timeout=300)
            response.raise_for_status()

            data = response.json()
            text = data.get('response', '')

            # Estimate tokens
            input_tokens = len(prompt.split()) * 1.3
            output_tokens = len(text.split()) * 1.3

            metadata = {
                'provider': 'ollama',
                'model': self.model,
                'input_tokens': int(input_tokens),
                'output_tokens': int(output_tokens),
                'cost': 0.0  # Local models are free
            }

            return text, metadata
        except requests.exceptions.ConnectionError:
            raise Exception(f"Cannot connect to Ollama server at {self.host}. Make sure Ollama is running.")
        except Exception as e:
            raise Exception(f"Ollama error: {str(e)}")

    def get_cost(self, input_tokens: int, output_tokens: int) -> float:
        """Calculate cost for Ollama (always free)"""
        return 0.0


class MultiModelEngine:
    """Multi-model AI engine with cost tracking"""

    def __init__(self):
        """Initialize the multi-model engine"""
        self.providers: Dict[str, ModelProvider] = {}
        self.current_provider: Optional[str] = None
        self.usage_history: List[Dict[str, Any]] = []
        self.total_cost = 0.0

        # Load configuration from environment
        self._load_config()

    def _load_config(self):
        """Load configuration from environment variables"""
        # Claude
        claude_key = os.getenv('ANTHROPIC_API_KEY')
        if claude_key:
            claude_model = os.getenv('CLAUDE_MODEL', 'claude-sonnet-4-5-20250929')
            try:
                self.providers['claude'] = ClaudeProvider(claude_key, claude_model)
                if not self.current_provider:
                    self.current_provider = 'claude'
            except Exception as e:
                print(f"Failed to initialize Claude: {e}")

        # OpenAI
        openai_key = os.getenv('OPENAI_API_KEY')
        if openai_key:
            openai_model = os.getenv('OPENAI_MODEL', 'gpt-4')
            try:
                self.providers['openai'] = OpenAIProvider(openai_key, openai_model)
                if not self.current_provider:
                    self.current_provider = 'openai'
            except Exception as e:
                print(f"Failed to initialize OpenAI: {e}")

        # Gemini
        gemini_key = os.getenv('GOOGLE_API_KEY')
        if gemini_key:
            gemini_model = os.getenv('GEMINI_MODEL', 'gemini-pro')
            try:
                self.providers['gemini'] = GeminiProvider(gemini_key, gemini_model)
                if not self.current_provider:
                    self.current_provider = 'gemini'
            except Exception as e:
                print(f"Failed to initialize Gemini: {e}")

        # Ollama
        if os.getenv('ENABLE_OLLAMA', 'false').lower() == 'true':
            ollama_model = os.getenv('OLLAMA_MODEL', 'codellama')
            ollama_host = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
            try:
                self.providers['ollama'] = OllamaProvider(ollama_model, ollama_host)
                if not self.current_provider:
                    self.current_provider = 'ollama'
            except Exception as e:
                print(f"Failed to initialize Ollama: {e}")

    def add_provider(self, name: str, provider: ModelProvider):
        """Add a custom provider

        Args:
            name: Provider name
            provider: ModelProvider instance
        """
        self.providers[name] = provider
        if not self.current_provider:
            self.current_provider = name

    def set_provider(self, provider_name: str) -> bool:
        """Set the current provider

        Args:
            provider_name: Name of the provider to use

        Returns:
            True if successful, False if provider not found
        """
        if provider_name in self.providers:
            self.current_provider = provider_name
            return True
        return False

    def generate(self, prompt: str, **kwargs) -> Tuple[str, Dict[str, Any]]:
        """Generate a response using the current provider

        Args:
            prompt: Input prompt
            **kwargs: Provider-specific parameters

        Returns:
            Tuple of (response_text, metadata)
        """
        if not self.current_provider:
            raise Exception("No AI provider configured. Please set up API keys in .env file.")

        provider = self.providers[self.current_provider]

        # Generate response
        text, metadata = provider.generate(prompt, **kwargs)

        # Track usage
        usage_record = {
            'timestamp': datetime.now().isoformat(),
            'provider': metadata['provider'],
            'model': metadata['model'],
            'input_tokens': metadata['input_tokens'],
            'output_tokens': metadata['output_tokens'],
            'cost': metadata['cost']
        }

        self.usage_history.append(usage_record)
        self.total_cost += metadata['cost']

        return text, metadata

    def get_available_providers(self) -> List[str]:
        """Get list of available providers

        Returns:
            List of provider names
        """
        return list(self.providers.keys())

    def get_usage_stats(self) -> Dict[str, Any]:
        """Get usage statistics

        Returns:
            Dictionary with usage statistics
        """
        total_input_tokens = sum(r['input_tokens'] for r in self.usage_history)
        total_output_tokens = sum(r['output_tokens'] for r in self.usage_history)

        # Group by provider
        by_provider = {}
        for record in self.usage_history:
            provider = record['provider']
            if provider not in by_provider:
                by_provider[provider] = {
                    'calls': 0,
                    'input_tokens': 0,
                    'output_tokens': 0,
                    'cost': 0.0
                }

            by_provider[provider]['calls'] += 1
            by_provider[provider]['input_tokens'] += record['input_tokens']
            by_provider[provider]['output_tokens'] += record['output_tokens']
            by_provider[provider]['cost'] += record['cost']

        return {
            'total_calls': len(self.usage_history),
            'total_input_tokens': total_input_tokens,
            'total_output_tokens': total_output_tokens,
            'total_cost': self.total_cost,
            'by_provider': by_provider,
            'current_provider': self.current_provider
        }

    def save_usage_history(self, filepath: str = 'usage_history.json'):
        """Save usage history to a file

        Args:
            filepath: Path to save the history
        """
        with open(filepath, 'w') as f:
            json.dump({
                'usage_history': self.usage_history,
                'total_cost': self.total_cost
            }, f, indent=2)

    def load_usage_history(self, filepath: str = 'usage_history.json'):
        """Load usage history from a file

        Args:
            filepath: Path to load the history from
        """
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                self.usage_history = data.get('usage_history', [])
                self.total_cost = data.get('total_cost', 0.0)
        except FileNotFoundError:
            pass  # File doesn't exist yet
