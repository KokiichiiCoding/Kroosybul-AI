# Kroosybul AI - Architecture Documentation

This document provides a detailed technical overview of the Kroosybul AI (CodeForge AI) codebase.

**Generated:** 2025-11-05  
**Version:** 1.0.0

---

## Quick Navigation

1. [Project Overview](#project-overview)
2. [Directory Structure](#directory-structure)
3. [Component Architecture](#component-architecture)
4. [Data Flow Diagrams](#data-flow-diagrams)
5. [Tech Stack](#tech-stack)
6. [Configuration](#configuration)
7. [API Reference](#api-reference)
8. [File Generation Pipeline](#file-generation-pipeline)
9. [Integration Points](#integration-points)
10. [Performance Metrics](#performance-metrics)

---

## Project Overview

**Kroosybul AI** is an intelligent code generation platform that:

- Accepts natural language project descriptions
- Uses Claude AI to analyze and plan projects
- Generates complete, production-ready project structures
- Tests generated code automatically
- Iteratively refines code until it works
- Packages projects for download

**Key Statistics:**
- ~3,000 lines of code total
- ~1,450 lines of Python (backend)
- ~1,130 lines of JavaScript/HTML/CSS (frontend)
- Supports 11+ programming languages
- 6 project template types

---

## Directory Structure

```
/home/user/Kroosybul-AI/
│
├── ARCHITECTURE.md                 # This file
├── README.md                       # Project overview
├── USAGE.md                        # User guide
├── CONTRIBUTING.md                # Contribution guidelines
├── CHANGELOG.md                    # Version history
│
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment template
├── .gitignore                      # Git ignore rules
│
├── core/                           # Core business logic
│   ├── __init__.py
│   ├── ai_engine.py               # Claude API integration
│   ├── project_generator.py       # Project structure creation
│   └── code_executor.py           # Code validation & testing
│
├── static/                         # Frontend assets
│   ├── css/
│   │   └── style.css              # Styling (dark theme)
│   └── js/
│       └── app.js                 # Client-side logic
│
├── templates/
│   └── index.html                 # Main HTML interface
│
├── generated_projects/            # Output directory (created at runtime)
│
├── run.sh                          # Linux/Mac startup script
├── run.bat                         # Windows startup script
└── test_setup.py                  # Setup utilities

```

---

## Component Architecture

### 1. Flask Web Server (app.py)

```
┌─────────────────────────────────────────┐
│         Flask Application               │
│                                         │
│  ├─ GET /                     (UI)      │
│  ├─ GET /api/health           (Status)  │
│  ├─ GET /api/languages        (Config)  │
│  ├─ GET /api/templates        (Config)  │
│  ├─ GET /api/download/<id>    (Download)
│  └─ WS /message               (Main)    │
│                                         │
│  Session Management:                    │
│  • active_sessions (dict)              │
│  • Per-socket ID tracking              │
│                                         │
└─────────────────────────────────────────┘
```

**Responsibilities:**
- HTTP routing
- WebSocket connection handling
- Session lifecycle management
- Project download packaging

---

### 2. AI Engine (core/ai_engine.py)

```
┌─────────────────────────────────────────┐
│         AI Engine (Claude)              │
│                                         │
│  ├─ analyze_project_request()          │
│  │   └─ Prompts: "Analyze request"     │
│  │   └─ Returns: Project plan JSON     │
│  │                                      │
│  ├─ generate_file_content()            │
│  │   └─ Prompts: "Generate this file"  │
│  │   └─ Returns: File content (string) │
│  │                                      │
│  ├─ fix_code_issues()                  │
│  │   └─ Prompts: "Fix these errors"    │
│  │   └─ Returns: Fixes (file mapping)  │
│  │                                      │
│  └─ enhance_project_idea()             │
│      └─ Prompts: "Enhance idea"        │
│      └─ Returns: Enhanced description  │
│                                         │
│  Configuration:                         │
│  • Model: claude-sonnet-4-5-20250929   │
│  • Max Tokens: 8000                    │
│  • Temperature: 0.7                    │
│                                         │
└─────────────────────────────────────────┘
```

**Prompting Strategy:**
- Structured output (JSON) with error handling
- Context-aware prompts with project details
- Markdown parsing for code blocks
- Fallback defaults on parse failure

---

### 3. Project Generator (core/project_generator.py)

```
┌─────────────────────────────────────────┐
│      Project Generator                  │
│                                         │
│  ├─ generate_project()                 │
│  │   ├─ Create directory                │
│  │   ├─ For each file:                  │
│  │   │   ├─ Call AI: generate_file()   │
│  │   │   └─ Write to disk              │
│  │   ├─ Generate config files          │
│  │   ├─ Generate README                │
│  │   └─ Save metadata JSON             │
│  │                                      │
│  ├─ _generate_config_files()           │
│  │   ├─ Python: requirements.txt       │
│  │   ├─ Node: package.json, tsconfig   │
│  │   ├─ Rust: Cargo.toml               │
│  │   └─ Go: go.mod                     │
│  │                                      │
│  ├─ _generate_readme()                 │
│  │   └─ Comprehensive setup guide      │
│  │                                      │
│  ├─ apply_fixes()                      │
│  │   └─ Update files from AI fixes     │
│  │                                      │
│  ├─ create_zip()                       │
│  │   └─ Package for download           │
│  │                                      │
│  └─ get_available_templates()          │
│      └─ Return template list           │
│                                         │
│  Language Configs:                      │
│  {python, javascript, typescript,      │
│   java, cpp, rust, go}                 │
│                                         │
└─────────────────────────────────────────┘
```

**Output Structure:**
```
generated_projects/
└── project-name_20251105_143022/
    ├── main.py (or main file for language)
    ├── other_source_files.py
    ├── requirements.txt
    ├── README.md
    └── .codeforge_metadata.json
```

---

### 4. Code Executor (core/code_executor.py)

```
┌─────────────────────────────────────────┐
│      Code Executor                      │
│                                         │
│  test_project() → language-specific:    │
│                                         │
│  ├─ _test_python()                     │
│  │   └─ python -m py_compile           │
│  │                                      │
│  ├─ _test_javascript()                 │
│  │   └─ node --check                   │
│  │                                      │
│  ├─ _test_typescript()                 │
│  │   └─ tsc --noEmit                   │
│  │                                      │
│  ├─ _test_rust()                       │
│  │   └─ cargo check                    │
│  │                                      │
│  ├─ _test_go()                         │
│  │   └─ go build                       │
│  │                                      │
│  ├─ _test_java()                       │
│  │   └─ javac                          │
│  │                                      │
│  ├─ _test_cpp()                        │
│  │   └─ g++ -fsyntax-only              │
│  │                                      │
│  └─ _test_generic()                    │
│      └─ File counting fallback         │
│                                         │
│  Safety:                                │
│  • Syntax validation only (no exec)    │
│  • Subprocess timeout: 30s              │
│  • RestrictedPython for analysis       │
│                                         │
└─────────────────────────────────────────┘
```

**Test Output Format:**
```python
{
    'success': bool,
    'errors': [str, ...],
    'warnings': [str, ...],
    'tested_files': int
}
```

---

## Data Flow Diagrams

### Complete Project Generation Flow

```
User Input (natural language)
     ↓
[WebSocket: /message event]
     ↓
Flask Message Handler (app.py)
     ↓
AIEngine.analyze_project_request()
     ├─ Sends to Claude: "Analyze project"
     ├─ Parses JSON response
     └─ Returns: project_plan
     ↓
[Emit: status="Analyzing..."]
     ↓
ProjectGenerator.generate_project()
     ├─ Create directory
     ├─ For each file in plan:
     │  ├─ AIEngine.generate_file_content()
     │  └─ Write to disk
     ├─ _generate_config_files()
     ├─ _generate_readme()
     └─ Save metadata
     ↓
[Emit: progress updates]
     ↓
CodeExecutor.test_project()
     ├─ Language-specific validation
     └─ Returns: test_results
     ↓
[Emit: status="Testing..."]
     ↓
If errors AND iterations < MAX:
     ├─ AIEngine.fix_code_issues()
     ├─ ProjectGenerator.apply_fixes()
     └─ CodeExecutor.test_project() [loop]
     ↓
[Emit: status="Complete"]
     ↓
ProjectGenerator.create_zip()
     ↓
[Emit: project_complete with download_url]
     ↓
User Downloads ZIP
```

### WebSocket Communication Pattern

```
Browser (Client)              Flask Server
     │                              │
     ├─ connect ─────────────────→  ├─ handle_connect()
     ←─ connected ─────────────────  │
     │                              │
     ├─ message ───────────────────→ ├─ handle_message()
     │                              │
     ←─ status ─────────────────────  │ (multiple events)
     ←─ progress ────────────────────  │
     ←─ ai_response ──────────────────  │
     ←─ project_complete ────────────  │
     │                              │
     ├─ [download via HTTP] ────────→ /api/download/session_id
     ←─ [ZIP file] ──────────────────  │
     │                              │
     ├─ disconnect ──────────────────→ ├─ handle_disconnect()
```

---

## Tech Stack

### Backend Stack

```
Python 3.8+
  ├─ Flask 3.0.0
  │   ├─ flask-cors 4.0.0
  │   └─ flask-socketio 5.3.5
  │       └─ python-socketio 5.11.0
  │
  ├─ Anthropic 0.39.0 (Claude API)
  │
  ├─ Code Analysis
  │   ├─ RestrictedPython 7.0
  │   └─ astunparse 1.6.3
  │
  ├─ Project Management
  │   ├─ GitPython 3.1.40
  │   └─ Jinja2 3.1.2
  │
  ├─ Server
  │   ├─ Gunicorn 21.2.0
  │   └─ Eventlet 0.33.3
  │
  ├─ Utilities
  │   ├─ python-dotenv 1.0.0
  │   ├─ requests 2.31.0
  │   └─ PyYAML 6.0.1
  │
  └─ Development
      ├─ pytest 7.4.3
      ├─ black 23.12.0
      └─ flake8 6.1.0
```

### Frontend Stack

```
JavaScript (Vanilla)
  ├─ Socket.IO 4.5.4 (client)
  └─ Browser APIs:
      ├─ WebSocket
      ├─ Fetch API
      ├─ DOM APIs
      └─ CSS3

HTML5 / CSS3
  ├─ CSS Grid & Flexbox
  ├─ CSS Custom Properties
  ├─ CSS Animations
  └─ Responsive Design
```

---

## Configuration

### Environment Variables (.env)

```bash
# API Keys
ANTHROPIC_API_KEY=sk-ant-...

# Flask Settings
FLASK_ENV=development|production
FLASK_DEBUG=True|False
SECRET_KEY=your-secret-key

# AI Model Settings
AI_MODEL=claude-sonnet-4-5-20250929
MAX_TOKENS=8000 (per call)
AI_TEMPERATURE=0.7 (0-1)
MAX_ITERATIONS=10 (refinement loops)

# Code Execution
CODE_TIMEOUT=30 (seconds)
MAX_FILE_SIZE=10485760 (10MB)
ENABLE_SANDBOX=True

# Languages & Projects
SUPPORTED_LANGUAGES=python,javascript,...
GENERATED_PROJECTS_DIR=generated_projects
MAX_PROJECT_SIZE=104857600 (100MB)

# Server
HOST=0.0.0.0
PORT=5000
```

### Language Support Configuration

Each language in `ProjectGenerator.language_configs`:

```python
{
    'extensions': ['.py'],           # File extensions
    'main_file': 'main.py',         # Entry point
    'config_files': [...],          # Required config files
    'test_command': 'python ...'    # Validation command
}
```

---

## API Reference

### HTTP Endpoints

#### GET /
Serves the main UI.

**Response:**
```html
HTML page with embedded Socket.IO client
```

---

#### GET /api/health
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-11-05T14:30:22.123456",
  "version": "1.0.0"
}
```

---

#### GET /api/languages
List supported programming languages.

**Response:**
```json
{
  "languages": ["python", "javascript", "typescript", ...],
  "templates": [...]
}
```

---

#### GET /api/templates
Get available project templates.

**Response:**
```json
{
  "templates": [
    {
      "id": "web_app",
      "name": "Web Application",
      "description": "...",
      "languages": ["python", "javascript", "typescript"]
    },
    ...
  ]
}
```

---

#### GET /api/download/<session_id>
Download generated project as ZIP.

**Parameters:**
- `session_id` (URL): Session ID from WebSocket connection

**Response:**
```
Content-Type: application/zip
(ZIP file binary data)
```

**Errors:**
```json
{"error": "Project not found"} (404)
```

---

### WebSocket Events

#### Client → Server

**message**
```json
{
  "message": "Create a Snake game in Python with Pygame"
}
```

---

#### Server → Client

**connected**
```json
{
  "session_id": "abc123xyz"
}
```

---

**status**
```json
{
  "message": "Analyzing your request...",
  "stage": "analysis|planning|generation|testing|refinement|complete",
  "iteration": 1
}
```

---

**progress**
```json
{
  "message": "Generating file 1/15: main.py"
}
```

---

**ai_response**
```json
{
  "message": "Project plan created...",
  "type": "plan|result|error"
}
```

---

**project_complete**
```json
{
  "project_path": "/path/to/project",
  "project_name": "my-project",
  "files": ["main.py", "README.md", ...],
  "download_url": "/api/download/session_id",
  "test_results": {
    "success": true,
    "errors": [],
    "warnings": [],
    "tested_files": 5
  },
  "warnings": false
}
```

---

**error**
```json
{
  "message": "Error message describing what went wrong"
}
```

---

## File Generation Pipeline

### Step 1: Analysis
```
User: "Create a Snake game in Python with Pygame"
     ↓
Claude: Analyze request → JSON project plan
     ↓
Output:
{
  "project_name": "snake-game",
  "description": "A classic Snake game with...",
  "language": "python",
  "project_type": "game",
  "frameworks": ["pygame"],
  "features": ["smooth movement", "score tracking", ...],
  "files": [
    {"path": "main.py", "purpose": "Game loop", "priority": "high"},
    ...
  ],
  "dependencies": ["pygame>=2.0.0"],
  ...
}
```

### Step 2: File Generation
```
For each file in plan:
  Claude: Generate {path} with {purpose}
     ↓
  Output: Complete source code
     ↓
  Write to: {project_dir}/{path}
     ↓
  Track progress
```

### Step 3: Configuration
```
Generate:
  • requirements.txt (dependencies)
  • .gitignore (Python patterns)
  • README.md (setup & usage)
  • .codeforge_metadata.json (tracking)
```

### Step 4: Testing
```
For each source file:
  python -m py_compile {file}
     ↓
  Capture errors
     ↓
  Return test_results object
```

### Step 5: Refinement (if errors)
```
If test_results.errors AND iterations < MAX:
  Claude: Fix these errors in project
     ↓
  Output: {"file.py": "fixed content", ...}
     ↓
  Apply fixes
     ↓
  Re-test
     ↓
  Loop
```

### Step 6: Packaging
```
Create ZIP:
  {project_name}_{timestamp}.zip
     ↓
  Return download link
```

---

## Integration Points

### Adding New Language Support

**1. Update ProjectGenerator:**
```python
# core/project_generator.py
self.language_configs = {
    'newlang': {
        'extensions': ['.ext'],
        'main_file': 'main.ext',
        'config_files': ['config.ext'],
        'test_command': 'newlang-compile'
    }
}
```

**2. Implement Test Method in CodeExecutor:**
```python
# core/code_executor.py
def _test_newlang(self, project_path: Path, metadata: Dict):
    # Syntax validation logic
    pass
```

**3. Register in Test Commands:**
```python
# core/code_executor.py
self.test_commands = {
    'newlang': self._test_newlang
}
```

**4. Update Config:**
```bash
# .env
SUPPORTED_LANGUAGES=...,newlang
```

---

### Adding New Project Templates

**1. Define Template:**
```python
# core/project_generator.py
def get_available_templates(self):
    return [
        {
            'id': 'new_template',
            'name': 'New Template',
            'description': '...',
            'languages': ['python', 'javascript']
        },
        ...
    ]
```

**2. Create Template Directory (future):**
```
core/templates/
└── new_template/
    ├── python/
    │   ├── main.py
    │   └── requirements.txt
    └── javascript/
        ├── index.js
        └── package.json
```

---

### Adding Pre-Generation Features

**1. Extend Project Plan:**
```python
# core/ai_engine.py
project_plan = {
    ...
    "new_field": "value"
}
```

**2. Use in Generator:**
```python
# core/project_generator.py
if project_plan.get('new_field'):
    # Use the field
```

---

### Adding Post-Generation Features

**1. Extend Test Results:**
```python
# core/code_executor.py
return {
    ...
    'new_metric': value
}
```

**2. Process in Flask:**
```python
# app.py
test_results = code_executor.test_project(...)
# Process new_metric
```

---

## Performance Metrics

### Generation Time Breakdown

```
Analysis:        2-5 seconds  (Claude API)
File Generation: 30-60 sec    (1-2 sec per file × file count)
Config Gen:      1-2 seconds
Testing:         5-10 seconds
Refinement:      30-60 sec per iteration (if needed)
Packaging:       1-2 seconds
───────────────────────────
Total:           1-5 minutes (typical)
```

### Resource Usage

```
Memory:          100-500MB typical
Disk (project):  100KB - 5MB per project
Network:         Depends on Claude API latency
Timeout:         30 seconds per subprocess
```

### Typical Project Stats

```
Files Generated:     5-50
Total Size:          100KB - 5MB
Lines of Code:       500 - 10,000
Dependencies:        1-20
Build Time:          1-3 seconds
Test Time:           3-10 seconds
```

---

## Deployment Notes

### Requirements

- Python 3.8+
- ANTHROPIC_API_KEY environment variable
- 500MB+ disk space for generated projects
- Ports 5000+ available

### Production Checklist

- [ ] Set FLASK_DEBUG=False
- [ ] Set FLASK_ENV=production
- [ ] Use strong SECRET_KEY
- [ ] Run behind Gunicorn/production server
- [ ] Enable HTTPS/SSL
- [ ] Set up log rotation
- [ ] Monitor disk space for generated_projects/
- [ ] Implement session cleanup (old projects)
- [ ] Set up error tracking/monitoring

---

## Conclusion

The Kroosybul AI codebase is designed with:

- **Modularity:** Clear separation of concerns (AI, generation, testing)
- **Extensibility:** Easy to add languages, templates, and features
- **Safety:** Validation-only testing, no code execution
- **Real-time UX:** WebSocket streaming of progress
- **Simplicity:** ~3,000 lines, minimal dependencies

The architecture supports rapid enhancement while maintaining code quality and safety.

