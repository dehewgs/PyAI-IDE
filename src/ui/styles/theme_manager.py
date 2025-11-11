"""
Theme Manager for PyAI IDE
"""

from utils.logger import logger


class ThemeManager:
    """Manages application themes"""
    
    DARK_THEME = """
        QMainWindow {
            background-color: #1e1e1e;
            color: #d4d4d4;
        }
        QMenuBar {
            background-color: #2d2d2d;
            color: #d4d4d4;
            border-bottom: 1px solid #3e3e3e;
        }
        QMenuBar::item:selected {
            background-color: #3e3e3e;
        }
        QMenu {
            background-color: #2d2d2d;
            color: #d4d4d4;
            border: 1px solid #3e3e3e;
        }
        QMenu::item:selected {
            background-color: #0e639c;
        }
        QPushButton {
            background-color: #0e639c;
            color: #d4d4d4;
            border: none;
            padding: 5px;
            border-radius: 3px;
        }
        QPushButton:hover {
            background-color: #1177bb;
        }
        QPushButton:pressed {
            background-color: #0d5a96;
        }
        QLineEdit, QTextEdit, QPlainTextEdit {
            background-color: #252526;
            color: #d4d4d4;
            border: 1px solid #3e3e3e;
            padding: 3px;
        }
        QComboBox {
            background-color: #252526;
            color: #d4d4d4;
            border: 1px solid #3e3e3e;
            padding: 3px;
        }
        QTreeWidget, QListWidget {
            background-color: #252526;
            color: #d4d4d4;
            border: 1px solid #3e3e3e;
        }
        QStatusBar {
            background-color: #2d2d2d;
            color: #d4d4d4;
            border-top: 1px solid #3e3e3e;
        }
        QTabWidget::pane {
            border: 1px solid #3e3e3e;
        }
        QTabBar::tab {
            background-color: #2d2d2d;
            color: #d4d4d4;
            padding: 5px 15px;
            border: 1px solid #3e3e3e;
        }
        QTabBar::tab:selected {
            background-color: #1e1e1e;
            border-bottom: 2px solid #0e639c;
        }
    """
    
    LIGHT_THEME = """
        QMainWindow {
            background-color: #ffffff;
            color: #333333;
        }
        QMenuBar {
            background-color: #f0f0f0;
            color: #333333;
            border-bottom: 1px solid #e0e0e0;
        }
        QMenuBar::item:selected {
            background-color: #e0e0e0;
        }
        QMenu {
            background-color: #f0f0f0;
            color: #333333;
            border: 1px solid #e0e0e0;
        }
        QMenu::item:selected {
            background-color: #0e639c;
            color: #ffffff;
        }
        QPushButton {
            background-color: #0e639c;
            color: #ffffff;
            border: none;
            padding: 5px;
            border-radius: 3px;
        }
        QPushButton:hover {
            background-color: #1177bb;
        }
        QPushButton:pressed {
            background-color: #0d5a96;
        }
        QLineEdit, QTextEdit, QPlainTextEdit {
            background-color: #ffffff;
            color: #333333;
            border: 1px solid #cccccc;
            padding: 3px;
        }
        QComboBox {
            background-color: #ffffff;
            color: #333333;
            border: 1px solid #cccccc;
            padding: 3px;
        }
        QTreeWidget, QListWidget {
            background-color: #ffffff;
            color: #333333;
            border: 1px solid #cccccc;
        }
        QStatusBar {
            background-color: #f0f0f0;
            color: #333333;
            border-top: 1px solid #e0e0e0;
        }
        QTabWidget::pane {
            border: 1px solid #e0e0e0;
        }
        QTabBar::tab {
            background-color: #f0f0f0;
            color: #333333;
            padding: 5px 15px;
            border: 1px solid #e0e0e0;
        }
        QTabBar::tab:selected {
            background-color: #ffffff;
            border-bottom: 2px solid #0e639c;
        }
    """
    
    def __init__(self):
        """Initialize theme manager"""
        self.current_theme = "dark"
        logger.debug("Theme Manager initialized")
    
    def get_theme(self, theme_name="dark"):
        """Get theme stylesheet"""
        if theme_name.lower() == "light":
            logger.info("Loading light theme")
            return self.LIGHT_THEME
        else:
            logger.info("Loading dark theme")
            return self.DARK_THEME
    
    def set_theme(self, app, theme_name="dark"):
        """Set application theme"""
        stylesheet = self.get_theme(theme_name)
        app.setStyleSheet(stylesheet)
        self.current_theme = theme_name
        logger.info(f"Theme changed to: {theme_name}")
    
    def get_current_theme(self):
        """Get current theme name"""
        return self.current_theme
