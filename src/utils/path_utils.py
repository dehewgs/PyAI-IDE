"""
Path utilities for PyAI IDE
Handles cross-platform path management and AppData directory setup
"""

import os
import sys
from pathlib import Path


def get_appdata_path(subdir: str = None) -> Path:
    """
    Get the application data directory path for the current platform.
    
    Args:
        subdir: Optional subdirectory within appdata
        
    Returns:
        Path object pointing to the appdata directory
    """
    # Determine platform-specific appdata directory
    if sys.platform == 'win32':
        # Windows: %APPDATA%/PyAI-IDE
        appdata = Path(os.environ.get('APPDATA', Path.home() / 'AppData' / 'Roaming'))
    elif sys.platform == 'darwin':
        # macOS: ~/Library/Application Support/PyAI-IDE
        appdata = Path.home() / 'Library' / 'Application Support'
    else:
        # Linux: ~/.config/PyAI-IDE
        appdata = Path.home() / '.config'
    
    # Create PyAI-IDE directory
    appdata = appdata / 'PyAI-IDE'
    
    # Add subdirectory if specified
    if subdir:
        appdata = appdata / subdir
    
    return appdata


def ensure_dir_exists(path: Path) -> Path:
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        path: Path to the directory
        
    Returns:
        The path object
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_project_dir() -> Path:
    """Get the projects directory"""
    return ensure_dir_exists(get_appdata_path('projects'))


def get_models_dir() -> Path:
    """Get the models cache directory"""
    return ensure_dir_exists(get_appdata_path('models'))


def get_themes_dir() -> Path:
    """Get the themes directory"""
    return ensure_dir_exists(get_appdata_path('themes'))


def get_cache_dir() -> Path:
    """Get the cache directory"""
    return ensure_dir_exists(get_appdata_path('cache'))


def get_config_file() -> Path:
    """Get the configuration file path"""
    config_dir = ensure_dir_exists(get_appdata_path())
    return config_dir / 'config.json'


def get_logs_dir() -> Path:
    """Get the logs directory"""
    return ensure_dir_exists(get_appdata_path('logs'))
