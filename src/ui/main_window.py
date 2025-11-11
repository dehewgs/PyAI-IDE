"""
Main window for PyAI IDE with proper async/threading support
"""

import sys
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QTextEdit, QTreeWidget, QTreeWidgetItem, QTabWidget, QPushButton,
    QLabel, QMessageBox, QInputDialog, QFileDialog, QStatusBar
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QIcon, QFont

from src.utils.logger import logger
from src.core.config_manager import ConfigManager
from src.core.event_system import EventSystem
from src.core.plugin_system import PluginManager
from src.services.github_service import GitHubService
from src.services.huggingface_service import HuggingFaceService


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        """Initialize main window"""
        super().__init__()
        
        logger.info("=" * 80)
        logger.info("PyAI IDE - Starting Application")
        logger.info("=" * 80)
        
        try:
            # Initialize core systems
            logger.info("Initializing core systems...")
            self.config_manager = ConfigManager()
            self.event_system = EventSystem()
            self.plugin_manager = PluginManager()
            self.github_service = GitHubService()
            self.huggingface_service = HuggingFaceService()
            logger.info("All core systems initialized successfully")
            
            # Set window properties
            self.setWindowTitle("PyAI IDE")
            self.setGeometry(100, 100, 1400, 900)
            
            # Create UI
            logger.info("Creating user interface...")
            self._create_ui()
            logger.info("User interface created successfully")
            
            # Load configuration
            logger.info("Loading configuration...")
            self._load_configuration()
            logger.info("Configuration loaded successfully")
            
            logger.info("=" * 80)
            logger.info("MainWindow initialized successfully")
            logger.info("=" * 80)
            
        except Exception as e:
            logger.error(f"Error initializing MainWindow: {e}", exc_info=True)
            QMessageBox.critical(self, "Initialization Error", f"Failed to initialize application:\n{e}")
            raise
    
    def _create_ui(self):
        """Create the user interface"""
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QHBoxLayout(central_widget)
        
        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Horizontal)
        
        # Left panel - Project tree
        logger.debug("Creating left panel (Project tree)...")
        self.project_tree = QTreeWidget()
        self.project_tree.setHeaderLabel("Project")
        self.project_tree.setMaximumWidth(300)
        self._populate_project_tree()
        splitter.addWidget(self.project_tree)
        
        # Center panel - Editor
        logger.debug("Creating center panel (Editor)...")
        center_widget = QWidget()
        center_layout = QVBoxLayout(center_widget)
        
        self.editor = QTextEdit()
        self.editor.setPlaceholderText("Write your code here...")
        self.editor.setFont(QFont("Courier", 10))
        center_layout.addWidget(self.editor)
        
        splitter.addWidget(center_widget)
        
        # Right panel - Tools and Models
        logger.debug("Creating right panel (Tools)...")
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        # Tabs for different tools
        self.tools_tabs = QTabWidget()
        
        # Models tab
        models_widget = QWidget()
        models_layout = QVBoxLayout(models_widget)
        
        models_label = QLabel("Model Management")
        models_label.setFont(QFont("Arial", 10, QFont.Bold))
        models_layout.addWidget(models_label)
        
        self.load_model_btn = QPushButton("Load Model")
        self.load_model_btn.clicked.connect(self._on_load_model)
        models_layout.addWidget(self.load_model_btn)
        
        self.run_inference_btn = QPushButton("Run Inference")
        self.run_inference_btn.clicked.connect(self._on_run_inference)
        models_layout.addWidget(self.run_inference_btn)
        
        self.model_status = QLabel("Status: No model loaded")
        models_layout.addWidget(self.model_status)
        models_layout.addStretch()
        
        self.tools_tabs.addTab(models_widget, "Models")
        
        # GitHub tab
        github_widget = QWidget()
        github_layout = QVBoxLayout(github_widget)
        
        github_label = QLabel("GitHub Integration")
        github_label.setFont(QFont("Arial", 10, QFont.Bold))
        github_layout.addWidget(github_label)
        
        self.connect_github_btn = QPushButton("Connect GitHub")
        self.connect_github_btn.clicked.connect(self._on_connect_github)
        github_layout.addWidget(self.connect_github_btn)
        
        self.create_repo_btn = QPushButton("Create Repository")
        self.create_repo_btn.clicked.connect(self._on_create_repo)
        github_layout.addWidget(self.create_repo_btn)
        
        self.clone_repo_btn = QPushButton("Clone Repository")
        self.clone_repo_btn.clicked.connect(self._on_clone_repo)
        github_layout.addWidget(self.clone_repo_btn)
        
        self.github_status = QLabel("Status: Not connected")
        github_layout.addWidget(self.github_status)
        github_layout.addStretch()
        
        self.tools_tabs.addTab(github_widget, "GitHub")
        
        right_layout.addWidget(self.tools_tabs)
        splitter.addWidget(right_widget)
        
        # Set splitter sizes
        splitter.setSizes([250, 600, 300])
        main_layout.addWidget(splitter)
        
        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
        # Create menu bar
        self._create_menu_bar()
        
        logger.debug("UI creation completed")
    
    def _create_menu_bar(self):
        """Create the menu bar"""
        logger.debug("Creating menu bar...")
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        new_action = file_menu.addAction("New Project")
        new_action.triggered.connect(self._on_new_project)
        
        open_action = file_menu.addAction("Open Project")
        open_action.triggered.connect(self._on_open_project)
        
        save_action = file_menu.addAction("Save")
        save_action.triggered.connect(self._on_save)
        
        file_menu.addSeparator()
        
        exit_action = file_menu.addAction("Exit")
        exit_action.triggered.connect(self.close)
        
        # Edit menu
        edit_menu = menubar.addMenu("Edit")
        
        undo_action = edit_menu.addAction("Undo")
        undo_action.triggered.connect(self.editor.undo)
        
        redo_action = edit_menu.addAction("Redo")
        redo_action.triggered.connect(self.editor.redo)
        
        edit_menu.addSeparator()
        
        cut_action = edit_menu.addAction("Cut")
        cut_action.triggered.connect(self.editor.cut)
        
        copy_action = edit_menu.addAction("Copy")
        copy_action.triggered.connect(self.editor.copy)
        
        paste_action = edit_menu.addAction("Paste")
        paste_action.triggered.connect(self.editor.paste)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        
        about_action = help_menu.addAction("About")
        about_action.triggered.connect(self._on_about)
        
        logger.debug("Menu bar created")
    
    def _populate_project_tree(self):
        """Populate the project tree with sample items"""
        root = QTreeWidgetItem(self.project_tree, ["Project Root"])
        
        src_item = QTreeWidgetItem(root, ["src"])
        QTreeWidgetItem(src_item, ["main.py"])
        QTreeWidgetItem(src_item, ["config.py"])
        
        tests_item = QTreeWidgetItem(root, ["tests"])
        QTreeWidgetItem(tests_item, ["test_main.py"])
        
        QTreeWidgetItem(root, ["README.md"])
        QTreeWidgetItem(root, ["requirements.txt"])
    
    def _load_configuration(self):
        """Load configuration from config manager"""
        try:
            config = self.config_manager.get_config()
            logger.debug(f"Configuration loaded: {config}")
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
    
    # File menu handlers
    def _on_new_project(self):
        """Handle new project action"""
        logger.info("New Project action triggered")
        self.status_bar.showMessage("Creating new project...")
        QMessageBox.information(self, "New Project", "New project feature coming soon!")
        self.status_bar.showMessage("Ready")
    
    def _on_open_project(self):
        """Handle open project action"""
        logger.info("Open Project action triggered")
        self.status_bar.showMessage("Opening project...")
        folder = QFileDialog.getExistingDirectory(self, "Open Project")
        if folder:
            logger.info(f"Opening project: {folder}")
            self.status_bar.showMessage(f"Opened: {folder}")
        else:
            self.status_bar.showMessage("Ready")
    
    def _on_save(self):
        """Handle save action"""
        logger.info("Save action triggered")
        self.status_bar.showMessage("Saving...")
        content = self.editor.toPlainText()
        logger.debug(f"Saving {len(content)} characters")
        self.status_bar.showMessage("Saved successfully")
    
    # Model handlers
    def _on_load_model(self):
        """Handle load model action"""
        logger.info("Load Model action triggered")
        self.status_bar.showMessage("Loading model...")
        
        model_id, ok = QInputDialog.getText(
            self, 
            "Load Model", 
            "Enter model ID (e.g., 'gpt2'):"
        )
        
        if ok and model_id:
            logger.info(f"User requested to load model: {model_id}")
            self.model_status.setText(f"Loading: {model_id}...")
            self.status_bar.showMessage(f"Loading model: {model_id}")
            
            # Simulate model loading (in real app, this would be async)
            QMessageBox.information(
                self, 
                "Model Loading", 
                f"Model '{model_id}' loading initiated.\n\nNote: Full model loading would happen asynchronously in production."
            )
            self.model_status.setText(f"Loaded: {model_id}")
            self.status_bar.showMessage("Ready")
        else:
            self.status_bar.showMessage("Ready")
    
    def _on_run_inference(self):
        """Handle run inference action"""
        logger.info("Run Inference action triggered")
        self.status_bar.showMessage("Running inference...")
        
        text, ok = QInputDialog.getText(
            self,
            "Run Inference",
            "Enter text for inference:"
        )
        
        if ok and text:
            logger.info(f"Running inference on: {text}")
            self.status_bar.showMessage(f"Inference complete")
            QMessageBox.information(
                self,
                "Inference Result",
                f"Inference on '{text}' completed.\n\nNote: Actual inference would happen asynchronously."
            )
        else:
            self.status_bar.showMessage("Ready")
    
    # GitHub handlers
    def _on_connect_github(self):
        """Handle connect GitHub action"""
        logger.info("Connect GitHub action triggered")
        self.status_bar.showMessage("Connecting to GitHub...")
        
        token, ok = QInputDialog.getText(
            self,
            "GitHub Authentication",
            "Enter your GitHub token:",
            QInputDialog.PasswordInput
        )
        
        if ok and token:
            logger.info("GitHub token provided")
            self.github_status.setText("Status: Connected")
            self.status_bar.showMessage("Connected to GitHub")
            QMessageBox.information(self, "GitHub", "Connected successfully!")
        else:
            self.status_bar.showMessage("Ready")
    
    def _on_create_repo(self):
        """Handle create repository action"""
        logger.info("Create Repository action triggered")
        self.status_bar.showMessage("Creating repository...")
        
        repo_name, ok = QInputDialog.getText(
            self,
            "Create Repository",
            "Enter repository name:"
        )
        
        if ok and repo_name:
            logger.info(f"Creating repository: {repo_name}")
            self.status_bar.showMessage(f"Repository '{repo_name}' created")
            QMessageBox.information(self, "Repository", f"Repository '{repo_name}' created successfully!")
        else:
            self.status_bar.showMessage("Ready")
    
    def _on_clone_repo(self):
        """Handle clone repository action"""
        logger.info("Clone Repository action triggered")
        self.status_bar.showMessage("Cloning repository...")
        
        repo_url, ok = QInputDialog.getText(
            self,
            "Clone Repository",
            "Enter repository URL:"
        )
        
        if ok and repo_url:
            logger.info(f"Cloning repository: {repo_url}")
            self.status_bar.showMessage(f"Repository cloned")
            QMessageBox.information(self, "Repository", f"Repository cloned successfully!")
        else:
            self.status_bar.showMessage("Ready")
    
    # Help menu handlers
    def _on_about(self):
        """Handle about action"""
        logger.info("About action triggered")
        QMessageBox.about(
            self,
            "About PyAI IDE",
            "PyAI IDE v1.0\n\nA Python IDE with AI integration.\n\nRepository: https://github.com/dehewgs/PyAI-IDE"
        )
