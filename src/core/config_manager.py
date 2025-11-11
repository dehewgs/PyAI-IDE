"""
Configuration manager for PyAI IDE
Handles loading, saving, and managing application configuration
"""

from pathlib import Path
from typing import Any, Dict, Optional

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
        self.config_file = get_config_file()
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default"""
        if self.config_file.exists():
            config = load_json(self.config_file)
            # Merge with defaults to ensure all keys exist
            return self._merge_configs(self.DEFAULT_CONFIG.copy(), config)
        else:
            # Save default config
            self.save()
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
        return get_nested(self.config, key, default)
    
    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value using dot notation.
        
        Args:
            key: Configuration key (e.g., 'github.token')
            value: Value to set
        """
        set_nested(self.config, key, value)
    
    def save(self) -> bool:
        """
        Save configuration to file.
        
        Returns:
            True if successful, False otherwise
        """
        return save_json(self.config_file, self.config)
    
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
