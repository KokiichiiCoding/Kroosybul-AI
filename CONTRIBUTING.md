# Contributing to Kroosybul AI

Thank you for your interest in contributing to Kroosybul AI! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Issues

If you find a bug or have a feature request:

1. Check if the issue already exists
2. Create a new issue with:
   - Clear title
   - Detailed description
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - Screenshots if applicable

### Submitting Code

1. **Fork the repository**

2. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the existing code style
   - Add comments for complex logic
   - Update documentation if needed

4. **Test your changes**
   ```bash
   # Run the application
   python app.py

   # Test with various project types
   # Verify the UI works correctly
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add feature: your feature description"
   ```

6. **Push and create a pull request**
   ```bash
   git push origin feature/your-feature-name
   ```

## Development Setup

### Prerequisites

- Python 3.8+
- Node.js (for frontend development)
- Git

### Setup

```bash
# Clone your fork
git clone https://github.com/your-username/fuzzy-broccoli.git
cd fuzzy-broccoli

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
# Add your API key to .env

# Run the application
python app.py
```

## Project Structure

```
fuzzy-broccoli/
├── app.py                  # Main Flask application
├── core/                   # Core modules
│   ├── ai_engine.py       # AI integration
│   ├── project_generator.py # Project generation
│   └── code_executor.py   # Code testing
├── templates/             # HTML templates
│   └── index.html
├── static/                # Frontend assets
│   ├── css/
│   └── js/
├── generated_projects/    # Output directory
└── requirements.txt       # Python dependencies
```

## Areas for Contribution

### High Priority

1. **New Language Support**
   - Add support for more programming languages
   - Implement language-specific testing
   - Add language-specific templates

2. **Project Templates**
   - Create more project templates
   - Add specialized configurations
   - Improve template quality

3. **Testing**
   - Add unit tests
   - Add integration tests
   - Improve code quality checks

4. **Documentation**
   - Improve user guides
   - Add video tutorials
   - Create examples gallery

### Medium Priority

1. **UI Improvements**
   - Better progress visualization
   - Project preview before download
   - Code syntax highlighting
   - Dark/light theme toggle

2. **Features**
   - Project history tracking
   - Save/load project specifications
   - Export to GitHub directly
   - Multi-project management

3. **Performance**
   - Optimize generation speed
   - Implement caching
   - Reduce API calls

### Low Priority

1. **Integrations**
   - GitHub integration
   - GitLab integration
   - VS Code extension
   - CLI version

2. **Advanced Features**
   - Custom templates
   - Plugin system
   - AI model selection
   - Cost estimation

## Code Style

### Python

Follow PEP 8 guidelines:

```python
# Good
def generate_project(name: str, language: str) -> Dict[str, Any]:
    """Generate a new project.

    Args:
        name: Project name
        language: Programming language

    Returns:
        Project information
    """
    # Implementation
    pass

# Use type hints
# Add docstrings
# Keep functions focused
```

### JavaScript

Follow standard JavaScript conventions:

```javascript
// Good
function handleMessage(data) {
    // Use clear variable names
    const messageText = data.message;

    // Add comments for complex logic
    if (messageText.length > 0) {
        sendMessage(messageText);
    }
}

// Use const/let, not var
// Use meaningful names
// Keep functions small
```

### CSS

```css
/* Good */
.chat-container {
    /* Group related properties */
    display: flex;
    flex-direction: column;

    /* Use consistent spacing */
    padding: 20px;
    gap: 10px;

    /* Use CSS variables */
    background: var(--bg-secondary);
}
```

## Adding New Languages

To add support for a new programming language:

1. **Update language_configs in `project_generator.py`**

```python
'kotlin': {
    'extensions': ['.kt'],
    'main_file': 'Main.kt',
    'config_files': ['build.gradle.kts', '.gitignore'],
    'test_command': 'kotlinc'
}
```

2. **Add test function in `code_executor.py`**

```python
def _test_kotlin(self, project_path: Path, metadata: Dict) -> Dict[str, Any]:
    # Implementation
    pass
```

3. **Add config generation in `_generate_config_files`**

```python
elif language == 'kotlin':
    # Generate build.gradle.kts
    # Generate .gitignore
    pass
```

4. **Update UI language list**

Add to `static/js/app.js` and `templates/index.html`

5. **Test thoroughly**

Generate several test projects and verify they work

## Adding Project Templates

1. **Define template in `project_generator.py`**

```python
{
    'id': 'mobile_app',
    'name': 'Mobile App',
    'description': 'Cross-platform mobile application',
    'languages': ['javascript', 'typescript']
}
```

2. **Create template prompts in `ai_engine.py`**

Add specific prompting for this project type

3. **Add example to UI**

Update the example buttons in `index.html`

## Testing Guidelines

### Manual Testing

Before submitting:

1. Test with multiple project types
2. Test with different languages
3. Verify error handling
4. Check UI responsiveness
5. Test on different browsers

### Automated Testing

We're working on adding automated tests. Contributions welcome!

## Documentation

When adding features:

1. Update README.md if needed
2. Update USAGE.md with new capabilities
3. Add inline code comments
4. Update this CONTRIBUTING.md if adding new areas

## Questions?

- Open an issue for questions
- Tag it with "question" label
- We're happy to help!

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn
- Keep discussions on-topic

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Kroosybul AI! 🔥
