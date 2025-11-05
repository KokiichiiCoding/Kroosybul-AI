# Kroosybul AI 🔥

An intelligent code generation studio that transforms your ideas into complete, runnable projects across multiple programming languages.

## Features

### Core Features
- **Multi-Language Support**: Generate projects in Python, JavaScript, TypeScript, Java, C++, Rust, Go, and more
- **Project Templates**: Pre-built templates for games, web apps, APIs, CLI tools, and AI applications
- **Iterative Refinement**: Continuously improves code until it works perfectly
- **Real-time Chat Interface**: Natural conversation to describe your project
- **Automatic Testing**: Built-in code execution and validation
- **Smart Dependencies**: Automatic dependency detection and management
- **Progress Tracking**: Visual feedback on generation progress
- **Export Projects**: Download complete, ready-to-run projects

### 🆕 Advanced Features

- **Context Persistence**: Save and resume project sessions anytime - never lose your work!
- **Multi-Model Support**: Switch between Claude, GPT-4, Gemini, or local Ollama models
- **Cost Tracking**: Monitor API usage and costs across all AI providers
- **Git Integration**: Auto-initialize repos, commit iterations, rollback to any version
- **Smart Venv Management**: Automatic virtual environment creation and dependency installation
- **Template Library**: Battle-tested templates, custom templates, import/export capability
- **Version Conflict Resolution**: Automatic detection and resolution of dependency conflicts
- **Session Management**: Load previous projects, view history, track all iterations

📖 See [FEATURES.md](FEATURES.md) for detailed documentation on all advanced features.

## Quick Start

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd fuzzy-broccoli

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### Running the Application

```bash
# Start the Flask server
python app.py

# Open your browser to http://localhost:5000
```

## Usage

1. **Start a conversation**: Describe your project idea in natural language
2. **Refine the requirements**: Kroosybul AI will ask clarifying questions
3. **Watch it build**: See your project being generated in real-time
4. **Test and iterate**: The system automatically tests and refines the code
5. **Download**: Get your complete, runnable project

## Example Prompts

- "Create a Snake game in Python with Pygame"
- "Build a REST API for a todo app using Flask"
- "Make a real-time chat application with WebSocket support"
- "Generate a machine learning project for image classification"
- "Create a 2D platformer game in JavaScript"

## Architecture

```
Kroosybul AI
├── app.py                      # Main Flask application
├── core/
│   ├── ai_engine.py           # AI integration and orchestration
│   ├── multi_model_engine.py  # Multi-model support (Claude/GPT/Gemini/Ollama)
│   ├── project_generator.py   # Project generation logic
│   ├── code_executor.py       # Safe code execution sandbox
│   ├── session_manager.py     # Session persistence (SQLite)
│   ├── git_manager.py         # Git version control integration
│   ├── venv_manager.py        # Virtual environment management
│   ├── template_library.py    # Template repository system
│   └── templates/             # Project templates
├── static/                    # Frontend assets
├── templates/                 # HTML templates
├── templates_library/         # Template library storage
│   ├── builtin/              # Built-in templates
│   ├── custom/               # User custom templates
│   └── community/            # Community templates
├── generated_projects/        # Output directory
└── sessions.db               # Session database
```

## Configuration

Edit `.env` file:

```bash
# AI Provider API Keys (add the ones you want to use)
ANTHROPIC_API_KEY=your_anthropic_key_here
OPENAI_API_KEY=your_openai_key_here
GOOGLE_API_KEY=your_google_key_here

# AI Model Selection
CLAUDE_MODEL=claude-sonnet-4-5-20250929
OPENAI_MODEL=gpt-4
GEMINI_MODEL=gemini-pro

# Local Models (Ollama)
ENABLE_OLLAMA=false
OLLAMA_MODEL=codellama
OLLAMA_HOST=http://localhost:11434

# Application Settings
MAX_ITERATIONS=10
CODE_TIMEOUT=30
SUPPORTED_LANGUAGES=python,javascript,typescript,java,cpp,rust,go
```

### Using Different AI Models

Kroosybul AI supports multiple AI providers:

1. **Claude** (Anthropic) - Default, excellent for code generation
2. **OpenAI GPT** - Alternative premium option
3. **Google Gemini** - Cost-effective option
4. **Ollama** - Free local models (no API costs!)

To use Ollama locally:
```bash
# Install Ollama from https://ollama.ai
ollama pull codellama
ollama serve

# In .env, set:
ENABLE_OLLAMA=true
```

## Safety

- Code execution runs in isolated sandboxes
- Network access is restricted for generated code
- Resource limits prevent runaway processes
- All generated code is scanned for security issues

## Contributing

Contributions are welcome! This project is designed to be extensible:
- Add new project templates in `core/templates/`
- Support new languages by extending the generator
- Improve the AI prompts for better code generation

## License

MIT License - feel free to use and modify!

## Credits

Inspired by Claude Code and Gemini AI Studio, built with ❤️ for developers who want to kickstart their projects faster.
