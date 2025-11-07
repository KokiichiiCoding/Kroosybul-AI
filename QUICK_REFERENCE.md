# Kroosybul AI - Quick Reference Guide

A fast lookup guide for key files, functions, and integration points.

---

## Key Files Quick Access

| File | Path | Lines | Purpose |
|------|------|-------|---------|
| Flask App | `/home/user/Kroosybul-AI/app.py` | 273 | WebSocket server, API routes, session mgmt |
| AI Engine | `/home/user/Kroosybul-AI/core/ai_engine.py` | 278 | Claude integration, prompting |
| Project Gen | `/home/user/Kroosybul-AI/core/project_generator.py` | 484 | File generation, configs, README |
| Code Executor | `/home/user/Kroosybul-AI/core/code_executor.py` | 417 | Syntax validation, testing |
| HTML UI | `/home/user/Kroosybul-AI/templates/index.html` | 168 | Main interface |
| JS Client | `/home/user/Kroosybul-AI/static/js/app.js` | 409 | WebSocket client, UI interactions |
| CSS Styles | `/home/user/Kroosybul-AI/static/css/style.css` | 556 | Dark theme styling |

---

## Important Classes & Methods

### AIEngine (core/ai_engine.py)

```python
class AIEngine:
    def analyze_project_request(user_message, conversation_history) → Dict
    def generate_file_content(file_info, project_context) → str
    def fix_code_issues(project_info, errors, conversation_history) → Dict[str, str]
    def enhance_project_idea(basic_idea) → str
```

**Usage Example:**
```python
ai_engine = AIEngine()
project_plan = ai_engine.analyze_project_request(
    "Create a Snake game in Python",
    []
)
```

---

### ProjectGenerator (core/project_generator.py)

```python
class ProjectGenerator:
    def generate_project(project_plan, progress_callback=None) → Dict
    def _generate_config_files(project_path, project_plan) → None
    def _generate_readme(project_path, project_plan) → None
    def apply_fixes(project_path, fixes) → None
    def create_zip(project_path) → str
    def get_available_templates() → List[Dict]
```

**Usage Example:**
```python
gen = ProjectGenerator()
result = gen.generate_project(
    project_plan,
    progress_callback=lambda msg: print(msg)
)
```

---

### CodeExecutor (core/code_executor.py)

```python
class CodeExecutor:
    def test_project(project_path) → Dict
    def _test_python(project_path, metadata) → Dict
    def _test_javascript(project_path, metadata) → Dict
    def _test_typescript(project_path, metadata) → Dict
    def _test_rust(project_path, metadata) → Dict
    def _test_go(project_path, metadata) → Dict
    def _test_java(project_path, metadata) → Dict
    def _test_cpp(project_path, metadata) → Dict
    def _test_generic(project_path, metadata) → Dict
```

**Usage Example:**
```python
executor = CodeExecutor()
test_results = executor.test_project("/path/to/project")
# Returns: {success: bool, errors: [], warnings: [], tested_files: int}
```

---

## Flask Routes (app.py)

### HTTP Routes

```python
@app.route('/')
def index()
    # Serve index.html

@app.route('/api/health', methods=['GET'])
def health_check()
    # Returns: {status, timestamp, version}

@app.route('/api/languages', methods=['GET'])
def get_supported_languages()
    # Returns: {languages: [...], templates: [...]}

@app.route('/api/templates', methods=['GET'])
def get_templates()
    # Returns: {templates: [...]}

@app.route('/api/download/<session_id>', methods=['GET'])
def download_project(session_id)
    # Returns: ZIP file
```

### WebSocket Events

```python
@socketio.on('connect')
def handle_connect()
    # Initializes session

@socketio.on('disconnect')
def handle_disconnect()
    # Cleans up session

@socketio.on('message')
def handle_message(data)
    # Main event: data = {'message': str}
    # Orchestrates: analyze → generate → test → [refine] → package
```

---

## Frontend Functions (static/js/app.js)

```javascript
function initializeSocket()          // Establish WebSocket
function sendMessage()                // Send project request
function addUserMessage(text)          // Display user msg
function addAIMessage(text, type)      // Display AI msg
function updateStatus(message, stage)  // Update status bar
function updateProgress(message)       // Update progress bar
function showDownloadModal(projectData) // Show completion modal
function formatText(text)              // Markdown formatting
function escapeHtml(text)              // XSS prevention
function loadSupportedLanguages()      // Fetch from API
```

---

## Configuration Variables

### .env Keys

```bash
ANTHROPIC_API_KEY           # Required: Claude API key
FLASK_ENV                   # development | production
FLASK_DEBUG                 # True | False
SECRET_KEY                  # Random secret for sessions
AI_MODEL                    # claude-sonnet-4-5-20250929 (default)
MAX_TOKENS                  # 8000 (default, per call)
AI_TEMPERATURE              # 0.7 (default, 0-1 range)
MAX_ITERATIONS              # 10 (default, refinement loops)
CODE_TIMEOUT                # 30 (default, seconds)
MAX_FILE_SIZE               # 10485760 (default, 10MB)
ENABLE_SANDBOX              # True (default, security)
SUPPORTED_LANGUAGES         # comma-separated list
GENERATED_PROJECTS_DIR      # generated_projects (default)
MAX_PROJECT_SIZE            # 104857600 (default, 100MB)
HOST                        # 0.0.0.0 (default)
PORT                        # 5000 (default)
```

---

## Data Structures

### Project Plan JSON

```json
{
  "project_name": "string",
  "description": "string",
  "language": "python|javascript|typescript|java|cpp|rust|go",
  "project_type": "web_app|game|api|cli_tool|ml_project|desktop_app",
  "frameworks": ["string", ...],
  "features": ["string", ...],
  "files": [
    {
      "path": "string",
      "purpose": "string",
      "priority": "high|medium|low"
    }
  ],
  "dependencies": ["package>=version", ...],
  "setup_instructions": "string",
  "estimated_complexity": "simple|moderate|complex"
}
```

---

### Test Results JSON

```json
{
  "success": boolean,
  "errors": ["error message", ...],
  "warnings": ["warning message", ...],
  "tested_files": integer
}
```

---

## Environment Setup Quick Commands

```bash
# Clone and setup
git clone <repo>
cd Kroosybul-AI
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Configure
cp .env.example .env
nano .env  # Edit and add ANTHROPIC_API_KEY

# Run
python app.py

# Visit
# http://localhost:5000
```

---

## Adding Features - Checklist

### Add New Language Support
- [ ] Add config to `ProjectGenerator.language_configs`
- [ ] Implement `CodeExecutor._test_newlang()` method
- [ ] Add to `test_commands` dict
- [ ] Update `.env` `SUPPORTED_LANGUAGES`
- [ ] Test file generation and validation

### Add API Endpoint
- [ ] Create `@app.route()` in `app.py`
- [ ] Handle request params and errors
- [ ] Return JSON response
- [ ] Test with curl/Postman

### Add UI Feature
- [ ] Update `templates/index.html` (HTML)
- [ ] Add event listeners in `static/js/app.js`
- [ ] Add styles to `static/css/style.css`
- [ ] Test in browser (Firefox, Chrome)

### Add AI Capability
- [ ] Update prompt in `AIEngine` method
- [ ] Adjust response parsing
- [ ] Add fallback handling
- [ ] Test with real Claude API

---

## Debugging Tips

### Enable Logging
```bash
export FLASK_DEBUG=True
python app.py
```

### Check Active Sessions
```python
# In Python shell with Flask context
from app import active_sessions
print(active_sessions)
```

### Verify AI Responses
```python
# Add debug logging in ai_engine.py
logger.info(f"Raw Claude response: {response_text}")
```

### Test Code Executor
```bash
python -c "
from core.code_executor import CodeExecutor
executor = CodeExecutor()
result = executor.test_project('/path/to/project')
print(result)
"
```

### Monitor WebSocket Events
```javascript
// In browser console
window.CodeForgeAI.socket.on('*', (event, data) => {
    console.log('Event:', event, 'Data:', data);
});
```

---

## Common Issues & Solutions

### Issue: ANTHROPIC_API_KEY not found
**Solution:** Check `.env` file exists and has correct API key
```bash
cat .env | grep ANTHROPIC_API_KEY
```

### Issue: WebSocket connection failed
**Solution:** Ensure Flask is running and CORS is enabled
```python
# Check in app.py:
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")
```

### Issue: Generated code won't compile
**Solution:** Check language is supported and syntax is valid
```python
# Run test manually
from core.code_executor import CodeExecutor
executor = CodeExecutor()
print(executor.test_project('/path'))
```

### Issue: Projects take too long to generate
**Solution:** Check Claude API latency, consider increasing MAX_TOKENS
```bash
# Monitor in logs:
tail -f logs/*.log
```

### Issue: Disk space running out
**Solution:** Clean old generated projects
```bash
# Remove old projects (older than 7 days)
find generated_projects -type d -mtime +7 -exec rm -rf {} \;
```

---

## Performance Optimization Tips

1. **Cache Language Configs**
   - Already done in `ProjectGenerator.__init__`

2. **Optimize Prompts**
   - Keep token count low by being specific
   - Use examples in prompts

3. **Parallel File Generation** (future)
   - Currently sequential, could be parallelized

4. **Incremental Testing** (future)
   - Test files as they're generated

5. **Session Cleanup** (future)
   - Auto-remove sessions older than X hours

---

## Testing Checklist

Before deploying new features:

- [ ] Flask server starts without errors
- [ ] WebSocket connects from browser
- [ ] Can generate simple Python project
- [ ] Can generate JavaScript project
- [ ] Can download generated project
- [ ] Downloaded ZIP extracts correctly
- [ ] Generated code passes syntax checks
- [ ] Error handling works (bad input, API down)
- [ ] UI is responsive on mobile
- [ ] No console JavaScript errors
- [ ] Log output is clean

---

## Database/Persistence Strategy

**Current:** File-based, in-memory sessions
**Limitations:**
- Sessions lost on server restart
- No persistent history
- No usage analytics

**Future Improvements:**
- SQLite for session persistence
- Database for project history
- Analytics/usage tracking

---

## Deployment Preparation

```bash
# 1. Build production config
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=<generate-random-key>

# 2. Install with gunicorn
pip install gunicorn

# 3. Test with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# 4. Set up systemd service (Linux)
# See CONTRIBUTING.md for details

# 5. Monitor
tail -f logs/*.log
curl http://localhost:5000/api/health
```

---

## Contact & Support

- **Documentation:** See ARCHITECTURE.md
- **Usage Guide:** See USAGE.md
- **Contributing:** See CONTRIBUTING.md
- **Issues:** GitHub issues
- **Pull Requests:** GitHub PRs

---

Generated: 2025-11-05  
Version: 1.0.0

