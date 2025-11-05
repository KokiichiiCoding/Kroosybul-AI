# Kroosybul AI - Advanced Features Guide

This document describes all the advanced features available in Kroosybul AI.

## Table of Contents

1. [Context Persistence](#context-persistence)
2. [Dependency Smart Install](#dependency-smart-install)
3. [Git Integration](#git-integration)
4. [Multi-Model Support](#multi-model-support)
5. [Template Library](#template-library)
6. [API Reference](#api-reference)

---

## 1. Context Persistence

Save and resume your project sessions anytime. Never lose your progress!

### Features

- **Auto-save sessions**: Every project generation is automatically saved to a SQLite database
- **Load previous projects**: Continue working on any previous project
- **Session history**: View all your past projects with full chat history
- **Iteration tracking**: See all refinements made to each project

### Usage

#### Via API

```bash
# List all sessions
curl http://localhost:5000/api/sessions

# Load a specific session
curl http://localhost:5000/api/sessions/<session_id>

# Delete a session
curl -X DELETE http://localhost:5000/api/sessions/<session_id>

# Update session status (active, archived, completed)
curl -X PUT http://localhost:5000/api/sessions/<session_id>/status \
  -H "Content-Type: application/json" \
  -d '{"status": "archived"}'
```

#### Via WebSocket

```javascript
// Load a previous session
socket.emit('load_session', {
  session_id: 'previous-session-id-here'
});

// Listen for session loaded event
socket.on('session_loaded', (data) => {
  console.log('Session loaded:', data);
  // data contains: messages, project, created_at, updated_at
});
```

### Session Data Structure

```json
{
  "session_id": "abc123",
  "created_at": "2025-01-01T12:00:00",
  "updated_at": "2025-01-01T14:30:00",
  "current_project": {
    "name": "My Project",
    "description": "Project description",
    "language": "python",
    "path": "/path/to/project",
    "files": ["file1.py", "file2.py"],
    "dependencies": ["flask", "requests"],
    "test_results": {...}
  },
  "messages": [
    {
      "role": "user",
      "content": "Create a web app",
      "timestamp": "2025-01-01T12:00:00"
    },
    {
      "role": "assistant",
      "content": "I'll create a web application for you...",
      "timestamp": "2025-01-01T12:00:05"
    }
  ],
  "iterations": [...]
}
```

---

## 2. Dependency Smart Install

Automatic dependency management with virtual environments and conflict resolution.

### Features

- **Auto virtual environment**: Automatically creates language-specific virtual environments
- **Dependency installation**: Detects and installs all required dependencies
- **Conflict detection**: Identifies and reports version conflicts
- **Multi-language support**: Python (venv/pip), Node.js (npm/yarn), Rust (cargo), Go (go mod), Ruby (bundler)

### Supported Languages

| Language | Virtual Env | Package Manager | Config File |
|----------|-------------|-----------------|-------------|
| Python | venv | pip/poetry/pipenv | requirements.txt |
| JavaScript/TypeScript | node_modules | npm/yarn/pnpm | package.json |
| Rust | - | cargo | Cargo.toml |
| Go | - | go mod | go.mod |
| Ruby | - | bundler | Gemfile |

### Usage

Virtual environments are created automatically during project generation. You can also manage them manually:

```python
from core.venv_manager import VenvManager

venv_manager = VenvManager()

# Create virtual environment
success, message = venv_manager.create_venv(
    project_path="/path/to/project",
    language="python"
)

# Install dependencies
success, message, installed = venv_manager.install_dependencies(
    project_path="/path/to/project",
    language="python",
    dependencies=["flask", "requests"]
)

# Check for conflicts
has_conflicts, conflicts = venv_manager.check_version_conflicts(
    project_path="/path/to/project",
    language="python"
)

# Get activation command
cmd = venv_manager.get_activation_command(
    project_path="/path/to/project",
    language="python"
)
# Returns: "source /path/to/project/.venv/bin/activate"
```

---

## 3. Git Integration

Automatic version control for all generated projects.

### Features

- **Auto-initialize**: Every project gets a Git repository automatically
- **Iteration commits**: Each refinement iteration is committed with a descriptive message
- **Rollback support**: Easily revert to any previous version
- **Branch management**: Create and manage branches
- **Custom .gitignore**: Language-specific gitignore templates

### Usage

#### Via API

```bash
# Get repository status
curl http://localhost:5000/api/git/<session_id>/status

# Get commit history
curl http://localhost:5000/api/git/<session_id>/history?limit=10

# Rollback to a commit
curl -X POST http://localhost:5000/api/git/<session_id>/rollback \
  -H "Content-Type: application/json" \
  -d '{"commit_hash": "abc123"}'
```

#### Via Python

```python
from core.git_manager import GitManager

git_manager = GitManager()

# Initialize repository
success, message = git_manager.init_repository(
    project_path="/path/to/project",
    language="python"
)

# Commit changes
success, message = git_manager.commit_changes(
    project_path="/path/to/project",
    message="Add new feature",
    add_all=True
)

# Commit iteration
success, message = git_manager.commit_iteration(
    project_path="/path/to/project",
    iteration_number=2,
    description="Fixed syntax errors"
)

# Get commit history
commits = git_manager.get_commit_history(
    project_path="/path/to/project",
    limit=10
)

# Rollback to commit
success, message = git_manager.rollback_to_commit(
    project_path="/path/to/project",
    commit_hash="abc123"
)

# Create branch
success, message = git_manager.create_branch(
    project_path="/path/to/project",
    branch_name="feature/new-feature"
)

# Get status
status = git_manager.get_status(project_path="/path/to/project")
# Returns: {branch, modified_files, commit_count, is_clean}
```

---

## 4. Multi-Model Support

Switch between different AI providers based on your needs and budget.

### Supported Providers

| Provider | Models | Cost | Speed | Quality |
|----------|--------|------|-------|---------|
| **Claude** (Anthropic) | Sonnet 4.5, Opus, Haiku | $$ | Fast | Excellent |
| **OpenAI** | GPT-4, GPT-4 Turbo, GPT-3.5 | $$$ | Fast | Excellent |
| **Gemini** (Google) | Gemini Pro, Gemini 1.5 Pro | $ | Fast | Good |
| **Ollama** (Local) | CodeLlama, Mistral, Llama2 | Free | Medium | Good |

### Setup

Add your API keys to `.env`:

```bash
# Claude (Anthropic)
ANTHROPIC_API_KEY=your_key_here
CLAUDE_MODEL=claude-sonnet-4-5-20250929

# OpenAI
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4

# Google Gemini
GOOGLE_API_KEY=your_key_here
GEMINI_MODEL=gemini-pro

# Ollama (Local)
ENABLE_OLLAMA=true
OLLAMA_MODEL=codellama
OLLAMA_HOST=http://localhost:11434
```

### Usage

#### Via API

```bash
# Get available models
curl http://localhost:5000/api/models

# Switch model
curl -X POST http://localhost:5000/api/models/switch \
  -H "Content-Type: application/json" \
  -d '{"provider": "openai"}'

# Get usage statistics
curl http://localhost:5000/api/models/usage
```

#### Via Python

```python
from core.multi_model_engine import MultiModelEngine

engine = MultiModelEngine()

# List available providers
providers = engine.get_available_providers()
# Returns: ['claude', 'openai', 'gemini', 'ollama']

# Switch provider
engine.set_provider('openai')

# Generate with current provider
text, metadata = engine.generate(
    prompt="Create a Python function to sort a list",
    temperature=0.7,
    max_tokens=1000
)

# Check metadata
print(f"Provider: {metadata['provider']}")
print(f"Model: {metadata['model']}")
print(f"Cost: ${metadata['cost']:.4f}")
print(f"Tokens: {metadata['input_tokens']} in, {metadata['output_tokens']} out")

# Get usage statistics
stats = engine.get_usage_stats()
print(f"Total API calls: {stats['total_calls']}")
print(f"Total cost: ${stats['total_cost']:.2f}")
print(f"By provider: {stats['by_provider']}")

# Save usage history
engine.save_usage_history('usage_history.json')
```

### Cost Tracking

Every API call is tracked with:
- Input/output token counts
- Cost calculation (per provider pricing)
- Timestamp
- Provider and model used

Access detailed cost reports:

```python
stats = engine.get_usage_stats()

print(f"Total spent: ${stats['total_cost']:.2f}")

for provider, data in stats['by_provider'].items():
    print(f"\n{provider}:")
    print(f"  Calls: {data['calls']}")
    print(f"  Tokens: {data['input_tokens']} in, {data['output_tokens']} out")
    print(f"  Cost: ${data['cost']:.2f}")
```

### Using Local Models (Ollama)

1. Install Ollama: https://ollama.ai
2. Pull a model: `ollama pull codellama`
3. Start Ollama: `ollama serve`
4. Enable in `.env`: `ENABLE_OLLAMA=true`

Benefits:
- **Free**: No API costs
- **Private**: Data stays local
- **Fast**: No network latency
- **Offline**: Works without internet

---

## 5. Template Library

Access battle-tested project templates and create your own.

### Built-in Templates

| Template | Category | Languages | Description |
|----------|----------|-----------|-------------|
| **Full-Stack Web App** | Web | JS/TS | React frontend + Node/Express backend |
| **REST API** | Backend | Python/JS/TS | Production-ready API with auth |
| **Microservice** | Backend | Python/JS/Go | Containerized microservice |
| **ML Project** | ML | Python | Data processing + training + inference |
| **CLI Tool** | Tools | Python/Rust/Go | Professional command-line app |
| **2D Game** | Game | Python/JS | Sprite rendering + physics |
| **Desktop App** | Desktop | JS/Python | Cross-platform GUI app |
| **Data Pipeline** | Data | Python | ETL pipeline with Airflow |

### Usage

#### Via API

```bash
# List all templates
curl http://localhost:5000/api/library/templates

# Filter templates
curl http://localhost:5000/api/library/templates?category=web&language=python&battle_tested=true

# Get template details
curl http://localhost:5000/api/library/templates/rest_api

# Create custom template
curl -X POST http://localhost:5000/api/library/templates \
  -H "Content-Type: application/json" \
  -d '{
    "id": "my_template",
    "name": "My Custom Template",
    "description": "A custom template for my projects",
    "category": "web",
    "languages": ["python"],
    "tags": ["custom", "api"],
    "structure": {
      "src": ["controllers", "models"],
      "tests": []
    }
  }'

# Export template
curl http://localhost:5000/api/library/templates/my_template/export \
  -o my_template.zip

# Search templates
curl http://localhost:5000/api/library/search?q=api
```

#### Via Python

```python
from core.template_library import TemplateLibrary

library = TemplateLibrary()

# List templates
templates = library.list_templates(
    category='web',
    language='python',
    battle_tested=True
)

# Get template
template = library.get_template('rest_api')

# Create custom template
success, message = library.create_template({
    'id': 'my_template',
    'name': 'My Template',
    'description': 'Custom template',
    'category': 'web',
    'languages': ['python'],
    'tags': ['api', 'backend'],
    'structure': {
        'src': ['controllers', 'models'],
        'tests': []
    },
    'dependencies': {
        'python': ['flask', 'sqlalchemy']
    }
}, source='custom')

# Export template
success, message = library.export_template(
    template_id='my_template',
    output_path='my_template.zip'
)

# Import template
success, message = library.import_template(
    import_path='template.zip',
    source='community'
)

# Search templates
results = library.search_templates('api')

# Get categories
categories = library.get_categories()
# Returns: ['web', 'backend', 'ml', 'game', 'tools', 'data', 'desktop']
```

### Creating Custom Templates

Template structure:

```json
{
  "id": "unique_id",
  "name": "Display Name",
  "description": "What this template does",
  "category": "web|backend|ml|game|tools|data|desktop",
  "tags": ["tag1", "tag2"],
  "languages": ["python", "javascript"],
  "battle_tested": false,
  "structure": {
    "src": ["subdir1", "subdir2"],
    "tests": [],
    "config": []
  },
  "dependencies": {
    "python": ["package1", "package2"],
    "javascript": ["package1", "package2"]
  }
}
```

---

## 6. API Reference

### Session Management

- `GET /api/sessions` - List all sessions
- `GET /api/sessions/<id>` - Get session details
- `DELETE /api/sessions/<id>` - Delete session
- `PUT /api/sessions/<id>/status` - Update status

### Model Management

- `GET /api/models` - List available models
- `POST /api/models/switch` - Switch model provider
- `GET /api/models/usage` - Get usage statistics

### Template Library

- `GET /api/library/templates` - List templates
- `GET /api/library/templates/<id>` - Get template
- `POST /api/library/templates` - Create template
- `DELETE /api/library/templates/<id>` - Delete template
- `GET /api/library/templates/<id>/export` - Export template
- `POST /api/library/templates/import` - Import template
- `GET /api/library/search?q=query` - Search templates

### Git Management

- `GET /api/git/<session_id>/status` - Get repo status
- `GET /api/git/<session_id>/history` - Get commit history
- `POST /api/git/<session_id>/rollback` - Rollback to commit

### WebSocket Events

#### Client → Server

- `message` - Send user message to generate project
- `load_session` - Load a previous session

#### Server → Client

- `connected` - Connection established
- `message_received` - Message acknowledged
- `status` - Status update during generation
- `progress` - Progress update (file generation)
- `ai_response` - AI response message
- `project_complete` - Project generation complete
- `session_loaded` - Previous session loaded
- `error` - Error occurred

---

## Best Practices

### Session Management

1. Archive completed sessions to keep the active list clean
2. Use meaningful project descriptions for easier searching
3. Regularly back up the `sessions.db` file

### Dependency Management

1. Let Kroosybul AI create virtual environments automatically
2. Check for conflicts before deploying
3. Use lock files (requirements.txt, package-lock.json) for reproducibility

### Git Integration

1. Review commit history before making manual changes
2. Use rollback carefully - it performs a hard reset
3. Create branches for experimental features

### Multi-Model Usage

1. Use Claude/GPT-4 for complex projects
2. Use GPT-3.5/Gemini for simple tasks (lower cost)
3. Use Ollama for development/testing (free)
4. Monitor usage statistics to control costs

### Templates

1. Start with battle-tested templates for production
2. Customize templates for your common use cases
3. Export and share templates with your team
4. Keep template dependencies up to date

---

## Troubleshooting

### Virtual Environment Issues

```bash
# If venv creation fails, ensure you have venv installed
python -m pip install virtualenv

# For Node.js, ensure npm is installed
npm --version
```

### Git Issues

```bash
# If Git initialization fails, ensure Git is installed
git --version

# Configure Git user
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

### Ollama Connection Issues

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama
ollama serve
```

### API Key Issues

- Double-check API keys in `.env` file
- Ensure no extra spaces or quotes around keys
- Verify API key permissions and quotas

---

## Support

For issues or feature requests, please visit:
https://github.com/YourUsername/Kroosybul-AI/issues

---

**Happy Coding with Kroosybul AI!** 🚀
