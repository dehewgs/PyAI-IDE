"""
Enhanced Theme Manager for PyAI IDE with Palette Support
"""

from PyQt5.QtCore import QObject, pyqtSignal
from typing import Dict, List, Callable, Optional
from utils.logger import logger
from ui.styles.theme_config import ThemeConfig


class EnhancedThemeManager(QObject):
    """Enhanced theme manager with palette and component support"""
    
    # Signals
    theme_changed = pyqtSignal(str)  # theme_id
    colors_changed = pyqtSignal(dict)  # colors dict
    
    def __init__(self):
        """Initialize enhanced theme manager"""
        super().__init__()
        self.current_theme_id = "dark"
        self.current_config: Optional[ThemeConfig] = None
        self.registered_components: Dict[str, List[Callable]] = {}
        
        self._load_theme("dark")
        logger.info("Enhanced Theme Manager initialized")
    
    def _load_theme(self, theme_id: str) -> None:
        """Load theme configuration
        
        Args:
            theme_id: Theme identifier
        """
        try:
            self.current_config = ThemeConfig(theme_id)
            self.current_theme_id = theme_id
            logger.info(f"Theme loaded: {theme_id}")
        except Exception as e:
            logger.error(f"Error loading theme: {e}")
            if theme_id != "dark":
                self._load_theme("dark")
    
    def register_component(self, component_id: str, update_callback: Callable) -> None:
        """Register a component for theme updates
        
        Args:
            component_id: Unique component identifier
            update_callback: Function to call when theme changes
        """
        if component_id not in self.registered_components:
            self.registered_components[component_id] = []
        
        self.registered_components[component_id].append(update_callback)
        logger.debug(f"Component registered: {component_id}")
    
    def unregister_component(self, component_id: str) -> None:
        """Unregister a component
        
        Args:
            component_id: Component identifier
        """
        if component_id in self.registered_components:
            del self.registered_components[component_id]
            logger.debug(f"Component unregistered: {component_id}")
    
    def set_theme(self, app, theme_id: str) -> None:
        """Set application theme
        
        Args:
            app: QApplication instance
            theme_id: Theme identifier
        """
        self._load_theme(theme_id)
        
        # Apply stylesheet to app
        stylesheet = self._generate_stylesheet()
        app.setStyleSheet(stylesheet)
        
        # Notify registered components
        self._notify_components()
        
        # Emit signals
        self.theme_changed.emit(theme_id)
        self.colors_changed.emit(self.current_config.get_all_colors())
        
        logger.info(f"Theme changed to: {theme_id}")
    
    def _notify_components(self) -> None:
        """Notify all registered components of theme change"""
        for component_id, callbacks in self.registered_components.items():
            for callback in callbacks:
                try:
                    callback(self.current_config)
                except Exception as e:
                    logger.error(f"Error updating component {component_id}: {e}")
    
    def _generate_stylesheet(self) -> str:
        """Generate QSS stylesheet from theme config
        
        Returns:
            QSS stylesheet string
        """
        if not self.current_config:
            return ""
        
        ui_colors = self.current_config.ui_colors
        
        stylesheet = f"""
            QMainWindow {{
                background-color: {ui_colors.get('menu_background', '#1e1e1e')};
                color: {ui_colors.get('menu_foreground', '#d4d4d4')};
            }}
            QMenuBar {{
                background-color: {ui_colors.get('menu_background', '#2d2d2d')};
                color: {ui_colors.get('menu_foreground', '#d4d4d4')};
                border-bottom: 1px solid {self.current_config.get_color('border', '#3e3e3e')};
            }}
            QMenuBar::item:selected {{
                background-color: {ui_colors.get('menu_selected', '#0e639c')};
            }}
            QMenu {{
                background-color: {ui_colors.get('menu_background', '#2d2d2d')};
                color: {ui_colors.get('menu_foreground', '#d4d4d4')};
                border: 1px solid {self.current_config.get_color('border', '#3e3e3e')};
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
                background-color: {self.current_config.get_color('primary_hover', '#1177bb')};
            }}
            QPushButton:pressed {{
                background-color: {self.current_config.get_color('primary_pressed', '#0d5a96')};
            }}
            QLineEdit, QTextEdit, QPlainTextEdit {{
                background-color: {ui_colors.get('input_background', '#252526')};
                color: {ui_colors.get('input_foreground', '#d4d4d4')};
                border: 1px solid {ui_colors.get('input_border', '#3e3e3e')};
                padding: 3px;
            }}
            QComboBox {{
                background-color: {ui_colors.get('input_background', '#252526')};
                color: {ui_colors.get('input_foreground', '#d4d4d4')};
                border: 1px solid {ui_colors.get('input_border', '#3e3e3e')};
                padding: 3px;
            }}
            QTreeWidget, QListWidget {{
                background-color: {ui_colors.get('input_background', '#252526')};
                color: {ui_colors.get('input_foreground', '#d4d4d4')};
                border: 1px solid {ui_colors.get('input_border', '#3e3e3e')};
            }}
            QStatusBar {{
                background-color: {ui_colors.get('status_bar_background', '#2d2d2d')};
                color: {ui_colors.get('status_bar_foreground', '#d4d4d4')};
                border-top: 1px solid {self.current_config.get_color('border', '#3e3e3e')};
            }}
            QTabWidget::pane {{
                border: 1px solid {self.current_config.get_color('border', '#3e3e3e')};
            }}
            QTabBar::tab {{
                background-color: {ui_colors.get('tab_background', '#2d2d2d')};
                color: {ui_colors.get('tab_foreground', '#d4d4d4')};
                padding: 5px 15px;
                border: 1px solid {self.current_config.get_color('border', '#3e3e3e')};
            }}
            QTabBar::tab:selected {{
                background-color: {ui_colors.get('tab_selected_background', '#1e1e1e')};
                border-bottom: 2px solid {ui_colors.get('tab_selected_border', '#0e639c')};
            }}
            QDialog {{
                background-color: {self.current_config.get_color('background', '#1e1e1e')};
                color: {self.current_config.get_color('foreground', '#d4d4d4')};
            }}
            QLabel {{
                color: {self.current_config.get_color('foreground', '#d4d4d4')};
            }}
        """
        
        return stylesheet
    
    def get_color(self, key: str, default: str = "#000000") -> str:
        """Get color by key
        
        Args:
            key: Color key
            default: Default color if not found
            
        Returns:
            Color hex value
        """
        if not self.current_config:
            return default
        return self.current_config.get_color(key, default)
    
    def get_editor_color(self, key: str, default: str = "#000000") -> str:
        """Get editor color by key
        
        Args:
            key: Color key
            default: Default color if not found
            
        Returns:
            Color hex value
        """
        if not self.current_config:
            return default
        return self.current_config.get_editor_color(key, default)
    
    def get_console_color(self, key: str, default: str = "#000000") -> str:
        """Get console color by key
        
        Args:
            key: Color key
            default: Default color if not found
            
        Returns:
            Color hex value
        """
        if not self.current_config:
            return default
        return self.current_config.get_console_color(key, default)
    
    def get_ui_color(self, key: str, default: str = "#000000") -> str:
        """Get UI color by key
        
        Args:
            key: Color key
            default: Default color if not found
            
        Returns:
            Color hex value
        """
        if not self.current_config:
            return default
        return self.current_config.get_ui_color(key, default)
    
    def get_current_theme(self) -> str:
        """Get current theme ID
        
        Returns:
            Theme identifier
        """
        return self.current_theme_id
    
    def get_available_themes(self) -> List[str]:
        """Get list of available themes
        
        Returns:
            List of theme identifiers
        """
        return ["dark", "light"]
