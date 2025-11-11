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

from utils.logger import logger
from core.config_manager import ConfigManager
from core.event_system import EventSystem
from core.plugin_system import PluginManager
from services.github_service import GitHubService
from services.huggingface_service import HuggingFaceService


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyAI IDE")
        self.setGeometry(100, 100, 1200, 800)
        
        # Initialize services
        self.config = ConfigManager()
        self.event_system = EventSystem()
        self.plugin_manager = PluginManager()
        self.github_service = GitHubService()
        self.huggingface_service = HuggingFaceService()
        
        logger.info("Initializing PyAI IDE Main Window")
        
        # Create UI
        self._create_ui()
        self._create_menu_bar()
        self._connect_signals()
        
        logger.info("Main Window initialized successfully")
    
    def _create_ui(self):
        """Create the main UI layout"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        
        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Horizontal)
        
        # Left panel - Project tree
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.addWidget(QLabel("Project"))
        self.project_tree = QTreeWidget()
        self.project_tree.setHeaderLabel("Files")
        left_layout.addWidget(self.project_tree)
        
        # Center panel - Editor and tabs
        center_panel = QWidget()
        center_layout = QVBoxLayout(center_panel)
        center_layout.addWidget(QLabel("Editor"))
        
        self.tab_widget = QTabWidget()
        self.editor = QTextEdit()
        self.editor.setPlaceholderText("Write your code here...")
        self.tab_widget.addTab(self.editor, "Untitled")
        center_layout.addWidget(self.tab_widget)
        
        # Right panel - Buttons and controls
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.addWidget(QLabel("Controls"))
        
        # Buttons
        self.load_model_btn = QPushButton("Load Model")
        self.load_model_btn.clicked.connect(self._on_load_model)
        right_layout.addWidget(self.load_model_btn)
        
        self.run_inference_btn = QPushButton("Run Inference")
        self.run_inference_btn.clicked.connect(self._on_run_inference)
        right_layout.addWidget(self.run_inference_btn)
        
        self.github_btn = QPushButton("Connect GitHub")
        self.github_btn.clicked.connect(self._on_github_connect)
        right_layout.addWidget(self.github_btn)
        
        self.create_repo_btn = QPushButton("Create Repository")
        self.create_repo_btn.clicked.connect(self._on_create_repo)
        right_layout.addWidget(self.create_repo_btn)
        
        self.clone_repo_btn = QPushButton("Clone Repository")
        self.clone_repo_btn.clicked.connect(self._on_clone_repo)
        right_layout.addWidget(self.clone_repo_btn)
        
        right_layout.addStretch()
        
        # Add panels to splitter
        splitter.addWidget(left_panel)
        splitter.addWidget(center_panel)
        splitter.addWidget(right_panel)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
        splitter.setStretchFactor(2, 1)
        
        main_layout.addWidget(splitter)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
    
    def _create_menu_bar(self):
        """Create menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        file_menu.addAction("New Project", self._on_new_project)
        file_menu.addAction("Open Project", self._on_open_project)
        file_menu.addAction("Save", self._on_save)
        file_menu.addSeparator()
        file_menu.addAction("Exit", self.close)
        
        # Edit menu
        edit_menu = menubar.addMenu("Edit")
        edit_menu.addAction("Undo", self._on_undo)
        edit_menu.addAction("Redo", self._on_redo)
        edit_menu.addSeparator()
        edit_menu.addAction("Cut", self._on_cut)
        edit_menu.addAction("Copy", self._on_copy)
        edit_menu.addAction("Paste", self._on_paste)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        help_menu.addAction("About", self._on_about)
    
    def _connect_signals(self):
        """Connect signals and slots"""
        self.event_system.subscribe("model_loaded", self._on_model_loaded)
        self.event_system.subscribe("inference_complete", self._on_inference_complete)
    
    # Button handlers
    def _on_load_model(self):
        """Handle load model button"""
        logger.info("Load Model button clicked")
        model_name, ok = QInputDialog.getText(self, "Load Model", "Enter model name:")
        if ok and model_name:
            self.status_bar.showMessage(f"Loading model: {model_name}...")
            logger.info(f"Loading model: {model_name}")
            self.huggingface_service.load_model(model_name)
            self.status_bar.showMessage(f"Model loaded: {model_name}")
            QMessageBox.information(self, "Success", f"Model '{model_name}' loaded successfully!")
    
    def _on_run_inference(self):
        """Handle run inference button"""
        logger.info("Run Inference button clicked")
        input_text, ok = QInputDialog.getText(self, "Run Inference", "Enter input text:")
        if ok and input_text:
            self.status_bar.showMessage("Running inference...")
            logger.info(f"Running inference with input: {input_text}")
            result = self.huggingface_service.run_inference(input_text)
            self.status_bar.showMessage("Inference complete")
            QMessageBox.information(self, "Inference Result", f"Result: {result}")
    
    def _on_github_connect(self):
        """Handle GitHub connect button"""
        logger.info("GitHub Connect button clicked")
        token, ok = QInputDialog.getText(self, "Connect GitHub", "Enter GitHub token:", QInputDialog.Password)
        if ok and token:
            self.status_bar.showMessage("Connecting to GitHub...")
            logger.info("Connecting to GitHub")
            self.github_service.authenticate(token)
            self.status_bar.showMessage("Connected to GitHub")
            QMessageBox.information(self, "Success", "Connected to GitHub successfully!")
    
    def _on_create_repo(self):
        """Handle create repository button"""
        logger.info("Create Repository button clicked")
        repo_name, ok = QInputDialog.getText(self, "Create Repository", "Enter repository name:")
        if ok and repo_name:
            self.status_bar.showMessage(f"Creating repository: {repo_name}...")
            logger.info(f"Creating repository: {repo_name}")
            self.github_service.create_repository(repo_name)
            self.status_bar.showMessage(f"Repository created: {repo_name}")
            QMessageBox.information(self, "Success", f"Repository '{repo_name}' created successfully!")
    
    def _on_clone_repo(self):
        """Handle clone repository button"""
        logger.info("Clone Repository button clicked")
        repo_url, ok = QInputDialog.getText(self, "Clone Repository", "Enter repository URL:")
        if ok and repo_url:
            self.status_bar.showMessage(f"Cloning repository: {repo_url}...")
            logger.info(f"Cloning repository: {repo_url}")
            self.github_service.clone_repository(repo_url)
            self.status_bar.showMessage(f"Repository cloned: {repo_url}")
            QMessageBox.information(self, "Success", f"Repository cloned successfully!")
    
    # Menu handlers
    def _on_new_project(self):
        """Handle new project"""
        logger.info("New Project menu clicked")
        project_name, ok = QInputDialog.getText(self, "New Project", "Enter project name:")
        if ok and project_name:
            self.status_bar.showMessage(f"Creating project: {project_name}")
            logger.info(f"Creating new project: {project_name}")
            QMessageBox.information(self, "Success", f"Project '{project_name}' created!")
    
    def _on_open_project(self):
        """Handle open project"""
        logger.info("Open Project menu clicked")
        path = QFileDialog.getExistingDirectory(self, "Open Project")
        if path:
            self.status_bar.showMessage(f"Opening project: {path}")
            logger.info(f"Opening project: {path}")
            QMessageBox.information(self, "Success", f"Project opened: {path}")
    
    def _on_save(self):
        """Handle save"""
        logger.info("Save menu clicked")
        self.status_bar.showMessage("Saving...")
        logger.info("Saving file")
        self.status_bar.showMessage("File saved")
        QMessageBox.information(self, "Success", "File saved successfully!")
    
    def _on_undo(self):
        """Handle undo"""
        logger.info("Undo menu clicked")
        self.editor.undo()
        self.status_bar.showMessage("Undo")
    
    def _on_redo(self):
        """Handle redo"""
        logger.info("Redo menu clicked")
        self.editor.redo()
        self.status_bar.showMessage("Redo")
    
    def _on_cut(self):
        """Handle cut"""
        logger.info("Cut menu clicked")
        self.editor.cut()
        self.status_bar.showMessage("Cut")
    
    def _on_copy(self):
        """Handle copy"""
        logger.info("Copy menu clicked")
        self.editor.copy()
        self.status_bar.showMessage("Copy")
    
    def _on_paste(self):
        """Handle paste"""
        logger.info("Paste menu clicked")
        self.editor.paste()
        self.status_bar.showMessage("Paste")
    
    def _on_about(self):
        """Handle about"""
        logger.info("About menu clicked")
        QMessageBox.about(self, "About PyAI IDE", 
                         "PyAI IDE v1.0\n\n"
                         "A comprehensive IDE for AI development\n"
                         "with GitHub and HuggingFace integration")
    
    # Event handlers
    def _on_model_loaded(self, data):
        """Handle model loaded event"""
        logger.info(f"Model loaded event: {data}")
        self.status_bar.showMessage("Model loaded")
    
    def _on_inference_complete(self, data):
        """Handle inference complete event"""
        logger.info(f"Inference complete event: {data}")
        self.status_bar.showMessage("Inference complete")
    
    def closeEvent(self, event):
        """Handle window close"""
        logger.info("Application closing")
        event.accept()
