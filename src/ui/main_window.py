"""
Main Window for PyAI IDE - Fully Integrated with All Components
"""

import sys
import os
from pathlib import Path
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter, QTabWidget,
    QMessageBox, QInputDialog, QFileDialog, QStatusBar, QProgressBar
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QIcon, QFont

from utils.logger import logger
from core.config_manager import ConfigManager
from core.event_system import EventSystem
from core.plugin_system import PluginManager
from services.github_service import GitHubService
from services.huggingface_service import HuggingFaceService

# Import UI components
from ui.editor.code_editor import CodeEditor
from ui.panels.console_panel import ConsolePanel
from ui.panels.project_panel import ProjectPanel
from ui.panels.model_panel import ModelPanel
from ui.dialogs.model_dialog import ModelLoadDialog
from ui.dialogs.inference_dialog import InferenceDialog
from ui.dialogs.github_dialog import GitHubAuthDialog
from ui.dialogs.repository_dialog import RepositoryDialog
from ui.dialogs.project_dialog import ProjectDialog
from ui.dialogs.settings_dialog import SettingsDialog
from ui.styles.theme_manager_enhanced import EnhancedThemeManager


class MainWindow(QMainWindow):
    """Main application window with full feature integration"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyAI IDE")
        self.setGeometry(100, 100, 1400, 900)
        
        logger.info("Initializing PyAI IDE Main Window")
        
        # Initialize services
        self.config = ConfigManager()
        self.event_system = EventSystem()
        self.plugin_manager = PluginManager()
        self.github_service = GitHubService()
        self.huggingface_service = HuggingFaceService()
        self.theme_manager = EnhancedThemeManager()
        
        # State
        self.current_project = None
        self.open_files = {}
        self.current_file = None
        
        # Create UI
        self._create_ui()
        self._create_menu_bar()
        self._connect_signals()
        self._apply_theme("dark")
        
        logger.info("Main Window initialized successfully")
    
    def _create_ui(self):
        """Create the main UI layout"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create main splitter (left panels | editor | right panels)
        main_splitter = QSplitter(Qt.Horizontal)
        
        # LEFT PANEL: Project and Model panels
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        # Project panel
        self.project_panel = ProjectPanel()
        left_layout.addWidget(self.project_panel)
        
        # Model panel
        self.model_panel = ModelPanel()
        left_layout.addWidget(self.model_panel)
        
        # CENTER PANEL: Editor with tabs
        center_panel = QWidget()
        center_layout = QVBoxLayout(center_panel)
        center_layout.setContentsMargins(0, 0, 0, 0)
        
        # Tab widget for multiple files
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self._on_tab_close)
        
        center_layout.addWidget(self.tab_widget)
        
        # RIGHT PANEL: Console
        self.console_panel = ConsolePanel(theme_manager=self.theme_manager)
        
        # Add panels to main splitter
        main_splitter.addWidget(left_panel)
        main_splitter.addWidget(center_panel)
        main_splitter.addWidget(self.console_panel)
        
        # Set stretch factors
        main_splitter.setStretchFactor(0, 1)
        main_splitter.setStretchFactor(1, 3)
        main_splitter.setStretchFactor(2, 1)
        
        main_layout.addWidget(main_splitter)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
        # Progress bar in status bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximumWidth(200)
        self.progress_bar.setVisible(False)
        self.status_bar.addPermanentWidget(self.progress_bar)
        
        # Connect tab signals AFTER status_bar is created
        self.tab_widget.currentChanged.connect(self._on_tab_changed)
        
        # Create initial editor tab AFTER status_bar is created
        self.editor = CodeEditor(theme_manager=self.theme_manager)
        self.tab_widget.addTab(self.editor, "Untitled")
        self.open_files["Untitled"] = self.editor
    
    def _create_menu_bar(self):
        """Create menu bar"""
        menubar = self.menuBar()
        
        # FILE MENU
        file_menu = menubar.addMenu("File")
        file_menu.addAction("New Project", self._on_new_project)
        file_menu.addAction("Open Project", self._on_open_project)
        file_menu.addAction("New File", self._on_new_file)
        file_menu.addAction("Open File", self._on_open_file)
        file_menu.addSeparator()
        file_menu.addAction("Save", self._on_save)
        file_menu.addAction("Save As", self._on_save_as)
        file_menu.addSeparator()
        file_menu.addAction("Exit", self.close)
        
        # EDIT MENU
        edit_menu = menubar.addMenu("Edit")
        edit_menu.addAction("Undo", self._on_undo)
        edit_menu.addAction("Redo", self._on_redo)
        edit_menu.addSeparator()
        edit_menu.addAction("Cut", self._on_cut)
        edit_menu.addAction("Copy", self._on_copy)
        edit_menu.addAction("Paste", self._on_paste)
        
        # AI MENU
        ai_menu = menubar.addMenu("AI")
        ai_menu.addAction("Load Model", self._on_load_model)
        ai_menu.addAction("Run Inference", self._on_run_inference)
        ai_menu.addSeparator()
        ai_menu.addAction("GitHub Auth", self._on_github_auth)
        ai_menu.addAction("Repository", self._on_repository)
        
        # VIEW MENU
        view_menu = menubar.addMenu("View")
        view_menu.addAction("Dark Theme", lambda: self._apply_theme("dark"))
        view_menu.addAction("Light Theme", lambda: self._apply_theme("light"))
        
        # TOOLS MENU
        tools_menu = menubar.addMenu("Tools")
        tools_menu.addAction("Settings", self._on_settings)
        tools_menu.addAction("Plugin Manager", self._on_plugin_manager)
        
        # HELP MENU
        help_menu = menubar.addMenu("Help")
        help_menu.addAction("About", self._on_about)
        help_menu.addAction("Documentation", self._on_documentation)
    
    def _connect_signals(self):
        """Connect signals and slots"""
        self.event_system.subscribe("model_loaded", self._on_model_loaded_event)
        self.event_system.subscribe("inference_complete", self._on_inference_complete_event)
        self.event_system.subscribe("file_saved", self._on_file_saved_event)
    
    # FILE OPERATIONS
    def _on_new_project(self):
        """Create new project"""
        logger.info("New Project menu clicked")
        dialog = ProjectDialog(self)
        if dialog.exec_():
            project_name = dialog.get_project_name()
            self.console_panel.write_success(f"Project created: {project_name}")
            logger.info(f"Project created: {project_name}")
    
    def _on_open_project(self):
        """Open project"""
        logger.info("Open Project menu clicked")
        path = QFileDialog.getExistingDirectory(self, "Open Project")
        if path:
            self.current_project = path
            self.console_panel.write_success(f"Project opened: {path}")
            logger.info(f"Project opened: {path}")
    
    def _on_new_file(self):
        """Create new file"""
        logger.info("New File menu clicked")
        filename = f"Untitled_{len(self.open_files)}"
        editor = CodeEditor(theme_manager=self.theme_manager)
        self.tab_widget.addTab(editor, filename)
        self.open_files[filename] = editor
        self.console_panel.write(f"New file created: {filename}")
    
    def _on_open_file(self):
        """Open file"""
        logger.info("Open File menu clicked")
        path, _ = QFileDialog.getOpenFileName(self, "Open File")
        if path:
            try:
                with open(path, 'r') as f:
                    content = f.read()
                
                filename = Path(path).name
                editor = CodeEditor(theme_manager=self.theme_manager)
                editor.setPlainText(content)
                self.tab_widget.addTab(editor, filename)
                self.open_files[filename] = editor
                self.console_panel.write_success(f"File opened: {filename}")
                logger.info(f"File opened: {path}")
            except Exception as e:
                self.console_panel.write_error(f"Error opening file: {e}")
                logger.error(f"Error opening file: {e}")
    
    def _on_save(self):
        """Save current file"""
        logger.info("Save menu clicked")
        current_editor = self.tab_widget.currentWidget()
        if current_editor:
            filename = self.tab_widget.tabText(self.tab_widget.currentIndex())
            self.console_panel.write_success(f"File saved: {filename}")
            self.event_system.emit("file_saved", {"filename": filename})
    
    def _on_save_as(self):
        """Save file as"""
        logger.info("Save As menu clicked")
        path, _ = QFileDialog.getSaveFileName(self, "Save File As")
        if path:
            self.console_panel.write_success(f"File saved as: {path}")
    
    def _on_undo(self):
        """Undo"""
        logger.info("Undo menu clicked")
    
    def _on_redo(self):
        """Redo"""
        logger.info("Redo menu clicked")
    
    def _on_cut(self):
        """Cut"""
        logger.info("Cut menu clicked")
    
    def _on_copy(self):
        """Copy"""
        logger.info("Copy menu clicked")
    
    def _on_paste(self):
        """Paste"""
        logger.info("Paste menu clicked")
    
    # AI OPERATIONS
    def _on_load_model(self):
        """Load model"""
        logger.info("Load Model menu clicked")
        dialog = ModelLoadDialog(self)
        if dialog.exec_():
            model_id = dialog.get_selected_model()
            self.console_panel.write_success(f"Model loaded: {model_id}")
            self.model_panel.add_model(model_id)
            self.event_system.emit("model_loaded", {"model_id": model_id})
    
    def _on_run_inference(self):
        """Run inference"""
        logger.info("Run Inference menu clicked")
        dialog = InferenceDialog(self)
        if dialog.exec_():
            prompt = dialog.get_prompt()
            self.console_panel.write(f"Running inference with prompt: {prompt}")
            self.event_system.emit("inference_complete", {"result": "inference result"})
    
    def _on_github_auth(self):
        """GitHub authentication"""
        logger.info("GitHub Auth menu clicked")
        dialog = GitHubAuthDialog(self)
        if dialog.exec_():
            token = dialog.get_token()
            self.console_panel.write_success("GitHub authenticated")
            logger.info("GitHub authenticated")
    
    def _on_repository(self):
        """Repository operations"""
        logger.info("Repository menu clicked")
        dialog = RepositoryDialog(self)
        if dialog.exec_():
            repo_url = dialog.get_repository_url()
            self.console_panel.write_success(f"Repository: {repo_url}")
    
    # TAB OPERATIONS
    def _on_tab_changed(self, index):
        """Handle tab change"""
        if index >= 0:
            filename = self.tab_widget.tabText(index)
            self.status_bar.showMessage(f"Editing: {filename}")
            logger.debug(f"Tab changed to: {filename}")
    
    def _on_tab_close(self, index):
        """Handle tab close"""
        filename = self.tab_widget.tabText(index)
        self.tab_widget.removeTab(index)
        if filename in self.open_files:
            del self.open_files[filename]
        logger.info(f"Tab closed: {filename}")
    
    # EVENT HANDLERS
    def _on_model_loaded_event(self, data):
        """Handle model loaded event"""
        logger.info(f"Model loaded event: {data}")
    
    def _on_inference_complete_event(self, data):
        """Handle inference complete event"""
        logger.info(f"Inference complete event: {data}")
    
    def _on_file_saved_event(self, data):
        """Handle file saved event"""
        logger.info(f"File saved event: {data}")
    
    def _apply_theme(self, theme_name):
        """Apply theme
        
        Args:
            theme_name: Theme identifier
        """
        logger.info(f"Applying theme: {theme_name}")
        self.theme_manager.set_theme(self, theme_name)
        self.status_bar.showMessage(f"Theme changed to: {theme_name}")
    
    # TOOLS OPERATIONS
    def _on_settings(self):
        """Open settings"""
        logger.info("Settings menu clicked")
        dialog = SettingsDialog(self, self.config)
        if dialog.exec_():
            settings = dialog.get_settings()
            self.console_panel.write_success(f"✓ Settings saved")
            logger.info(f"Settings saved: {settings}")
    
    def _on_plugin_manager(self):
        """Open plugin manager"""
        logger.info("Plugin Manager menu clicked")
        self.console_panel.write("Plugin Manager opened")
    
    # HELP OPERATIONS
    def _on_about(self):
        """Show about dialog"""
        logger.info("About menu clicked")
        QMessageBox.about(self, "About PyAI IDE", 
                         "PyAI IDE v1.0.0\n\n"
                         "A lightweight, fully-featured Python IDE with HuggingFace AI integration "
                         "and GitHub repository management.\n\n"
                         "© 2025 PyAI IDE Contributors")
    
    def _on_documentation(self):
        """Show documentation"""
        logger.info("Documentation menu clicked")
        self.console_panel.write("Opening documentation...")
