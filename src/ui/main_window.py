"""
Main window for PyAI IDE
"""

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QMenuBar, QMenu, QStatusBar, QDockWidget, QTextEdit, QTreeWidget,
    QTreeWidgetItem, QLabel, QPushButton, QTabWidget
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QFont

from core.config_manager import ConfigManager
from core.plugin_system import PluginManager
from core.event_system import EventSystem
from services.github_service import GitHubService
from services.huggingface_service import HuggingFaceService


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        """Initialize main window"""
        super().__init__()
        
        # Initialize core systems
        self.config = ConfigManager()
        self.plugin_manager = PluginManager()
        self.event_system = EventSystem()
        self.github_service = GitHubService()
        self.huggingface_service = HuggingFaceService()
        
        # Set window properties
        self.setWindowTitle("PyAI IDE")
        self.setGeometry(100, 100, 1200, 800)
        
        # Create UI
        self._create_menu_bar()
        self._create_central_widget()
        self._create_dock_widgets()
        self._create_status_bar()
        
        # Load configuration
        self._load_configuration()
    
    def _create_menu_bar(self):
        """Create application menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        file_menu.addAction("New Project")
        file_menu.addAction("Open Project")
        file_menu.addAction("Save")
        file_menu.addAction("Save As")
        file_menu.addSeparator()
        file_menu.addAction("Exit")
        
        # Edit menu
        edit_menu = menubar.addMenu("Edit")
        edit_menu.addAction("Undo")
        edit_menu.addAction("Redo")
        edit_menu.addSeparator()
        edit_menu.addAction("Cut")
        edit_menu.addAction("Copy")
        edit_menu.addAction("Paste")
        
        # View menu
        view_menu = menubar.addMenu("View")
        view_menu.addAction("Toggle Console")
        view_menu.addAction("Toggle Project Tree")
        view_menu.addAction("Toggle Model Panel")
        view_menu.addAction("Toggle GitHub Panel")
        
        # Tools menu
        tools_menu = menubar.addMenu("Tools")
        tools_menu.addAction("Settings")
        tools_menu.addAction("Plugin Manager")
        
        # GitHub menu
        github_menu = menubar.addMenu("GitHub")
        github_menu.addAction("Connect Account")
        github_menu.addAction("Create Repository")
        github_menu.addAction("Clone Repository")
        
        # AI menu
        ai_menu = menubar.addMenu("AI")
        ai_menu.addAction("Load Model")
        ai_menu.addAction("Run Inference")
        ai_menu.addAction("Model Manager")
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        help_menu.addAction("Documentation")
        help_menu.addAction("About")
    
    def _create_central_widget(self):
        """Create central widget with editor and panels"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QHBoxLayout(central_widget)
        
        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Horizontal)
        
        # Project tree (left panel)
        self.project_tree = QTreeWidget()
        self.project_tree.setHeaderLabel("Project")
        self.project_tree.setMaximumWidth(250)
        splitter.addWidget(self.project_tree)
        
        # Editor area (center)
        editor_layout = QVBoxLayout()
        
        # Tab widget for multiple files
        self.editor_tabs = QTabWidget()
        self.editor_tabs.setTabsClosable(True)
        
        # Create a default editor tab
        default_editor = QTextEdit()
        default_editor.setFont(QFont("Courier New", 11))
        self.editor_tabs.addTab(default_editor, "Untitled")
        
        editor_layout.addWidget(self.editor_tabs)
        
        editor_widget = QWidget()
        editor_widget.setLayout(editor_layout)
        splitter.addWidget(editor_widget)
        
        # Right panels (Model and GitHub)
        right_layout = QVBoxLayout()
        
        # Model panel
        model_label = QLabel("AI Models")
        model_label.setFont(QFont("Arial", 10, QFont.Bold))
        right_layout.addWidget(model_label)
        
        self.model_list = QTreeWidget()
        self.model_list.setHeaderLabel("Loaded Models")
        self.model_list.setMaximumWidth(250)
        right_layout.addWidget(self.model_list)
        
        # GitHub panel
        github_label = QLabel("GitHub")
        github_label.setFont(QFont("Arial", 10, QFont.Bold))
        right_layout.addWidget(github_label)
        
        self.github_panel = QTreeWidget()
        self.github_panel.setHeaderLabel("Repositories")
        self.github_panel.setMaximumWidth(250)
        right_layout.addWidget(self.github_panel)
        
        right_widget = QWidget()
        right_widget.setLayout(right_layout)
        splitter.addWidget(right_widget)
        
        layout.addWidget(splitter)
    
    def _create_dock_widgets(self):
        """Create dock widgets for console and other panels"""
        # Console dock
        console_dock = QDockWidget("Console", self)
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setFont(QFont("Courier New", 10))
        self.console.setMaximumHeight(200)
        console_dock.setWidget(self.console)
        self.addDockWidget(Qt.BottomDockWidgetArea, console_dock)
    
    def _create_status_bar(self):
        """Create status bar"""
        status_bar = self.statusBar()
        status_bar.showMessage("Ready")
    
    def _load_configuration(self):
        """Load configuration from config manager"""
        # Load window size
        width = self.config.get("app.window_width", 1200)
        height = self.config.get("app.window_height", 800)
        self.resize(width, height)
        
        # Load theme
        theme = self.config.get("app.theme", "dark")
        self._apply_theme(theme)
    
    def _apply_theme(self, theme: str):
        """Apply theme to application"""
        if theme == "dark":
            self._apply_dark_theme()
        else:
            self._apply_light_theme()
    
    def _apply_dark_theme(self):
        """Apply dark theme"""
        dark_stylesheet = """
            QMainWindow {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QMenuBar {
                background-color: #2d2d2d;
                color: #ffffff;
            }
            QMenuBar::item:selected {
                background-color: #3d3d3d;
            }
            QMenu {
                background-color: #2d2d2d;
                color: #ffffff;
            }
            QMenu::item:selected {
                background-color: #3d3d3d;
            }
            QTextEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #3d3d3d;
            }
            QTreeWidget {
                background-color: #252525;
                color: #ffffff;
                border: 1px solid #3d3d3d;
            }
            QTreeWidget::item:selected {
                background-color: #0e639c;
            }
            QStatusBar {
                background-color: #2d2d2d;
                color: #ffffff;
            }
        """
        self.setStyleSheet(dark_stylesheet)
    
    def _apply_light_theme(self):
        """Apply light theme"""
        light_stylesheet = """
            QMainWindow {
                background-color: #ffffff;
                color: #000000;
            }
            QMenuBar {
                background-color: #f0f0f0;
                color: #000000;
            }
            QMenuBar::item:selected {
                background-color: #e0e0e0;
            }
            QMenu {
                background-color: #f0f0f0;
                color: #000000;
            }
            QMenu::item:selected {
                background-color: #e0e0e0;
            }
            QTextEdit {
                background-color: #ffffff;
                color: #000000;
                border: 1px solid #cccccc;
            }
            QTreeWidget {
                background-color: #fafafa;
                color: #000000;
                border: 1px solid #cccccc;
            }
            QTreeWidget::item:selected {
                background-color: #0078d4;
                color: #ffffff;
            }
            QStatusBar {
                background-color: #f0f0f0;
                color: #000000;
            }
        """
        self.setStyleSheet(light_stylesheet)
    
    def closeEvent(self, event):
        """Handle window close event"""
        # Save configuration
        self.config.set("app.window_width", self.width())
        self.config.set("app.window_height", self.height())
        self.config.save()
        
        event.accept()
