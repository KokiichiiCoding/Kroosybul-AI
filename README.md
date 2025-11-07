# Kroosybul AI 🔥

An intelligent AI-powered code generation studio that transforms your ideas into complete, runnable projects across multiple programming languages. Now with **10+ new advanced features** including multi-model support, architecture diagrams, natural-language debugging, and more!

## ✨ Core Features

- **Multi-Language Support**: Generate projects in Python, JavaScript, TypeScript, Java, C++, Rust, Go, and more
- **15+ Project Templates**: Discord bots, Flask dashboards, Next.js apps, AI agents, WebGL games, Chrome extensions, and more
- **Iterative Refinement**: Continuously improves code until it works perfectly
- **Real-time Chat Interface**: Natural conversation to describe your project
- **Automatic Testing**: Built-in code execution and validation
- **Smart Dependencies**: Automatic dependency detection and management
- **Progress Tracking**: Visual feedback on generation progress
- **Export Projects**: Download complete, ready-to-run projects

## 🚀 NEW Advanced Features

### AI & Intelligence
- **🤖 Multi-Model Support**: Choose between Claude, GPT-4, or Gemini
- **🧠 AI Architecture Planner**: Auto-generates Mermaid.js diagrams before coding
- **🔍 Natural-Language Debugging**: Plain-English error explanations with fix suggestions
- **📊 AI-Powered Test Summaries**: Human-readable test result analysis
- **📝 Auto-Documentation**: Generates comments and docstrings for all code
- **⚡ Performance Metrics**: AI-estimated complexity analysis (Big-O notation)

### Developer Tools
- **📁 File Upload Support**: Upload existing code for context-aware generation
- **🔧 Dependency Intelligence**: Auto-detects and manages imports
- **📚 Component Library**: Save and reuse code snippets across projects
- **🎨 15+ New Templates**: Discord bots, AI agents, dashboards, games, and more

**[📖 View Detailed Feature Documentation →](NEW_FEATURES.md)**

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
2. **Refine the requirements**: CodeForge AI will ask clarifying questions
3. **Watch it build**: See your project being generated in real-time
4. **Test and iterate**: The system automatically tests and refines the code
5. **Download**: Get your complete, runnable project

## Example Prompts

### Classic Projects
- "Create a Snake game in Python with Pygame"
- "Build a REST API for a todo app using Flask"
- "Make a real-time chat application with WebSocket support"
- "Generate a machine learning project for image classification"

### NEW Templates
- "Create a Discord bot with slash commands and database integration"
- "Build a Flask dashboard with real-time data and authentication"
- "Make a Next.js dashboard with TypeScript and TailwindCSS"
- "Generate a LangChain AI agent with tool calling capabilities"
- "Create a WebGL mini-game with Three.js and physics"
- "Build a Telegram bot with inline keyboards"
- "Make a FastAPI microservice with async endpoints"
- "Create a Chrome extension with popup and content scripts"

## Architecture

```
CodeForge AI
├── app.py                  # Main Flask application
├── core/
│   ├── ai_engine.py       # AI integration and orchestration
│   ├── project_generator.py # Project generation logic
│   ├── code_executor.py   # Safe code execution sandbox
│   └── templates/         # Project templates
├── static/                # Frontend assets
├── templates/             # HTML templates
└── generated_projects/    # Output directory
```

## Configuration

Edit `.env` file:

```bash
# Required: Choose at least one AI provider
ANTHROPIC_API_KEY=your_api_key_here

# Optional: Multi-model support
OPENAI_API_KEY=your_openai_key_optional
GOOGLE_API_KEY=your_google_key_optional

# AI Settings
MAX_ITERATIONS=10
AI_TEMPERATURE=0.7
MAX_TOKENS=8000

# Code Execution
CODE_TIMEOUT=30
ENABLE_SANDBOX=True

# Supported Languages
SUPPORTED_LANGUAGES=python,javascript,typescript,java,cpp,rust,go
```

### Multi-Model Configuration

Kroosybul AI now supports multiple AI models! Configure your preferred provider(s):

- **Claude Sonnet 4.5** (Anthropic): Best for code generation and long context
- **GPT-4** (OpenAI): Versatile and creative, excellent for diverse projects
- **Gemini Pro** (Google): Fast and efficient for quick iterations

You can configure one or all three models - the system will use the available ones.

## Safety

- Code execution runs in isolated sandboxes
- Network access is restricted for generated code
- Resource limits prevent runaway processes
- All generated code is scanned for security issues

## API Endpoints

### Project Generation
- `GET /api/health` - Health check
- `GET /api/languages` - Get supported languages
- `GET /api/templates` - Get all project templates
- `GET /api/templates/category/<category>` - Filter templates by category

### NEW Enhanced Features
- `GET /api/models` - Get available AI models
- `POST /api/components/search` - Search reusable components
- `POST /api/components/save` - Save a component
- `POST /api/analyze/complexity` - Analyze code complexity
- `POST /api/document/generate` - Generate documentation

### WebSocket Events
- `message` - Send project request
- `upload_file` - Upload code for context
- `architecture_diagram` - Receive Mermaid.js diagram
- `error_explanation` - Get natural-language error help
- `test_summary` - AI-generated test summary
- `project_complete` - Project ready for download

See [NEW_FEATURES.md](NEW_FEATURES.md) for detailed API documentation.

## Contributing

Contributions are welcome! This project is designed to be extensible:
- Add new project templates in `core/project_templates.py`
- Support new languages by extending the generator
- Improve the AI prompts for better code generation
- Add new enhanced features in `core/enhanced_features.py`

## License

MIT License - feel free to use and modify!

## Credits

Inspired by Claude Code and Gemini AI Studio, built with ❤️ for developers who want to kickstart their projects faster.
