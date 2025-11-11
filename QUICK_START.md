# PyAI IDE - Quick Start Guide

## Overview

PyAI IDE is a comprehensive Python IDE with AI integration, GitHub support, and HuggingFace model management. This guide will help you get started quickly.

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip or poetry
- Git

### Quick Setup

```bash
# Clone the repository
git clone https://github.com/dehewgs/PyAI-IDE.git
cd PyAI-IDE

# Install dependencies
pip install -r requirements.txt

# Run the application
python3 src/main.py
```

## Running Tests

```bash
# Run comprehensive test suite
python3 test_app.py

# Expected output: 6/7 tests passing
```

## Accessing Logs

### View Real-Time Logs
Logs appear in the application console widget in real-time.

### View Log Files

**Linux/macOS:**
```bash
cat ~/.config/PyAI-IDE/logs/app.log
```

**Windows:**
```cmd
type %APPDATA%\PyAI-IDE\logs\app.log
```

### Log Levels
- **DEBUG** - Detailed debugging information
- **INFO** - General information messages
- **WARNING** - Warning messages
- **ERROR** - Error messages
- **CRITICAL** - Critical error messages

## Using the Logger in Your Code

```python
from utils.logger import get_logger
from pathlib import Path

# Initialize logger
logger = get_logger("MyModule", log_file=Path("my_app.log"))

# Log messages
logger.debug("Debug information")
logger.info("Information message")
logger.warning("Warning message")
logger.error("Error message")
logger.critical("Critical message")

# Log exceptions
try:
    # Your code here
    pass
except Exception as e:
    logger.exception("Operation failed", e)
```

## Core Features

### 1. File Management
- New Project
- Open Project
- Save
- Save As
- Exit

### 2. Editing
- Undo
- Redo
- Cut
- Copy
- Paste

### 3. View Options
- Toggle Console
- Toggle Project Tree

### 4. Tools
- Settings
- Plugin Manager

### 5. GitHub Integration
- Connect Account
- Create Repository
- Clone Repository

### 6. AI Features
- Load Model
- Run Inference
- Model Manager

### 7. Help
- Documentation
- About

## Configuration

Configuration is stored in:
- **Linux/macOS:** `~/.config/PyAI-IDE/config.json`
- **Windows:** `%APPDATA%\PyAI-IDE\config.json`

### Common Settings

```python
from core.config_manager import ConfigManager

config = ConfigManager()

# Get a setting
theme = config.get("app.theme", "dark")

# Set a setting
config.set("app.theme", "light")

# Save configuration
config.save()
```

## Debugging Tips

### 1. Check the Console Widget
The application console shows real-time logging output with color-coded messages.

### 2. Review Log Files
Log files contain complete history with timestamps and full exception tracebacks.

### 3. Use Debug Level Logging
Set log level to DEBUG for detailed operation information:

```python
logger.debug("Detailed debugging information")
```

### 4. Exception Logging
Always log exceptions with full context:

```python
try:
    risky_operation()
except Exception as e:
    logger.exception("Operation failed", e)
```

## Project Structure

```
PyAI-IDE/
├── src/
│   ├── main.py                    # Entry point
│   ├── core/
│   │   ├── config_manager.py      # Configuration management
│   │   ├── event_system.py        # Event handling
│   │   └── plugin_system.py       # Plugin architecture
│   ├── services/
│   │   ├── github_service.py      # GitHub integration
│   │   └── huggingface_service.py # HuggingFace integration
│   ├── ui/
│   │   └── main_window.py         # Main UI window
│   └── utils/
│       ├── logger.py              # Logging system
│       ├── path_utils.py          # Path utilities
│       ├── config_utils.py        # Config utilities
│       └── validators.py          # Input validation
├── test_app.py                    # Test suite
├── requirements.txt               # Dependencies
├── README.md                      # Project documentation
├── IMPROVEMENTS.md                # Improvements documentation
├── COMPLETION_SUMMARY.md          # Completion summary
├── FINAL_REPORT.txt               # Final report
└── QUICK_START.md                 # This file
```

## Common Tasks

### Adding a New Feature

1. Create your feature in the appropriate module
2. Add logging at key points:
   ```python
   logger.info("Feature started")
   logger.debug("Step completed")
   logger.info("Feature completed successfully")
   ```
3. Add error handling:
   ```python
   try:
       # Your code
   except Exception as e:
       logger.error(f"Feature failed: {e}")
       logger.exception("Feature error", e)
   ```
4. Test your feature
5. Commit with descriptive message

### Debugging an Issue

1. Check the console widget for error messages
2. Review the log file for detailed information
3. Look for exception tracebacks
4. Add debug logging to narrow down the issue
5. Run tests to verify the fix

### Adding a New Service

1. Create a new file in `src/services/`
2. Implement your service class
3. Add logging throughout
4. Add error handling
5. Create tests in `test_app.py`
6. Document the service

## Troubleshooting

### Application Won't Start
1. Check Python version (3.8+)
2. Verify all dependencies installed: `pip install -r requirements.txt`
3. Check log file for error details
4. Ensure no port conflicts

### Buttons Not Responding
1. Check console for error messages
2. Verify signal/slot connections in main_window.py
3. Check log file for exceptions
4. Restart the application

### Configuration Issues
1. Check config file location
2. Verify JSON syntax in config file
3. Delete config file to reset to defaults
4. Check log file for config errors

### Logging Issues
1. Verify log directory exists
2. Check file permissions
3. Ensure disk space available
4. Check log file path in error messages

## Performance Tips

1. **Use lazy loading** for services
2. **Cache frequently accessed data** in ConfigManager
3. **Use WorkerThread** for long-running operations
4. **Limit log entries** to 10,000 in memory
5. **Archive old log files** periodically

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes with proper logging
4. Add tests for new features
5. Commit with descriptive messages
6. Push to your fork
7. Create a pull request

## Resources

- **Repository:** https://github.com/dehewgs/PyAI-IDE
- **Documentation:** See README.md, IMPROVEMENTS.md, COMPLETION_SUMMARY.md
- **Issues:** Report on GitHub
- **Logs:** Check ~/.config/PyAI-IDE/logs/

## Support

For issues or questions:
1. Check the log files for error details
2. Review the documentation
3. Check GitHub issues
4. Create a new issue with log file contents

## Next Steps

1. ✅ Install and run the application
2. ✅ Run the test suite
3. ✅ Explore the UI and features
4. ✅ Check the logging system
5. ✅ Review the code structure
6. ✅ Start developing new features

---

**Last Updated:** November 11, 2025
**Status:** Production Ready
