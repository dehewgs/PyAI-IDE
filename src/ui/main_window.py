"""
Main window for PyAI IDE
"""

import sys
import traceback
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QMenuBar, QMenu, QStatusBar, QDockWidget, QTextEdit, QTreeWidget,
    QTreeWidgetItem, QLabel, QPushButton, QTabWidget, QMessageBox
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QFont

try:
    from core.config_manager import ConfigManager
    from core.plugin_system import PluginManager
    from core.event_system import EventSystem
    from services.github_service import GitHubService
    from services.huggingface_service import HuggingFaceService
except ImportError as e:
    print(f"Error importing core modules: {e}")
    traceback.print_exc()


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        """Initialize main window"""
        super().__init__()
        
        try:
            # Initialize core systems with error handling
            print("[*] Initializing ConfigManager...")
            self.config = ConfigManager()
            print("[OK] ConfigManager initialized")
            
            print("[*] Initializing PluginManager...")
            self.plugin_manager = PluginManager()
            print("[OK] PluginManager initialized")
            
            print("[*] Initializing EventSystem...")
            self.event_system = EventSystem()
            print("[OK] EventSystem initialized")
            
            print("[*] Initializing GitHub Service...")
            self.github_service = GitHubService()
            print("[OK] GitHub Service initialized")
            
            print("[*] Initializing HuggingFace Service...")
            self.huggingface_service = HuggingFaceService()
            print("[OK] HuggingFace Service initialized")
            
            # Set window properties
            self.setWindowTitle("PyAI IDE")
            self.setGeometry(100, 100, 1200, 800)
            
            # Create UI
            print("[*] Creating UI...")
            self._create_menu_bar()
            self._create_central_widget()
            self._create_dock_widgets()
            self._create_status_bar()
            print("[OK] UI created")
            
            # Load configuration
            print("[*] Loading configuration...")
            self._load_configuration()
            print("[OK] Configuration loaded")
            
            print("[OK] MainWindow initialized successfully")
            
        except Exception as e:
            print(f"[ERROR] Failed to initialize MainWindow: {e}")
            traceback.print_exc()
            
            # Show error dialog
            try:
                QMessageBox.critical(
                    self,
                    "Initialization Error",
                    f"Failed to initialize application:\n\n{str(e)}\n\n"
                    f"Check console for details."
                )
            except:
                pass
            
            raise
    
    def _create_menu_bar(self):
        """Create application menu bar"""
        try:
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
        except Exception as e:
            print(f"[ERROR] Failed to create menu bar: {e}")
            traceback.print_exc()
    
    def _create_central_widget(self):
        """Create central widget with editor and panels"""
        try:
            central_widget = QWidget()
            layout = QHBoxLayout()
            
            # Create splitter for resizable panels
            splitter = QSplitter(Qt.Horizontal)
            
            # Left panel - Project tree
            left_panel = QWidget()
            left_layout = QVBoxLayout()
            left_layout.addWidget(QLabel("Project"))
            tree = QTreeWidget()
            tree.setHeaderLabel("Files")
            left_layout.addWidget(tree)
            left_panel.setLayout(left_layout)
            
            # Center panel - Editor
            center_panel = QWidget()
            center_layout = QVBoxLayout()
            center_layout.addWidget(QLabel("Editor"))
            editor = QTextEdit()
            editor.setPlaceholderText("Start coding here...")
            center_layout.addWidget(editor)
            center_panel.setLayout(center_layout)
            
            # Right panel - Models and GitHub
            right_panel = QWidget()
            right_layout = QVBoxLayout()
            tabs = QTabWidget()
            
            # Models tab
            models_widget = QWidget()
            models_layout = QVBoxLayout()
            models_layout.addWidget(QLabel("Available Models"))
            models_layout.addWidget(QPushButton("Load Model"))
            models_widget.setLayout(models_layout)
            tabs.addTab(models_widget, "Models")
            
            # GitHub tab
            github_widget = QWidget()
            github_layout = QVBoxLayout()
            github_layout.addWidget(QLabel("GitHub Repositories"))
            github_layout.addWidget(QPushButton("Connect GitHub"))
            github_widget.setLayout(github_layout)
            tabs.addTab(github_widget, "GitHub")
            
            right_layout.addWidget(tabs)
            right_panel.setLayout(right_layout)
            
            # Add panels to splitter
            splitter.addWidget(left_panel)
            splitter.addWidget(center_panel)
            splitter.addWidget(right_panel)
            splitter.setStretchFactor(0, 1)
            splitter.setStretchFactor(1, 2)
            splitter.setStretchFactor(2, 1)
            
            layout.addWidget(splitter)
            central_widget.setLayout(layout)
            self.setCentralWidget(central_widget)
        except Exception as e:
            print(f"[ERROR] Failed to create central widget: {e}")
            traceback.print_exc()
    
    def _create_dock_widgets(self):
        """Create dock widgets"""
        try:
            # Console dock
            console_dock = QDockWidget("Console", self)
            console = QTextEdit()
            console.setReadOnly(True)
            console.setMaximumHeight(150)
            console_dock.setWidget(console)
            self.addDockWidget(Qt.BottomDockWidgetArea, console_dock)
        except Exception as e:
            print(f"[ERROR] Failed to create dock widgets: {e}")
            traceback.print_exc()
    
    def _create_status_bar(self):
        """Create status bar"""
        try:
            status_bar = self.statusBar()
            status_bar.showMessage("Ready")
        except Exception as e:
            print(f"[ERROR] Failed to create status bar: {e}")
            traceback.print_exc()
    
    def _load_configuration(self):
        """Load configuration from config manager"""
        try:
            if not hasattr(self, 'config') or self.config is None:
                print("[!] Warning: Config not initialized")
                return
            
            # Load window size
            width = self.config.get("app.window_width", 1200)
            height = self.config.get("app.window_height", 800)
            self.resize(width, height)
            
            # Load theme
            theme = self.config.get("app.theme", "dark")
            self._apply_theme(theme)
        except Exception as e:
            print(f"[ERROR] Failed to load configuration: {e}")
            traceback.print_exc()
    
    def _apply_theme(self, theme: str):
        """Apply theme to application"""
        try:
            if theme == "dark":
                self._apply_dark_theme()
            else:
                self._apply_light_theme()
        except Exception as e:
            print(f"[ERROR] Failed to apply theme: {e}")
            traceback.print_exc()
    
    def _apply_dark_theme(self):
        """Apply dark theme"""
        try:
            dark_stylesheet = """
                QMainWindow { background-color: #1e1e1e; color: #ffffff; }
                QMenuBar { background-color: #2d2d2d; color: #ffffff; }
                QMenuBar::item:selected { background-color: #3d3d3d; }
                QMenu { background-color: #2d2d2d; color: #ffffff; }
                QMenu::item:selected { background-color: #3d3d3d; }
                QTextEdit { background-color: #252526; color: #d4d4d4; border: 1px solid #3e3e42; }
                QTreeWidget { background-color: #252526; color: #d4d4d4; border: 1px solid #3e3e42; }
                QLabel { color: #d4d4d4; }
                QPushButton { background-color: #0e639c; color: #ffffff; border: none; padding: 5px; border-radius: 3px; }
                QPushButton:hover { background-color: #1177bb; }
                QStatusBar { background-color: #2d2d2d; color: #ffffff; }
            """
            self.setStyleSheet(dark_stylesheet)
        except Exception as e:
            print(f"[ERROR] Failed to apply dark theme: {e}")
            traceback.print_exc()
    
    def _apply_light_theme(self):
        """Apply light theme"""
        try:
            light_stylesheet = """
                QMainWindow { background-color: #ffffff; color: #000000; }
                QMenuBar { background-color: #f3f3f3; color: #000000; }
                QMenuBar::item:selected { background-color: #e0e0e0; }
                QMenu { background-color: #f3f3f3; color: #000000; }
                QMenu::item:selected { background-color: #e0e0e0; }
                QTextEdit { background-color: #ffffff; color: #000000; border: 1px solid #cccccc; }
                QTreeWidget { background-color: #ffffff; color: #000000; border: 1px solid #cccccc; }
                QLabel { color: #000000; }
                QPushButton { background-color: #0078d4; color: #ffffff; border: none; padding: 5px; border-radius: 3px; }
                QPushButton:hover { background-color: #1084d7; }
                QStatusBar { background-color: #f3f3f3; color: #000000; }
            """
            self.setStyleSheet(light_stylesheet)
        except Exception as e:
            print(f"[ERROR] Failed to apply light theme: {e}")
            traceback.print_exc()
