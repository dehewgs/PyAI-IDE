"""
Configuration manager for PyAI IDE
Handles loading, saving, and managing application configuration
"""

import sys
from pathlib import Path
from typing import Any, Dict, Optional

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.config_utils import load_json, save_json, get_nested, set_nested
from utils.path_utils import get_config_file


class ConfigManager:
    """
    Manages application configuration with persistent storage
    """
    
    DEFAULT_CONFIG = {
        "app": {
            "theme": "dark",
            "window_width": 1200,
            "window_height": 800,
            "auto_save": True,
            "auto_save_interval": 30,
        },
        "editor": {
            "font_family": "Courier New",
            "font_size": 11,
            "tab_size": 4,
            "use_spaces": True,
            "line_numbers": True,
            "syntax_highlighting": True,
        },
        "github": {
            "token": None,
            "username": None,
            "auto_sync": False,
        },
        "huggingface": {
            "token": None,
            "cache_dir": None,
            "default_model": None,
        },
        "plugins": {
            "enabled": [],
            "disabled": [],
        },
    }
    
    def __init__(self):
        """Initialize config manager"""
        try:
            self.config_file = get_config_file()
            self.config = self._load_config()
        except Exception as e:
            print(f"Warning: Failed to load config: {e}")
            print("Using default configuration")
            self.config = self.DEFAULT_CONFIG.copy()
            self.config_file = None
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default"""
        if self.config_file and self.config_file.exists():
            try:
                config = load_json(self.config_file)
                # Merge with defaults to ensure all keys exist
                return self._merge_configs(self.DEFAULT_CONFIG.copy(), config)
            except Exception as e:
                print(f"Error loading config file: {e}")
                return self.DEFAULT_CONFIG.copy()
        else:
            # Save default config
            try:
                self.save()
            except Exception as e:
                print(f"Warning: Could not save default config: {e}")
            return self.DEFAULT_CONFIG.copy()
    
    def _merge_configs(self, defaults: Dict, custom: Dict) -> Dict:
        """
        Merge custom config with defaults, preserving custom values
        
        Args:
            defaults: Default configuration
            custom: Custom configuration
            
        Returns:
            Merged configuration
        """
        result = defaults.copy()
        
        for key, value in custom.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value
        
        return result
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation.
        
        Args:
            key: Configuration key (e.g., 'github.token')
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        try:
            return get_nested(self.config, key, default)
        except Exception as e:
            print(f"Error getting config key '{key}': {e}")
            return default
    
    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value using dot notation.
        
        Args:
            key: Configuration key (e.g., 'github.token')
            value: Value to set
        """
        try:
            set_nested(self.config, key, value)
        except Exception as e:
            print(f"Error setting config key '{key}': {e}")
    
    def save(self) -> bool:
        """
        Save configuration to file.
        
        Returns:
            True if successful, False otherwise
        """
        if not self.config_file:
            print("Warning: No config file path set")
            return False
        
        try:
            return save_json(self.config_file, self.config)
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def reset_to_defaults(self) -> None:
        """Reset configuration to defaults"""
        self.config = self.DEFAULT_CONFIG.copy()
        self.save()
    
    def get_all(self) -> Dict[str, Any]:
        """Get entire configuration dictionary"""
        return self.config.copy()
    
    def update(self, updates: Dict[str, Any]) -> None:
        """
        Update multiple configuration values.
        
        Args:
            updates: Dictionary of updates
        """
        for key, value in updates.items():
            self.set(key, value)
