# CodeForge AI - Usage Guide

Welcome to CodeForge AI! This guide will help you get the most out of your AI-powered project generator.

## Getting Started

### 1. Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd fuzzy-broccoli

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your Anthropic API key
nano .env  # or use your preferred editor
```

Add your API key:
```
ANTHROPIC_API_KEY=sk-ant-...your-key-here...
```

You can get an API key from: https://console.anthropic.com/

### 3. Run the Application

```bash
python app.py
```

Open your browser to: http://localhost:5000

## How to Use

### Creating Your First Project

1. **Describe Your Idea**: Type a detailed description of what you want to build
   - Example: "Create a Snake game in Python with Pygame"

2. **Wait for Generation**: CodeForge AI will:
   - Analyze your request
   - Plan the project structure
   - Generate all necessary files
   - Test the code
   - Refine any issues

3. **Download Your Project**: Once complete, download the ZIP file and extract it

4. **Run Your Project**: Follow the README.md in the generated project

## Best Practices

### Writing Good Prompts

**Be Specific** ✅
- Good: "Create a REST API for a todo app using Flask with SQLite database, user authentication, and CRUD operations"
- Bad: "Make an app"

**Mention Technology** ✅
- Good: "Build a 2D platformer game in JavaScript using HTML5 Canvas with gravity and collision detection"
- Bad: "Make a game"

**Describe Features** ✅
- Good: "Create a CLI task manager in Python with file persistence, due dates, priorities, and filtering"
- Bad: "Task manager"

**Specify Project Type** ✅
- Good: "Build a machine learning image classifier using Python, TensorFlow, and transfer learning with VGG16"
- Bad: "ML project"

### Example Prompts

#### Games
```
Create a Snake game in Python with Pygame featuring:
- Smooth movement controls
- Score tracking
- Collision detection
- Increasing difficulty
- Game over screen
```

#### Web Applications
```
Build a full-stack todo application with:
- Flask backend with REST API
- SQLite database
- User authentication (JWT)
- CRUD operations for tasks
- Task categories and due dates
- Search and filter functionality
```

#### CLI Tools
```
Create a command-line weather app in Python that:
- Fetches weather data from OpenWeather API
- Shows current conditions and forecast
- Supports multiple cities
- Has colorful terminal output
- Saves favorite locations
```

#### Machine Learning
```
Build an image classification project using Python with:
- TensorFlow/Keras
- Transfer learning with pre-trained models
- Data augmentation
- Training and evaluation scripts
- Model saving and loading
- Prediction API endpoint
```

#### Desktop Applications
```
Create a desktop note-taking app with:
- Python and Tkinter GUI
- Rich text editing
- File save/load functionality
- Search notes feature
- Dark/light theme
```

## Supported Languages

CodeForge AI supports multiple programming languages:

- **Python** - Best for: AI/ML, web apps, scripts, data science
- **JavaScript** - Best for: web apps, games, Node.js servers
- **TypeScript** - Best for: large web applications, type-safe code
- **Java** - Best for: enterprise apps, Android development
- **C++** - Best for: performance-critical apps, games, systems
- **Rust** - Best for: safe systems programming, WebAssembly
- **Go** - Best for: microservices, CLI tools, concurrent systems

## Project Types

### Web Applications
Full-stack web apps with frontend and backend:
- REST APIs
- Real-time applications (WebSocket)
- CRUD applications
- Authentication systems

### Games
2D and 3D games:
- Arcade games (Snake, Pong, Tetris)
- Platformers
- Puzzle games
- Simple RPGs

### CLI Tools
Command-line applications:
- Task managers
- File processors
- API clients
- System utilities

### Machine Learning
AI and data science projects:
- Image classification
- Text analysis
- Data processing pipelines
- Model training scripts

### Desktop Applications
GUI applications:
- Productivity tools
- Utilities
- Database clients
- Media players

## Troubleshooting

### Generated Project Won't Run

1. **Check Dependencies**
   ```bash
   # For Python projects
   pip install -r requirements.txt

   # For JavaScript projects
   npm install
   ```

2. **Check Language Version**
   - Ensure you have the correct version of Python/Node/etc.

3. **Read the README**
   - Every generated project has setup instructions

### Code Has Errors

CodeForge AI tests the code, but some edge cases might occur:

1. **Review Error Messages**: Check what's failing
2. **Install Missing Dependencies**: Sometimes OS-specific packages are needed
3. **Regenerate**: Try regenerating with more specific requirements

### API Key Issues

If you get authentication errors:

1. Check your `.env` file has the correct API key
2. Verify the key is valid at https://console.anthropic.com/
3. Ensure no extra spaces in the `.env` file

## Advanced Features

### Iterative Refinement

CodeForge AI automatically:
- Tests generated code
- Identifies errors
- Fixes issues
- Re-tests
- Repeats up to 10 times

This ensures high-quality, working code.

### Multi-File Projects

The AI can generate complex projects with:
- Multiple modules
- Configuration files
- Documentation
- Test files
- Build scripts

### Language-Specific Features

Each language gets appropriate:
- Package managers (pip, npm, cargo, etc.)
- Configuration files (tsconfig.json, Cargo.toml, etc.)
- Best practices
- Testing setup

## Tips & Tricks

### 1. Start Simple
Build a basic version first, then ask for enhancements

### 2. Use Examples
Click the example buttons in the sidebar for inspiration

### 3. Be Patient
Complex projects take longer to generate (30-60 seconds)

### 4. Iterate
If the first version isn't perfect, describe what needs improvement

### 5. Specify Frameworks
Mention specific libraries/frameworks you want to use:
- "Use Flask" vs "Use Django"
- "Use Pygame" vs "Use Arcade"
- "Use React" vs "Use Vue"

## Environment Variables

Customize CodeForge AI in `.env`:

```bash
# AI Settings
AI_MODEL=claude-sonnet-4-5-20250929  # AI model to use
MAX_ITERATIONS=10                     # Max refinement attempts
AI_TEMPERATURE=0.7                    # Creativity (0.0-1.0)
MAX_TOKENS=8000                       # Max response length

# Code Execution
CODE_TIMEOUT=30                       # Timeout for tests (seconds)
ENABLE_SANDBOX=True                   # Safe code execution

# Languages
SUPPORTED_LANGUAGES=python,javascript,typescript,java,cpp,rust,go

# Server
HOST=0.0.0.0                         # Server host
PORT=5000                            # Server port
```

## FAQ

**Q: Can I generate mobile apps?**
A: Not yet, but web apps and desktop apps are supported

**Q: Will the code be production-ready?**
A: The code is tested and functional, but you should review it for your specific needs

**Q: Can I modify the generated code?**
A: Absolutely! The code is yours to use and modify

**Q: What if I don't know programming?**
A: The generated projects include README files with setup instructions, but basic programming knowledge is helpful

**Q: Can it generate documentation?**
A: Yes! Every project includes a comprehensive README

**Q: Is there a limit to project size?**
A: Projects are limited by the AI's context window, but most practical projects fit easily

## Getting Help

- Check the README.md in your generated project
- Review error messages carefully
- Try regenerating with more details
- File issues on GitHub

## What's Next?

After generating your project:

1. **Explore the Code**: Understand what was generated
2. **Read the README**: Follow setup instructions
3. **Run Tests**: If included, run the test suite
4. **Customize**: Modify the code for your needs
5. **Learn**: Use the generated code to learn new concepts
6. **Share**: Show off your creation!

---

Happy coding with CodeForge AI! 🔥
