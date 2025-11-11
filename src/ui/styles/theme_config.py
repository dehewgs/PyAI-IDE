"""
Theme Configuration System for PyAI IDE
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from utils.logger import logger


class ThemeConfig:
    """Manages theme configuration and color palettes"""
    
    def __init__(self, theme_id: str = "dark"):
        """Initialize theme configuration
        
        Args:
            theme_id: Theme identifier (dark, light, etc.)
        """
        self.theme_id = theme_id
        self.config: Dict[str, Any] = {}
        self.colors: Dict[str, str] = {}
        self.editor_colors: Dict[str, str] = {}
        self.console_colors: Dict[str, str] = {}
        self.ui_colors: Dict[str, str] = {}
        
        self._load_theme()
    
    def _load_theme(self) -> None:
        """Load theme configuration from JSON file"""
        theme_dir = Path(__file__).parent / "themes"
        theme_file = theme_dir / f"{self.theme_id}.json"
        
        if not theme_file.exists():
            logger.warning(f"Theme file not found: {theme_file}, using defaults")
            self._set_defaults()
            return
        
        try:
            with open(theme_file, 'r') as f:
                self.config = json.load(f)
            
            self.colors = self.config.get("colors", {})
            self.editor_colors = self.config.get("editor", {})
            self.console_colors = self.config.get("console", {})
            self.ui_colors = self.config.get("ui", {})
            
            logger.info(f"Theme loaded: {self.config.get('name', self.theme_id)}")
        except Exception as e:
            logger.error(f"Error loading theme: {e}")
            self._set_defaults()
    
    def _set_defaults(self) -> None:
        """Set default theme colors"""
        if self.theme_id == "light":
            self.colors = {
                "primary": "#0e639c",
                "background": "#ffffff",
                "foreground": "#333333",
                "border": "#cccccc",
            }
        else:
            self.colors = {
                "primary": "#0e639c",
                "background": "#1e1e1e",
                "foreground": "#d4d4d4",
                "border": "#3e3e3e",
            }
    
    def get_color(self, key: str, default: str = "#000000") -> str:
        """Get color by key
        
        Args:
            key: Color key
            default: Default color if not found
            
        Returns:
            Color hex value
        """
        return self.colors.get(key, default)
    
    def get_editor_color(self, key: str, default: str = "#000000") -> str:
        """Get editor color by key
        
        Args:
            key: Color key
            default: Default color if not found
            
        Returns:
            Color hex value
        """
        return self.editor_colors.get(key, default)
    
    def get_console_color(self, key: str, default: str = "#000000") -> str:
        """Get console color by key
        
        Args:
            key: Color key
            default: Default color if not found
            
        Returns:
            Color hex value
        """
        return self.console_colors.get(key, default)
    
    def get_ui_color(self, key: str, default: str = "#000000") -> str:
        """Get UI color by key
        
        Args:
            key: Color key
            default: Default color if not found
            
        Returns:
            Color hex value
        """
        return self.ui_colors.get(key, default)
    
    def get_all_colors(self) -> Dict[str, str]:
        """Get all colors
        
        Returns:
            Dictionary of all colors
        """
        return {
            **self.colors,
            **self.editor_colors,
            **self.console_colors,
            **self.ui_colors,
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert theme to dictionary
        
        Returns:
            Theme configuration dictionary
        """
        return self.config
