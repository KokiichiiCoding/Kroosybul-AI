# CodeForge AI 🔥

An intelligent code generation studio that transforms your ideas into complete, runnable projects across multiple programming languages.

## Features

- **Multi-Language Support**: Generate projects in Python, JavaScript, TypeScript, Java, C++, Rust, Go, and more
- **Project Templates**: Pre-built templates for games, web apps, APIs, CLI tools, and AI applications
- **Iterative Refinement**: Continuously improves code until it works perfectly
- **Real-time Chat Interface**: Natural conversation to describe your project
- **Automatic Testing**: Built-in code execution and validation
- **Smart Dependencies**: Automatic dependency detection and management
- **Progress Tracking**: Visual feedback on generation progress
- **Export Projects**: Download complete, ready-to-run projects

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

- "Create a Snake game in Python with Pygame"
- "Build a REST API for a todo app using Flask"
- "Make a real-time chat application with WebSocket support"
- "Generate a machine learning project for image classification"
- "Create a 2D platformer game in JavaScript"

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

```
ANTHROPIC_API_KEY=your_api_key_here
MAX_ITERATIONS=10
CODE_TIMEOUT=30
SUPPORTED_LANGUAGES=python,javascript,typescript,java,cpp,rust,go
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
