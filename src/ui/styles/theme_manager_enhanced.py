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
        
        # Get safe defaults from theme config
        menu_bg = ui_colors.get('menu_background', colors.get('background', '#1e1e1e'))
        menu_fg = ui_colors.get('menu_foreground', colors.get('foreground', '#d4d4d4'))
        menu_selected = ui_colors.get('menu_selected', colors.get('primary', '#0e639c'))
        button_bg = ui_colors.get('button_background', colors.get('primary', '#0e639c'))
        button_fg = ui_colors.get('button_foreground', colors.get('background', '#ffffff'))
        input_bg = ui_colors.get('input_background', colors.get('background', '#ffffff'))
        input_fg = ui_colors.get('input_foreground', colors.get('foreground', '#333333'))
        input_border = ui_colors.get('input_border', colors.get('border', '#cccccc'))
        # Determine if dark theme based on background color
        is_dark = colors.get('background', '#1e1e1e').lower() in ['#1e1e1e', '#000000', '#0a0a0a']
        
        # Set appropriate defaults based on theme
        light_default_bg = '#f0f0f0'
        dark_default_bg = '#2d2d2d'
        light_default_fg = '#333333'
        dark_default_fg = '#d4d4d4'
        light_default_border = '#cccccc'
        dark_default_border = '#3e3e3e'
        
        default_bg = dark_default_bg if is_dark else light_default_bg
        default_fg = dark_default_fg if is_dark else light_default_fg
        default_border = dark_default_border if is_dark else light_default_border
        
        tab_bg = ui_colors.get('tab_background', colors.get('background_secondary', default_bg))
        tab_fg = ui_colors.get('tab_foreground', colors.get('foreground', default_fg))
        tab_selected_bg = ui_colors.get('tab_selected_background', colors.get('background', default_bg))
        tab_selected_border = ui_colors.get('tab_selected_border', colors.get('primary', '#0e639c'))
        status_bg = ui_colors.get('status_bar_background', colors.get('background_secondary', default_bg))
        status_fg = ui_colors.get('status_bar_foreground', colors.get('foreground', default_fg))
        label_fg = ui_colors.get('label_foreground', colors.get('foreground', default_fg))
        border = colors.get('border', default_border)
        primary = colors.get('primary', '#0e639c')
        primary_hover = colors.get('primary_hover', '#1177bb')
        primary_pressed = colors.get('primary_pressed', '#0d5a96')
        scrollbar_bg = ui_colors.get('scrollbar_background', colors.get('background_secondary', default_bg))
        scrollbar_handle = ui_colors.get('scrollbar_handle', colors.get('border', default_border))
        scrollbar_handle_hover = ui_colors.get('scrollbar_handle_hover', colors.get('foreground_secondary', '#999999'))
        
        stylesheet = f"""
            QMainWindow {{
                background-color: {menu_bg};
                color: {menu_fg};
            }}
            QMenuBar {{
                background-color: {menu_bg};
                color: {menu_fg};
                border-bottom: 1px solid {border};
            }}
            QMenuBar::item:selected {{
                background-color: {menu_selected};
            }}
            QMenu {{
                background-color: {menu_bg};
                color: {menu_fg};
                border: 1px solid {border};
            }}
            QMenu::item:selected {{
                background-color: {menu_selected};
            }}
            QPushButton {{
                background-color: {button_bg};
                color: {button_fg};
                border: none;
                padding: 5px;
                border-radius: 3px;
            }}
            QPushButton:hover {{
                background-color: {primary_hover};
            }}
            QPushButton:pressed {{
                background-color: {primary_pressed};
            }}
            QLineEdit, QTextEdit, QPlainTextEdit {{
                background-color: {input_bg};
                color: {input_fg};
                border: 1px solid {input_border};
                padding: 3px;
            }}
            QTabWidget {{
                background-color: {tab_bg};
                color: {tab_fg};
            }}
            QTabBar::tab {{
                background-color: {tab_bg};
                color: {tab_fg};
                padding: 5px 15px;
                border: 1px solid {border};
            }}
            QTabBar::tab:selected {{
                background-color: {tab_selected_bg};
                border-bottom: 2px solid {tab_selected_border};
            }}
            QStatusBar {{
                background-color: {status_bg};
                color: {status_fg};
                border-top: 1px solid {border};
            }}
            QProgressBar {{
                background-color: {input_bg};
                border: 1px solid {border};
                border-radius: 3px;
            }}
            QProgressBar::chunk {{
                background-color: {primary};
            }}
            QScrollBar:vertical {{
                background-color: {scrollbar_bg};
                width: 12px;
                border: none;
            }}
            QScrollBar::handle:vertical {{
                background-color: {scrollbar_handle};
                border-radius: 6px;
                min-height: 20px;
            }}
            QScrollBar::handle:vertical:hover {{
                background-color: {scrollbar_handle_hover};
            }}
            QScrollBar:horizontal {{
                background-color: {scrollbar_bg};
                height: 12px;
                border: none;
            }}
            QScrollBar::handle:horizontal {{
                background-color: {scrollbar_handle};
                border-radius: 6px;
                min-width: 20px;
            }}
            QScrollBar::handle:horizontal:hover {{
                background-color: {scrollbar_handle_hover};
            }}
            QLabel {{
                color: {label_fg};
            }}
            QGroupBox {{
                color: {label_fg};
                border: 1px solid {border};
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
