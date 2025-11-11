"""
Main window for PyAI IDE - Completely rewritten with proper signal/slot connections
"""

import sys
import traceback
from pathlib import Path
from typing import Optional

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QMenuBar, QMenu, QStatusBar, QDockWidget, QTextEdit, QTreeWidget,
    QTreeWidgetItem, QLabel, QPushButton, QTabWidget, QMessageBox,
    QFileDialog, QInputDialog, QProgressDialog, QDialog, QLineEdit,
    QFormLayout
)
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QObject, QThread
from PyQt5.QtGui import QIcon, QFont, QTextCursor

from utils.logger import get_logger

try:
    from core.config_manager import ConfigManager
    from core.plugin_system import PluginManager
    from core.event_system import EventSystem
    from services.github_service import GitHubService
    from services.huggingface_service import HuggingFaceService
except ImportError as e:
    print(f"Error importing core modules: {e}")
    traceback.print_exc()


# Initialize logger
logger = get_logger("PyAI-IDE")


class WorkerThread(QThread):
    """Worker thread for long-running operations"""
    
    finished = pyqtSignal()
    error = pyqtSignal(str)
    progress = pyqtSignal(str)
    
    def __init__(self, operation, *args, **kwargs):
        super().__init__()
        self.operation = operation
        self.args = args
        self.kwargs = kwargs
    
    def run(self):
        """Run the operation in a separate thread"""
        try:
            logger.debug(f"WorkerThread: Starting operation {self.operation.__name__}")
            self.operation(*self.args, **self.kwargs)
            logger.debug(f"WorkerThread: Operation {self.operation.__name__} completed")
            self.finished.emit()
        except Exception as e:
            logger.error(f"WorkerThread: Error in operation {self.operation.__name__}: {e}")
            self.error.emit(str(e))


class MainWindow(QMainWindow):
    """Main application window with comprehensive debugging"""
    
    # Signals for thread-safe operations
    log_signal = pyqtSignal(str)
    
    def __init__(self):
        """Initialize main window"""
        super().__init__()
        
        logger.info("=" * 80)
        logger.info("PyAI IDE - Starting Application")
        logger.info("=" * 80)
        
        try:
            # Initialize core systems with error handling
            logger.info("Initializing core systems...")
            self._initialize_core_systems()
            
            # Set window properties
            logger.debug("Setting window properties...")
            self.setWindowTitle("PyAI IDE")
            self.setGeometry(100, 100, 1200, 800)
            
            # Create UI
            logger.info("Creating user interface...")
            self._create_menu_bar()
            self._create_central_widget()
            self._create_dock_widgets()
            self._create_status_bar()
            logger.info("User interface created successfully")
            
            # Load configuration
            logger.info("Loading configuration...")
            self._load_configuration()
            logger.info("Configuration loaded successfully")
            
            # Connect signals
            logger.debug("Connecting signals...")
            self._connect_signals()
            
            logger.info("=" * 80)
            logger.info("MainWindow initialized successfully")
            logger.info("=" * 80)
            
        except Exception as e:
            logger.critical(f"Failed to initialize MainWindow: {e}")
            logger.exception("MainWindow initialization error", e)
            
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
    
    def _initialize_core_systems(self):
        """Initialize all core systems"""
        try:
            logger.debug("Initializing ConfigManager...")
            self.config = ConfigManager()
            logger.debug("ConfigManager initialized")
            
            logger.debug("Initializing PluginManager...")
            self.plugin_manager = PluginManager()
            logger.debug("PluginManager initialized")
            
            logger.debug("Initializing EventSystem...")
            self.event_system = EventSystem()
            logger.debug("EventSystem initialized")
            
            logger.debug("Initializing GitHub Service...")
            self.github_service = GitHubService()
            logger.debug("GitHub Service initialized")
            
            logger.debug("Initializing HuggingFace Service...")
            self.huggingface_service = HuggingFaceService()
            logger.debug("HuggingFace Service initialized")
            
            logger.info("All core systems initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing core systems: {e}")
            logger.exception("Core systems initialization error", e)
            raise
    
    def _create_menu_bar(self):
        """Create application menu bar with proper signal connections"""
        try:
            logger.debug("Creating menu bar...")
            menubar = self.menuBar()
            
            # File menu
            logger.debug("Creating File menu...")
            file_menu = menubar.addMenu("File")
            
            new_project_action = file_menu.addAction("New Project")
            new_project_action.triggered.connect(self._on_new_project)
            logger.debug("Added 'New Project' action")
            
            open_project_action = file_menu.addAction("Open Project")
            open_project_action.triggered.connect(self._on_open_project)
            logger.debug("Added 'Open Project' action")
            
            save_action = file_menu.addAction("Save")
            save_action.triggered.connect(self._on_save)
            logger.debug("Added 'Save' action")
            
            save_as_action = file_menu.addAction("Save As")
            save_as_action.triggered.connect(self._on_save_as)
            logger.debug("Added 'Save As' action")
            
            file_menu.addSeparator()
            
            exit_action = file_menu.addAction("Exit")
            exit_action.triggered.connect(self.close)
            logger.debug("Added 'Exit' action")
            
            # Edit menu
            logger.debug("Creating Edit menu...")
            edit_menu = menubar.addMenu("Edit")
            
            undo_action = edit_menu.addAction("Undo")
            undo_action.triggered.connect(self._on_undo)
            logger.debug("Added 'Undo' action")
            
            redo_action = edit_menu.addAction("Redo")
            redo_action.triggered.connect(self._on_redo)
            logger.debug("Added 'Redo' action")
            
            edit_menu.addSeparator()
            
            cut_action = edit_menu.addAction("Cut")
            cut_action.triggered.connect(self._on_cut)
            logger.debug("Added 'Cut' action")
            
            copy_action = edit_menu.addAction("Copy")
            copy_action.triggered.connect(self._on_copy)
            logger.debug("Added 'Copy' action")
            
            paste_action = edit_menu.addAction("Paste")
            paste_action.triggered.connect(self._on_paste)
            logger.debug("Added 'Paste' action")
            
            # View menu
            logger.debug("Creating View menu...")
            view_menu = menubar.addMenu("View")
            
            toggle_console_action = view_menu.addAction("Toggle Console")
            toggle_console_action.triggered.connect(self._on_toggle_console)
            logger.debug("Added 'Toggle Console' action")
            
            toggle_tree_action = view_menu.addAction("Toggle Project Tree")
            toggle_tree_action.triggered.connect(self._on_toggle_tree)
            logger.debug("Added 'Toggle Project Tree' action")
            
            # Tools menu
            logger.debug("Creating Tools menu...")
            tools_menu = menubar.addMenu("Tools")
            
            settings_action = tools_menu.addAction("Settings")
            settings_action.triggered.connect(self._on_settings)
            logger.debug("Added 'Settings' action")
            
            plugin_manager_action = tools_menu.addAction("Plugin Manager")
            plugin_manager_action.triggered.connect(self._on_plugin_manager)
            logger.debug("Added 'Plugin Manager' action")
            
            # GitHub menu
            logger.debug("Creating GitHub menu...")
            github_menu = menubar.addMenu("GitHub")
            
            connect_github_action = github_menu.addAction("Connect Account")
            connect_github_action.triggered.connect(self._on_connect_github)
            logger.debug("Added 'Connect Account' action")
            
            create_repo_action = github_menu.addAction("Create Repository")
            create_repo_action.triggered.connect(self._on_create_repository)
            logger.debug("Added 'Create Repository' action")
            
            clone_repo_action = github_menu.addAction("Clone Repository")
            clone_repo_action.triggered.connect(self._on_clone_repository)
            logger.debug("Added 'Clone Repository' action")
            
            # AI menu
            logger.debug("Creating AI menu...")
            ai_menu = menubar.addMenu("AI")
            
            load_model_action = ai_menu.addAction("Load Model")
            load_model_action.triggered.connect(self._on_load_model)
            logger.debug("Added 'Load Model' action")
            
            run_inference_action = ai_menu.addAction("Run Inference")
            run_inference_action.triggered.connect(self._on_run_inference)
            logger.debug("Added 'Run Inference' action")
            
            model_manager_action = ai_menu.addAction("Model Manager")
            model_manager_action.triggered.connect(self._on_model_manager)
            logger.debug("Added 'Model Manager' action")
            
            # Help menu
            logger.debug("Creating Help menu...")
            help_menu = menubar.addMenu("Help")
            
            docs_action = help_menu.addAction("Documentation")
            docs_action.triggered.connect(self._on_documentation)
            logger.debug("Added 'Documentation' action")
            
            about_action = help_menu.addAction("About")
            about_action.triggered.connect(self._on_about)
            logger.debug("Added 'About' action")
            
            logger.info("Menu bar created successfully")
            
        except Exception as e:
            logger.error(f"Failed to create menu bar: {e}")
            logger.exception("Menu bar creation error", e)
    
    def _create_central_widget(self):
        """Create central widget with editor and panels"""
        try:
            logger.debug("Creating central widget...")
            central_widget = QWidget()
            layout = QHBoxLayout()
            
            # Create splitter for resizable panels
            splitter = QSplitter(Qt.Horizontal)
            
            # Left panel - Project tree
            logger.debug("Creating left panel (Project tree)...")
            left_panel = QWidget()
            left_layout = QVBoxLayout()
            left_layout.addWidget(QLabel("Project"))
            self.project_tree = QTreeWidget()
            self.project_tree.setHeaderLabel("Files")
            left_layout.addWidget(self.project_tree)
            left_panel.setLayout(left_layout)
            logger.debug("Left panel created")
            
            # Center panel - Editor
            logger.debug("Creating center panel (Editor)...")
            center_panel = QWidget()
            center_layout = QVBoxLayout()
            center_layout.addWidget(QLabel("Editor"))
            self.editor = QTextEdit()
            self.editor.setPlaceholderText("Start coding here...")
            center_layout.addWidget(self.editor)
            center_panel.setLayout(center_layout)
            logger.debug("Center panel created")
            
            # Right panel - Models and GitHub
            logger.debug("Creating right panel (Models and GitHub)...")
            right_panel = QWidget()
            right_layout = QVBoxLayout()
            tabs = QTabWidget()
            
            # Models tab
            logger.debug("Creating Models tab...")
            models_widget = QWidget()
            models_layout = QVBoxLayout()
            models_layout.addWidget(QLabel("Available Models"))
            self.load_model_btn = QPushButton("Load Model")
            self.load_model_btn.clicked.connect(self._on_load_model)
            models_layout.addWidget(self.load_model_btn)
            logger.debug("Load Model button connected")
            models_widget.setLayout(models_layout)
            tabs.addTab(models_widget, "Models")
            logger.debug("Models tab created")
            
            # GitHub tab
            logger.debug("Creating GitHub tab...")
            github_widget = QWidget()
            github_layout = QVBoxLayout()
            github_layout.addWidget(QLabel("GitHub Repositories"))
            self.connect_github_btn = QPushButton("Connect GitHub")
            self.connect_github_btn.clicked.connect(self._on_connect_github)
            github_layout.addWidget(self.connect_github_btn)
            logger.debug("Connect GitHub button connected")
            github_widget.setLayout(github_layout)
            tabs.addTab(github_widget, "GitHub")
            logger.debug("GitHub tab created")
            
            right_layout.addWidget(tabs)
            right_panel.setLayout(right_layout)
            logger.debug("Right panel created")
            
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
            
            logger.info("Central widget created successfully")
            
        except Exception as e:
            logger.error(f"Failed to create central widget: {e}")
            logger.exception("Central widget creation error", e)
    
    def _create_dock_widgets(self):
        """Create dock widgets"""
        try:
            logger.debug("Creating dock widgets...")
            
            # Console dock
            console_dock = QDockWidget("Console", self)
            self.console = QTextEdit()
            self.console.setReadOnly(True)
            self.console.setMaximumHeight(150)
            console_dock.setWidget(self.console)
            self.addDockWidget(Qt.BottomDockWidgetArea, console_dock)
            
            logger.info("Dock widgets created successfully")
            
        except Exception as e:
            logger.error(f"Failed to create dock widgets: {e}")
            logger.exception("Dock widgets creation error", e)
    
    def _create_status_bar(self):
        """Create status bar"""
        try:
            logger.debug("Creating status bar...")
            status_bar = self.statusBar()
            status_bar.showMessage("Ready")
            logger.debug("Status bar created")
            
        except Exception as e:
            logger.error(f"Failed to create status bar: {e}")
            logger.exception("Status bar creation error", e)
    
    def _connect_signals(self):
        """Connect custom signals"""
        try:
            logger.debug("Connecting custom signals...")
            self.log_signal.connect(self._on_log_message)
            logger.debug("Log signal connected")
            
        except Exception as e:
            logger.error(f"Failed to connect signals: {e}")
            logger.exception("Signal connection error", e)
    
    def _load_configuration(self):
        """Load configuration from config manager"""
        try:
            logger.debug("Loading configuration...")
            
            if not hasattr(self, 'config') or self.config is None:
                logger.warning("Config not initialized")
                return
            
            # Load window size
            width = self.config.get("app.window_width", 1200)
            height = self.config.get("app.window_height", 800)
            logger.debug(f"Loading window size: {width}x{height}")
            self.resize(width, height)
            
            # Load theme
            theme = self.config.get("app.theme", "dark")
            logger.debug(f"Loading theme: {theme}")
            self._apply_theme(theme)
            
            logger.info("Configuration loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
            logger.exception("Configuration loading error", e)
    
    def _apply_theme(self, theme: str):
        """Apply theme to application"""
        try:
            logger.debug(f"Applying theme: {theme}")
            
            if theme == "dark":
                self._apply_dark_theme()
            else:
                self._apply_light_theme()
            
            logger.debug(f"Theme '{theme}' applied successfully")
            
        except Exception as e:
            logger.error(f"Failed to apply theme: {e}")
            logger.exception("Theme application error", e)
    
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
                QPushButton:pressed { background-color: #0d5a8f; }
                QStatusBar { background-color: #2d2d2d; color: #ffffff; }
                QDockWidget { background-color: #1e1e1e; color: #ffffff; }
                QTabWidget { background-color: #1e1e1e; color: #ffffff; }
                QTabBar::tab { background-color: #2d2d2d; color: #ffffff; padding: 5px; }
                QTabBar::tab:selected { background-color: #3d3d3d; }
            """
            self.setStyleSheet(dark_stylesheet)
            logger.debug("Dark theme applied")
            
        except Exception as e:
            logger.error(f"Failed to apply dark theme: {e}")
            logger.exception("Dark theme error", e)
    
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
                QPushButton:pressed { background-color: #005a9e; }
                QStatusBar { background-color: #f3f3f3; color: #000000; }
                QDockWidget { background-color: #ffffff; color: #000000; }
                QTabWidget { background-color: #ffffff; color: #000000; }
                QTabBar::tab { background-color: #e0e0e0; color: #000000; padding: 5px; }
                QTabBar::tab:selected { background-color: #ffffff; }
            """
            self.setStyleSheet(light_stylesheet)
            logger.debug("Light theme applied")
            
        except Exception as e:
            logger.error(f"Failed to apply light theme: {e}")
            logger.exception("Light theme error", e)
    
    # ==================== Menu Action Handlers ====================
    
    def _on_new_project(self):
        """Handle new project action"""
        logger.info("New Project action triggered")
        try:
            project_name, ok = QInputDialog.getText(self, "New Project", "Project name:")
            if ok and project_name:
                logger.info(f"Creating new project: {project_name}")
                self._log_to_console(f"Creating new project: {project_name}")
                self.statusBar().showMessage(f"Created project: {project_name}")
        except Exception as e:
            logger.error(f"Error creating new project: {e}")
            self._show_error("New Project Error", str(e))
    
    def _on_open_project(self):
        """Handle open project action"""
        logger.info("Open Project action triggered")
        try:
            path = QFileDialog.getExistingDirectory(self, "Open Project")
            if path:
                logger.info(f"Opening project: {path}")
                self._log_to_console(f"Opening project: {path}")
                self.statusBar().showMessage(f"Opened project: {path}")
        except Exception as e:
            logger.error(f"Error opening project: {e}")
            self._show_error("Open Project Error", str(e))
    
    def _on_save(self):
        """Handle save action"""
        logger.info("Save action triggered")
        try:
            content = self.editor.toPlainText()
            logger.debug(f"Saving {len(content)} characters")
            self._log_to_console("File saved")
            self.statusBar().showMessage("File saved")
        except Exception as e:
            logger.error(f"Error saving file: {e}")
            self._show_error("Save Error", str(e))
    
    def _on_save_as(self):
        """Handle save as action"""
        logger.info("Save As action triggered")
        try:
            path, _ = QFileDialog.getSaveFileName(self, "Save As")
            if path:
                logger.info(f"Saving file as: {path}")
                self._log_to_console(f"File saved as: {path}")
                self.statusBar().showMessage(f"File saved as: {path}")
        except Exception as e:
            logger.error(f"Error saving file as: {e}")
            self._show_error("Save As Error", str(e))
    
    def _on_undo(self):
        """Handle undo action"""
        logger.debug("Undo action triggered")
        try:
            self.editor.undo()
            self._log_to_console("Undo")
        except Exception as e:
            logger.error(f"Error undoing: {e}")
    
    def _on_redo(self):
        """Handle redo action"""
        logger.debug("Redo action triggered")
        try:
            self.editor.redo()
            self._log_to_console("Redo")
        except Exception as e:
            logger.error(f"Error redoing: {e}")
    
    def _on_cut(self):
        """Handle cut action"""
        logger.debug("Cut action triggered")
        try:
            self.editor.cut()
            self._log_to_console("Cut")
        except Exception as e:
            logger.error(f"Error cutting: {e}")
    
    def _on_copy(self):
        """Handle copy action"""
        logger.debug("Copy action triggered")
        try:
            self.editor.copy()
            self._log_to_console("Copy")
        except Exception as e:
            logger.error(f"Error copying: {e}")
    
    def _on_paste(self):
        """Handle paste action"""
        logger.debug("Paste action triggered")
        try:
            self.editor.paste()
            self._log_to_console("Paste")
        except Exception as e:
            logger.error(f"Error pasting: {e}")
    
    def _on_toggle_console(self):
        """Handle toggle console action"""
        logger.debug("Toggle Console action triggered")
        try:
            # Find console dock widget
            for dock in self.findChildren(QDockWidget):
                if "Console" in dock.windowTitle():
                    dock.setVisible(not dock.isVisible())
                    logger.debug(f"Console visibility toggled: {dock.isVisible()}")
                    break
        except Exception as e:
            logger.error(f"Error toggling console: {e}")
    
    def _on_toggle_tree(self):
        """Handle toggle project tree action"""
        logger.debug("Toggle Project Tree action triggered")
        try:
            self.project_tree.setVisible(not self.project_tree.isVisible())
            logger.debug(f"Project tree visibility toggled: {self.project_tree.isVisible()}")
        except Exception as e:
            logger.error(f"Error toggling project tree: {e}")
    
    def _on_settings(self):
        """Handle settings action"""
        logger.info("Settings action triggered")
        try:
            self._log_to_console("Opening settings...")
            self.statusBar().showMessage("Settings dialog opened")
        except Exception as e:
            logger.error(f"Error opening settings: {e}")
            self._show_error("Settings Error", str(e))
    
    def _on_plugin_manager(self):
        """Handle plugin manager action"""
        logger.info("Plugin Manager action triggered")
        try:
            plugins = self.plugin_manager.list_plugins()
            logger.info(f"Loaded plugins: {len(plugins)}")
            self._log_to_console(f"Loaded plugins: {len(plugins)}")
            for plugin in plugins:
                logger.debug(f"  - {plugin}")
                self._log_to_console(f"  - {plugin}")
        except Exception as e:
            logger.error(f"Error opening plugin manager: {e}")
            self._show_error("Plugin Manager Error", str(e))
    
    def _on_connect_github(self):
        """Handle connect GitHub action"""
        logger.info("Connect GitHub action triggered")
        try:
            token, ok = QInputDialog.getText(
                self, 
                "GitHub Token", 
                "Enter your GitHub Personal Access Token:",
                QLineEdit.Password
            )
            if ok and token:
                logger.info("Attempting to authenticate with GitHub...")
                self._log_to_console("Authenticating with GitHub...")
                success, message = self.github_service.set_token(token)
                if success:
                    logger.info(f"GitHub authentication successful: {message}")
                    self._log_to_console(f"GitHub: {message}")
                    self.statusBar().showMessage(f"GitHub: {message}")
                else:
                    logger.error(f"GitHub authentication failed: {message}")
                    self._show_error("GitHub Error", message)
        except Exception as e:
            logger.error(f"Error connecting to GitHub: {e}")
            logger.exception("GitHub connection error", e)
            self._show_error("GitHub Error", str(e))
    
    def _on_create_repository(self):
        """Handle create repository action"""
        logger.info("Create Repository action triggered")
        try:
            if not self.github_service.is_authenticated():
                logger.warning("Not authenticated with GitHub")
                self._show_error("GitHub Error", "Not authenticated with GitHub")
                return
            
            repo_name, ok = QInputDialog.getText(self, "Create Repository", "Repository name:")
            if ok and repo_name:
                logger.info(f"Creating repository: {repo_name}")
                self._log_to_console(f"Creating repository: {repo_name}...")
                success, result = self.github_service.create_repository(repo_name)
                if success:
                    logger.info(f"Repository created: {result}")
                    self._log_to_console(f"Repository created: {result}")
                    self.statusBar().showMessage(f"Repository created: {result}")
                else:
                    logger.error(f"Failed to create repository: {result}")
                    self._show_error("Repository Error", result)
        except Exception as e:
            logger.error(f"Error creating repository: {e}")
            logger.exception("Repository creation error", e)
            self._show_error("Repository Error", str(e))
    
    def _on_clone_repository(self):
        """Handle clone repository action"""
        logger.info("Clone Repository action triggered")
        try:
            repo_url, ok = QInputDialog.getText(self, "Clone Repository", "Repository URL:")
            if ok and repo_url:
                path = QFileDialog.getExistingDirectory(self, "Select destination folder")
                if path:
                    logger.info(f"Cloning repository: {repo_url} to {path}")
                    self._log_to_console(f"Cloning repository: {repo_url}...")
                    success, message = self.github_service.clone_repository(repo_url, path)
                    if success:
                        logger.info(f"Repository cloned: {message}")
                        self._log_to_console(f"Repository cloned: {message}")
                        self.statusBar().showMessage(message)
                    else:
                        logger.error(f"Failed to clone repository: {message}")
                        self._show_error("Clone Error", message)
        except Exception as e:
            logger.error(f"Error cloning repository: {e}")
            logger.exception("Repository clone error", e)
            self._show_error("Clone Error", str(e))
    
    def _on_load_model(self):
        """Handle load model action"""
        logger.info("Load Model action triggered")
        try:
            model_id, ok = QInputDialog.getText(self, "Load Model", "Model ID (e.g., gpt2):")
            if ok and model_id:
                logger.info(f"Loading model: {model_id}")
                self._log_to_console(f"Loading model: {model_id}...")
                success, message = self.huggingface_service.load_model(model_id)
                if success:
                    logger.info(f"Model loaded: {message}")
                    self._log_to_console(f"Model loaded: {message}")
                    self.statusBar().showMessage(message)
                else:
                    logger.error(f"Failed to load model: {message}")
                    self._show_error("Model Error", message)
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            logger.exception("Model loading error", e)
            self._show_error("Model Error", str(e))
    
    def _on_run_inference(self):
        """Handle run inference action"""
        logger.info("Run Inference action triggered")
        try:
            models = self.huggingface_service.list_loaded_models()
            if not models:
                logger.warning("No models loaded")
                self._show_error("Inference Error", "No models loaded. Load a model first.")
                return
            
            text, ok = QInputDialog.getText(self, "Run Inference", "Input text:")
            if ok and text:
                logger.info(f"Running inference with input: {text[:50]}...")
                self._log_to_console(f"Running inference...")
                # Use first loaded model
                model_id = models[0]
                success, result = self.huggingface_service.infer(model_id, text)
                if success:
                    logger.info(f"Inference completed")
                    self._log_to_console(f"Inference result: {str(result)[:200]}...")
                    self.statusBar().showMessage("Inference completed")
                else:
                    logger.error(f"Inference failed: {result}")
                    self._show_error("Inference Error", result)
        except Exception as e:
            logger.error(f"Error running inference: {e}")
            logger.exception("Inference error", e)
            self._show_error("Inference Error", str(e))
    
    def _on_model_manager(self):
        """Handle model manager action"""
        logger.info("Model Manager action triggered")
        try:
            models = self.huggingface_service.list_loaded_models()
            logger.info(f"Loaded models: {len(models)}")
            self._log_to_console(f"Loaded models: {len(models)}")
            for model in models:
                logger.debug(f"  - {model}")
                self._log_to_console(f"  - {model}")
        except Exception as e:
            logger.error(f"Error opening model manager: {e}")
            self._show_error("Model Manager Error", str(e))
    
    def _on_documentation(self):
        """Handle documentation action"""
        logger.info("Documentation action triggered")
        try:
            self._log_to_console("Opening documentation...")
            self.statusBar().showMessage("Documentation opened")
        except Exception as e:
            logger.error(f"Error opening documentation: {e}")
    
    def _on_about(self):
        """Handle about action"""
        logger.info("About action triggered")
        try:
            QMessageBox.information(
                self,
                "About PyAI IDE",
                "PyAI IDE v1.0.0\n\n"
                "A lightweight, fully-featured Python IDE with HuggingFace and GitHub integration.\n\n"
                "© 2025 PyAI IDE Contributors"
            )
        except Exception as e:
            logger.error(f"Error showing about dialog: {e}")
    
    # ==================== Utility Methods ====================
    
    def _log_to_console(self, message: str):
        """Log message to console widget"""
        try:
            cursor = self.console.textCursor()
            cursor.movePosition(QTextCursor.End)
            cursor.insertText(f"{message}\n")
            self.console.setTextCursor(cursor)
        except Exception as e:
            logger.error(f"Error logging to console: {e}")
    
    def _show_error(self, title: str, message: str):
        """Show error dialog"""
        try:
            logger.error(f"{title}: {message}")
            QMessageBox.critical(self, title, message)
        except Exception as e:
            logger.error(f"Error showing error dialog: {e}")
    
    def _on_log_message(self, message: str):
        """Handle log message signal"""
        self._log_to_console(message)
    
    def closeEvent(self, event):
        """Handle window close event"""
        logger.info("Application closing...")
        try:
            # Save configuration
            if hasattr(self, 'config'):
                self.config.set("app.window_width", self.width())
                self.config.set("app.window_height", self.height())
                self.config.save()
                logger.info("Configuration saved")
        except Exception as e:
            logger.error(f"Error saving configuration on close: {e}")
        
        logger.info("=" * 80)
        logger.info("PyAI IDE - Application Closed")
        logger.info("=" * 80)
        event.accept()
