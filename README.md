# PyAI IDE

A lightweight, fully-featured Python IDE with integrated HuggingFace and GitHub support, built with PyQt5.

## Features

### Core IDE Features
- **Multi-file Editor**: Tabbed interface for editing multiple Python files
- **Syntax Highlighting**: Full Python syntax highlighting with Pygments
- **Project Management**: Organize and manage Python projects
- **Console Output**: Real-time console for script execution and debugging
- **Dark/Light Themes**: Customizable UI themes

### AI Integration
- **HuggingFace Models**: Load and run inference with HuggingFace models
- **Local & API Inference**: Support for both local model execution and API-based inference
- **Model Management**: Easy model loading, unloading, and switching
- **Model Search**: Search and discover models from HuggingFace Hub

### GitHub Integration
- **Repository Management**: Create, clone, and manage GitHub repositories
- **Authentication**: Secure GitHub token-based authentication
- **Git Operations**: Push, pull, and commit changes directly from the IDE
- **Issue & PR Management**: Create issues and pull requests
- **Repository Browser**: Browse and manage your repositories

### Plugin System
- **Extensible Architecture**: Create custom plugins to extend functionality
- **Hook System**: Register callbacks for various application events
- **Plugin Manager**: Enable/disable plugins at runtime
- **Easy Development**: Simple plugin API for developers

## Installation

### Requirements
- Python 3.8 or higher
- Windows, macOS, or Linux

### Quick Start

#### Windows
Simply run the launcher from the project root:
```bash
Launcher.bat
```

The launcher will:
1. Check for Python installation
2. Create a virtual environment (if needed)
3. Install all dependencies
4. Launch the application

#### macOS/Linux
```bash
python launcher.py
```

Or create a shell script launcher:
```bash
#!/bin/bash
cd "$(dirname "$0")"
python launcher.py
```

### Manual Installation

If you prefer manual setup:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python launcher.py
```

## Usage

### Starting the IDE

**Windows:**
```bash
Launcher.bat
```

**macOS/Linux:**
```bash
python launcher.py
```

### Basic Workflow

1. **Create a Project**: File → New Project
2. **Write Code**: Use the editor tabs to write Python code
3. **Load AI Models**: AI → Load Model (requires HuggingFace token)
4. **Connect GitHub**: GitHub → Connect Account (requires GitHub token)
5. **Run Code**: Execute Python scripts and view output in console

### Configuration

Configuration is stored in your platform's appdata directory:

- **Windows**: `%APPDATA%\PyAI-IDE\config.json`
- **macOS**: `~/Library/Application Support/PyAI-IDE/config.json`
- **Linux**: `~/.config/PyAI-IDE/config.json`

### Setting Up Tokens

#### GitHub Token
1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Create a new token with `repo` and `user` scopes
3. In PyAI IDE: GitHub → Connect Account
4. Paste your token

#### HuggingFace Token
1. Go to [HuggingFace Settings](https://huggingface.co/settings/tokens)
2. Create a new token with read access
3. In PyAI IDE: AI → Model Manager
4. Enter your token in settings

## Project Structure

```
PyAI-IDE/
├── Launcher.bat              # Windows launcher
├── launcher.py               # Cross-platform launcher
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── TECHNICAL_DESIGN.md       # Technical documentation
├── src/
│   ├── main.py              # Application entry point
│   ├── core/                # Core systems
│   │   ├── plugin_system.py # Plugin architecture
│   │   ├── config_manager.py # Configuration management
│   │   └── event_system.py  # Event handling
│   ├── services/            # External service integrations
│   │   ├── github_service.py # GitHub API wrapper
│   │   └── huggingface_service.py # HuggingFace API wrapper
│   ├── ui/                  # User interface
│   │   ├── main_window.py   # Main application window
│   │   ├── editor/          # Editor components
│   │   ├── panels/          # UI panels
│   │   ├── dialogs/         # Dialog windows
│   │   └── styles/          # Stylesheets
│   ├── plugins/             # Plugin directory
│   └── utils/               # Utility functions
│       ├── path_utils.py    # Path management
│       ├── config_utils.py  # Config file operations
│       └── validators.py    # Input validation
├── tests/                   # Unit tests
└── appdata/                 # Application data (created at runtime)
    ├── projects/            # User projects
    ├── models/              # Cached models
    ├── themes/              # Custom themes
    └── config.json          # Configuration file
```

## Creating Plugins

Plugins extend PyAI IDE functionality. Here's a simple example:

```python
from core.plugin_system import BasePlugin, PluginHook

class MyPlugin(BasePlugin):
    def __init__(self):
        super().__init__("My Plugin", "1.0.0")
    
    def initialize(self) -> bool:
        """Called when plugin is loaded"""
        print("Plugin initialized!")
        self.register_hook(PluginHook.ON_STARTUP, self.on_startup)
        return True
    
    def shutdown(self) -> bool:
        """Called when plugin is unloaded"""
        print("Plugin shutdown!")
        return True
    
    def on_startup(self):
        """Called on application startup"""
        print("Application started!")
```

Save as `my_plugin.py` in the plugins directory, then load it through the Plugin Manager.

## API Reference

### ConfigManager
```python
from core.config_manager import ConfigManager

config = ConfigManager()

# Get configuration value
theme = config.get("app.theme", "dark")

# Set configuration value
config.set("app.theme", "light")

# Save to file
config.save()
```

### GitHubService
```python
from services.github_service import GitHubService

github = GitHubService()

# Authenticate
success, message = github.set_token("ghp_xxxxxxxxxxxx")

# Create repository
success, url = github.create_repository("my-repo", "My Repository")

# List repositories
repos = github.list_repositories()
```

### HuggingFaceService
```python
from services.huggingface_service import HuggingFaceService

hf = HuggingFaceService()

# Set token
success, message = hf.set_token("hf_xxxxxxxxxxxx")

# Load model
success, message = hf.load_model("gpt2")

# Run inference
success, result = hf.infer("gpt2", "Hello, world!")
```

### EventSystem
```python
from core.event_system import EventSystem

events = EventSystem()

# Subscribe to event
def on_file_saved(filename):
    print(f"File saved: {filename}")

listener = events.subscribe("file_saved", on_file_saved)

# Emit event
events.emit("file_saved", "main.py")

# Unsubscribe
events.unsubscribe(listener)
```

## Troubleshooting

### Python Not Found
Ensure Python 3.8+ is installed and in your PATH. Download from [python.org](https://www.python.org)

### Dependencies Installation Fails
Try updating pip:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### HuggingFace Model Loading Fails
- Ensure you have enough disk space for model caching
- Check your internet connection
- Verify your HuggingFace token is valid

### GitHub Authentication Fails
- Verify your GitHub token is valid
- Check that the token has appropriate scopes (`repo`, `user`)
- Ensure you have internet connectivity

## Development

### Running Tests
```bash
pytest tests/
```

### Code Style
```bash
black src/
flake8 src/
mypy src/
```

### Building Distribution
```bash
# Create executable (Windows)
pyinstaller --onefile launcher.py

# Create app bundle (macOS)
py2app launcher.py
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - See LICENSE file for details

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check the [Technical Design Document](TECHNICAL_DESIGN.md)
- Review the [API Reference](#api-reference)

## Roadmap

- [ ] Advanced code completion with AI
- [ ] Integrated debugger
- [ ] Database management tools
- [ ] Docker integration
- [ ] Remote development support
- [ ] Collaborative editing
- [ ] Custom theme editor
- [ ] Performance profiler

## Acknowledgments

Built with:
- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/) - GUI Framework
- [PyGithub](https://github.com/PyGithub/PyGithub) - GitHub API
- [HuggingFace Hub](https://github.com/huggingface/huggingface_hub) - Model Management
- [Transformers](https://github.com/huggingface/transformers) - NLP Models
- [Pygments](https://pygments.org/) - Syntax Highlighting

---

**PyAI IDE** - Making Python development smarter with AI
