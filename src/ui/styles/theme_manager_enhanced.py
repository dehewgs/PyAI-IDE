"""
Enhanced Theme Manager for PyAI IDE
"""

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QColor
from .theme_config import ThemeConfig
import os


class EnhancedThemeManager(QObject):
    """Enhanced theme manager with component registration and signals"""
    
    theme_changed = pyqtSignal(str)
    colors_changed = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.current_theme = "dark"
        self.theme_config = ThemeConfig()
        self.registered_components = []
    
    def register_component(self, component):
        """Register a component for theme updates
        
        Args:
            component: Component with _apply_theme() method
        """
        if component not in self.registered_components:
            self.registered_components.append(component)
    
    def unregister_component(self, component):
        """Unregister a component
        
        Args:
            component: Component to unregister
        """
        if component in self.registered_components:
            self.registered_components.remove(component)
    
    def set_theme(self, app, theme_name):
        """Set application theme
        
        Args:
            app: QApplication instance
            theme_name: Theme identifier (dark, light, etc.)
        """
        self.current_theme = theme_name
        self.theme_config.load_theme(theme_name)
        
        # Emit signals
        self.theme_changed.emit(theme_name)
        self.colors_changed.emit(self.theme_config.colors)
        
        # Update all registered components
        for component in self.registered_components:
            if hasattr(component, '_apply_theme'):
                component._apply_theme()
            if hasattr(component, 'set_theme'):
                is_dark = theme_name == "dark"
                component.set_theme(is_dark)
    
    def get_color(self, color_name, default="#1e1e1e"):
        """Get color from current theme
        
        Args:
            color_name: Color identifier
            default: Default color if not found
            
        Returns:
            Color hex string
        """
        return self.theme_config.get_color(color_name, default)
    
    def get_editor_color(self, color_name, default="#f92672"):
        """Get editor color from current theme
        
        Args:
            color_name: Color identifier
            default: Default color if not found
            
        Returns:
            Color hex string
        """
        return self.theme_config.get_editor_color(color_name, default)
    
    def get_console_color(self, color_name, default="#d4d4d4"):
        """Get console color from current theme
        
        Args:
            color_name: Color identifier
            default: Default color if not found
            
        Returns:
            Color hex string
        """
        return self.theme_config.get_console_color(color_name, default)
    
    def get_ui_color(self, color_name, default="#1e1e1e"):
        """Get UI color from current theme
        
        Args:
            color_name: Color identifier
            default: Default color if not found
            
        Returns:
            Color hex string
        """
        return self.theme_config.get_ui_color(color_name, default)
