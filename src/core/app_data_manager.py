"""
AppData Manager for PyAI IDE
Handles user data persistence, configuration, and project metadata
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional
from utils.logger import logger


class AppDataManager:
    """Manages application data, configuration, and user preferences"""
    
    def __init__(self):
        """Initialize AppData manager"""
        self.app_data_dir = self._get_app_data_dir()
        self._ensure_app_data_structure()
        self.config_file = self.app_data_dir / "config.json"
        self.shortcuts_file = self.app_data_dir / "shortcuts.json"
        self.projects_file = self.app_data_dir / "projects.json"
        self.themes_dir = self.app_data_dir / "themes"
        self.plugins_dir = self.app_data_dir / "plugins"
        
        # Load existing config
        self.config = self._load_config()
        self.shortcuts = self._load_shortcuts()
        self.projects = self._load_projects()
    
    def _get_app_data_dir(self) -> Path:
        """Get or create AppData directory based on OS"""
        if os.name == 'nt':  # Windows
            app_data = Path(os.environ.get('APPDATA', Path.home() / 'AppData' / 'Roaming'))
        else:  # Linux/macOS
            app_data = Path.home() / '.config'
        
        app_data_dir = app_data / 'PyAI-IDE'
        return app_data_dir
    
    def _ensure_app_data_structure(self):
        """Create AppData directory structure if it doesn't exist"""
        try:
            # Create main directory
            self.app_data_dir.mkdir(parents=True, exist_ok=True)
            
            # Create subdirectories
            subdirs = ['themes', 'plugins', 'projects', 'backups', 'logs']
            for subdir in subdirs:
                (self.app_data_dir / subdir).mkdir(exist_ok=True)
            
            logger.info(f"AppData directory initialized at: {self.app_data_dir}")
        except Exception as e:
            logger.error(f"Failed to create AppData structure: {e}")
            raise
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to load config: {e}")
                return self._get_default_config()
        else:
            config = self._get_default_config()
            self.save_config(config)
            return config
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            'theme': 'dark',
            'auto_save': True,
            'auto_save_interval': 30000,  # milliseconds
            'font_size': 12,
            'font_family': 'Courier New',
            'tab_size': 4,
            'use_spaces': True,
            'word_wrap': False,
            'show_line_numbers': True,
            'show_minimap': True,
            'recent_projects': [],
            'last_project': None,
            'window_geometry': None,
            'window_state': None,
        }
    
    def _load_shortcuts(self) -> Dict[str, str]:
        """Load keyboard shortcuts from file or create default"""
        if self.shortcuts_file.exists():
            try:
                with open(self.shortcuts_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to load shortcuts: {e}")
                return self._get_default_shortcuts()
        else:
            shortcuts = self._get_default_shortcuts()
            self.save_shortcuts(shortcuts)
            return shortcuts
    
    def _get_default_shortcuts(self) -> Dict[str, str]:
        """Get default keyboard shortcuts"""
        return {
            'new_file': 'Ctrl+N',
            'open_project': 'Ctrl+O',
            'save_file': 'Ctrl+S',
            'save_all': 'Ctrl+Shift+S',
            'quick_search': 'Ctrl+P',
            'toggle_comment': 'Ctrl+/',
            'global_search': 'Ctrl+Shift+F',
            'toggle_project_tree': 'Ctrl+B',
            'run_project': 'Ctrl+Shift+R',
            'undo': 'Ctrl+Z',
            'redo': 'Ctrl+Y',
            'cut': 'Ctrl+X',
            'copy': 'Ctrl+C',
            'paste': 'Ctrl+V',
            'find': 'Ctrl+F',
            'replace': 'Ctrl+H',
            'close_tab': 'Ctrl+W',
            'next_tab': 'Ctrl+Tab',
            'prev_tab': 'Ctrl+Shift+Tab',
        }
    
    def _load_projects(self) -> Dict[str, Any]:
        """Load projects metadata from file"""
        if self.projects_file.exists():
            try:
                with open(self.projects_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to load projects: {e}")
                return {'projects': []}
        else:
            return {'projects': []}
    
    def save_config(self, config: Dict[str, Any]):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
            self.config = config
            logger.info("Configuration saved")
        except Exception as e:
            logger.error(f"Failed to save config: {e}")
    
    def save_shortcuts(self, shortcuts: Dict[str, str]):
        """Save shortcuts to file"""
        try:
            with open(self.shortcuts_file, 'w') as f:
                json.dump(shortcuts, f, indent=2)
            self.shortcuts = shortcuts
            logger.info("Shortcuts saved")
        except Exception as e:
            logger.error(f"Failed to save shortcuts: {e}")
    
    def save_projects(self, projects: Dict[str, Any]):
        """Save projects metadata to file"""
        try:
            with open(self.projects_file, 'w') as f:
                json.dump(projects, f, indent=2)
            self.projects = projects
            logger.info("Projects saved")
        except Exception as e:
            logger.error(f"Failed to save projects: {e}")
    
    def add_recent_project(self, project_path: str):
        """Add project to recent projects list"""
        recent = self.config.get('recent_projects', [])
        
        # Remove if already exists
        if project_path in recent:
            recent.remove(project_path)
        
        # Add to front
        recent.insert(0, project_path)
        
        # Keep only last 10
        recent = recent[:10]
        
        self.config['recent_projects'] = recent
        self.config['last_project'] = project_path
        self.save_config(self.config)
    
    def get_recent_projects(self) -> list:
        """Get list of recent projects"""
        return self.config.get('recent_projects', [])
    
    def get_config_value(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self.config.get(key, default)
    
    def set_config_value(self, key: str, value: Any):
        """Set configuration value"""
        self.config[key] = value
        self.save_config(self.config)
    
    def get_shortcut(self, action: str) -> Optional[str]:
        """Get keyboard shortcut for action"""
        return self.shortcuts.get(action)
    
    def set_shortcut(self, action: str, shortcut: str):
        """Set keyboard shortcut for action"""
        self.shortcuts[action] = shortcut
        self.save_shortcuts(self.shortcuts)
    
    def get_app_data_path(self) -> Path:
        """Get AppData directory path"""
        return self.app_data_dir
    
    def get_app_data_dir(self) -> Path:
        """Alias for get_app_data_path for backward compatibility"""
        return self.get_app_data_path()
    
    def get_themes_path(self) -> Path:
        """Get themes directory path"""
        return self.themes_dir
    
    def get_plugins_path(self) -> Path:
        """Get plugins directory path"""
        return self.plugins_dir
