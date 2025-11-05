# Changelog

All notable changes to Kroosybul AI will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-11-05

### Added
- Initial release of Kroosybul AI
- AI-powered project generation using Claude
- Support for multiple programming languages:
  - Python
  - JavaScript
  - TypeScript
  - Java
  - C++
  - Rust
  - Go
- Real-time chat interface for project description
- WebSocket-based communication
- Automatic code testing and validation
- Iterative code refinement (up to 10 iterations)
- Project templates for:
  - Web applications
  - Games
  - CLI tools
  - APIs
  - Machine Learning projects
  - Desktop applications
- Comprehensive project generation with:
  - Complete file structure
  - Configuration files
  - Documentation (README.md)
  - Dependency management
  - .gitignore files
- Language-specific features:
  - requirements.txt for Python
  - package.json for JavaScript/TypeScript
  - Cargo.toml for Rust
  - go.mod for Go
  - pom.xml for Java
- Code execution sandbox for testing
- Download generated projects as ZIP
- Progress tracking and status updates
- Beautiful, responsive UI with dark theme
- Quick example buttons
- Supported languages display
- Error handling and recovery
- Session management
- Project metadata tracking

### Features
- **Multi-Language Support**: Generate projects in 7+ languages
- **Intelligent Planning**: AI analyzes requirements and creates structured plans
- **Auto-Testing**: Automatically tests generated code for syntax errors
- **Self-Healing**: Iteratively fixes issues until code works
- **Complete Projects**: Generates all necessary files, not just code
- **Production-Ready**: Includes best practices, error handling, and documentation
- **User-Friendly**: Simple chat interface, no technical setup required
- **Extensible**: Easy to add new languages and templates

### Documentation
- Comprehensive README with quick start guide
- Detailed USAGE guide with examples
- Contributing guidelines
- Environment configuration examples
- Run scripts for Windows and Linux/Mac

### Technical Details
- Flask web framework
- Socket.IO for real-time communication
- Anthropic Claude API integration
- RestrictedPython for safe code evaluation
- GitPython for version control integration
- EventLet for async operations
- Modular architecture for easy extension

## [Unreleased]

### Planned Features
- GitHub/GitLab direct integration
- Custom project templates
- Project history and management
- Code preview before download
- Multi-file editing interface
- Collaborative features
- CLI version
- VS Code extension
- More language support (Swift, Kotlin, etc.)
- Advanced testing frameworks
- Docker containerization
- Cloud deployment options

---

For more details, see the [README](README.md) and [USAGE](USAGE.md) guides.
