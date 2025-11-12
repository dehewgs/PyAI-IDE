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
        self.theme_config = ThemeConfig("dark")
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
        # Create new ThemeConfig with the theme name
        self.theme_config = ThemeConfig(theme_name)
        
        # Apply stylesheet to app
        stylesheet = self._generate_stylesheet()
        app.setStyleSheet(stylesheet)
        
        # Emit signals
        self.theme_changed.emit(theme_name)
        self.colors_changed.emit(self.theme_config.get_all_colors())
        
        # Update all registered components
        for component in self.registered_components:
            if hasattr(component, '_apply_theme'):
                component._apply_theme()
            if hasattr(component, 'set_theme'):
                is_dark = theme_name == "dark"
                component.set_theme(is_dark)
    
    def _generate_stylesheet(self) -> str:
        """Generate QSS stylesheet from theme config
        
        Returns:
            QSS stylesheet string
        """
        if not self.theme_config:
            return ""
        
        ui_colors = self.theme_config.ui_colors
        colors = self.theme_config.colors
        
        stylesheet = f"""
            QMainWindow {{
                background-color: {ui_colors.get('menu_background', '#1e1e1e')};
                color: {ui_colors.get('menu_foreground', '#d4d4d4')};
            }}
            QMenuBar {{
                background-color: {ui_colors.get('menu_background', '#2d2d2d')};
                color: {ui_colors.get('menu_foreground', '#d4d4d4')};
                border-bottom: 1px solid {colors.get('border', '#3e3e3e')};
            }}
            QMenuBar::item:selected {{
                background-color: {ui_colors.get('menu_selected', '#0e639c')};
            }}
            QMenu {{
                background-color: {ui_colors.get('menu_background', '#2d2d2d')};
                color: {ui_colors.get('menu_foreground', '#d4d4d4')};
                border: 1px solid {colors.get('border', '#3e3e3e')};
            }}
            QMenu::item:selected {{
                background-color: {ui_colors.get('menu_selected', '#0e639c')};
            }}
            QPushButton {{
                background-color: {ui_colors.get('button_background', '#0e639c')};
                color: {ui_colors.get('button_foreground', '#d4d4d4')};
                border: none;
                padding: 5px;
                border-radius: 3px;
            }}
            QPushButton:hover {{
                background-color: {colors.get('primary', '#0e639c')};
                opacity: 0.8;
            }}
            QPushButton:pressed {{
                background-color: {ui_colors.get('button_pressed', '#0d5a96')};
            }}
            QLineEdit, QTextEdit, QPlainTextEdit {{
                background-color: {ui_colors.get('input_background', '#252526')};
                color: {ui_colors.get('input_foreground', '#d4d4d4')};
                border: 1px solid {ui_colors.get('input_border', '#3e3e3e')};
                padding: 3px;
            }}
            QTabWidget {{
                background-color: {ui_colors.get('tab_background', '#1e1e1e')};
                color: {ui_colors.get('tab_foreground', '#d4d4d4')};
            }}
            QTabBar::tab {{
                background-color: {ui_colors.get('tab_background', '#2d2d2d')};
                color: {ui_colors.get('tab_foreground', '#d4d4d4')};
                padding: 5px 15px;
                border: 1px solid {colors.get('border', '#3e3e3e')};
            }}
            QTabBar::tab:selected {{
                background-color: {ui_colors.get('tab_selected', '#1e1e1e')};
                border-bottom: 2px solid {colors.get('primary', '#0e639c')};
            }}
            QStatusBar {{
                background-color: {ui_colors.get('status_background', '#2d2d2d')};
                color: {ui_colors.get('status_foreground', '#d4d4d4')};
                border-top: 1px solid {colors.get('border', '#3e3e3e')};
            }}
            QProgressBar {{
                background-color: {ui_colors.get('input_background', '#252526')};
                border: 1px solid {colors.get('border', '#3e3e3e')};
                border-radius: 3px;
            }}
            QProgressBar::chunk {{
                background-color: {colors.get('primary', '#0e639c')};
            }}
            QScrollBar:vertical {{
                background-color: {ui_colors.get('scrollbar_background', '#1e1e1e')};
                width: 12px;
                border: none;
            }}
            QScrollBar::handle:vertical {{
                background-color: {ui_colors.get('scrollbar_handle', '#464647')};
                border-radius: 6px;
                min-height: 20px;
            }}
            QScrollBar::handle:vertical:hover {{
                background-color: {ui_colors.get('scrollbar_handle_hover', '#5a5a5a')};
            }}
            QScrollBar:horizontal {{
                background-color: {ui_colors.get('scrollbar_background', '#1e1e1e')};
                height: 12px;
                border: none;
            }}
            QScrollBar::handle:horizontal {{
                background-color: {ui_colors.get('scrollbar_handle', '#464647')};
                border-radius: 6px;
                min-width: 20px;
            }}
            QScrollBar::handle:horizontal:hover {{
                background-color: {ui_colors.get('scrollbar_handle_hover', '#5a5a5a')};
            }}
            QLabel {{
                color: {ui_colors.get('label_foreground', '#d4d4d4')};
            }}
            QGroupBox {{
                color: {ui_colors.get('label_foreground', '#d4d4d4')};
                border: 1px solid {colors.get('border', '#3e3e3e')};
                border-radius: 3px;
                margin-top: 10px;
                padding-top: 10px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px 0 3px;
            }}
        """
        
        return stylesheet
    
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
