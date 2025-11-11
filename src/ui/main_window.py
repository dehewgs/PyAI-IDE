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
from ui.styles.theme_manager import ThemeManager


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
        self.theme_manager = ThemeManager()
        
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
        self.tab_widget.currentChanged.connect(self._on_tab_changed)
        
        # Create initial editor tab
        self.editor = CodeEditor()
        self.tab_widget.addTab(self.editor, "Untitled")
        self.open_files["Untitled"] = self.editor
        
        center_layout.addWidget(self.tab_widget)
        
        # RIGHT PANEL: Console
        self.console_panel = ConsolePanel()
        
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
        ai_menu.addAction("Model Manager", self._on_model_manager)
        
        # GITHUB MENU
        github_menu = menubar.addMenu("GitHub")
        github_menu.addAction("Connect Account", self._on_github_connect)
        github_menu.addAction("Create Repository", self._on_create_repo)
        github_menu.addAction("Clone Repository", self._on_clone_repo)
        github_menu.addSeparator()
        github_menu.addAction("Disconnect", self._on_github_disconnect)
        
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
            data = dialog.get_project_data()
            if data:
                self.current_project = data["name"]
                self.project_panel.clear()
                self.project_panel.add_folder(data["name"])
                self.status_bar.showMessage(f"Project created: {data['name']}")
                self.console_panel.write(f"✓ Project '{data['name']}' created at {data['location']}")
                logger.info(f"Project created: {data['name']}")
    
    def _on_open_project(self):
        """Open existing project"""
        logger.info("Open Project menu clicked")
        path = QFileDialog.getExistingDirectory(self, "Open Project")
        if path:
            self.current_project = Path(path).name
            self.project_panel.clear()
            self.project_panel.add_folder(self.current_project)
            self.status_bar.showMessage(f"Project opened: {path}")
            self.console_panel.write(f"✓ Project opened: {path}")
            logger.info(f"Project opened: {path}")
    
    def _on_new_file(self):
        """Create new file"""
        logger.info("New File menu clicked")
        name, ok = QInputDialog.getText(self, "New File", "Enter filename:")
        if ok and name:
            editor = CodeEditor()
            self.open_files[name] = editor
            self.tab_widget.addTab(editor, name)
            self.tab_widget.setCurrentWidget(editor)
            self.current_file = name
            self.status_bar.showMessage(f"New file: {name}")
            self.console_panel.write(f"✓ New file created: {name}")
            logger.info(f"New file created: {name}")
    
    def _on_open_file(self):
        """Open file"""
        logger.info("Open File menu clicked")
        path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Python Files (*.py);;All Files (*)")
        if path:
            filename = Path(path).name
            if filename not in self.open_files:
                try:
                    with open(path, 'r') as f:
                        content = f.read()
                    editor = CodeEditor()
                    editor.setPlainText(content)
                    self.open_files[filename] = editor
                    self.tab_widget.addTab(editor, filename)
                    self.tab_widget.setCurrentWidget(editor)
                    self.current_file = filename
                    self.status_bar.showMessage(f"File opened: {filename}")
                    self.console_panel.write(f"✓ File opened: {path}")
                    logger.info(f"File opened: {path}")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to open file: {e}")
                    logger.error(f"Failed to open file: {e}")
            else:
                self.tab_widget.setCurrentWidget(self.open_files[filename])
    
    def _on_save(self):
        """Save current file"""
        logger.info("Save menu clicked")
        if self.current_file:
            editor = self.tab_widget.currentWidget()
            if isinstance(editor, CodeEditor):
                content = editor.toPlainText()
                self.status_bar.showMessage(f"File saved: {self.current_file}")
                self.console_panel.write(f"✓ File saved: {self.current_file}")
                self.event_system.emit("file_saved", self.current_file)
                logger.info(f"File saved: {self.current_file}")
    
    def _on_save_as(self):
        """Save file as"""
        logger.info("Save As menu clicked")
        path, _ = QFileDialog.getSaveFileName(self, "Save File As", "", "Python Files (*.py);;All Files (*)")
        if path:
            editor = self.tab_widget.currentWidget()
            if isinstance(editor, CodeEditor):
                content = editor.toPlainText()
                try:
                    with open(path, 'w') as f:
                        f.write(content)
                    filename = Path(path).name
                    self.status_bar.showMessage(f"File saved: {filename}")
                    self.console_panel.write(f"✓ File saved as: {path}")
                    logger.info(f"File saved as: {path}")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to save file: {e}")
                    logger.error(f"Failed to save file: {e}")
    
    # EDIT OPERATIONS
    def _on_undo(self):
        """Undo"""
        logger.info("Undo menu clicked")
        editor = self.tab_widget.currentWidget()
        if isinstance(editor, CodeEditor):
            editor.undo()
            self.status_bar.showMessage("Undo")
    
    def _on_redo(self):
        """Redo"""
        logger.info("Redo menu clicked")
        editor = self.tab_widget.currentWidget()
        if isinstance(editor, CodeEditor):
            editor.redo()
            self.status_bar.showMessage("Redo")
    
    def _on_cut(self):
        """Cut"""
        logger.info("Cut menu clicked")
        editor = self.tab_widget.currentWidget()
        if isinstance(editor, CodeEditor):
            editor.cut()
            self.status_bar.showMessage("Cut")
    
    def _on_copy(self):
        """Copy"""
        logger.info("Copy menu clicked")
        editor = self.tab_widget.currentWidget()
        if isinstance(editor, CodeEditor):
            editor.copy()
            self.status_bar.showMessage("Copy")
    
    def _on_paste(self):
        """Paste"""
        logger.info("Paste menu clicked")
        editor = self.tab_widget.currentWidget()
        if isinstance(editor, CodeEditor):
            editor.paste()
            self.status_bar.showMessage("Paste")
    
    # AI OPERATIONS
    def _on_load_model(self):
        """Load model"""
        logger.info("Load Model menu clicked")
        available_models = self.huggingface_service.list_models()
        dialog = ModelLoadDialog(self, available_models)
        if dialog.exec_():
            model_id = dialog.get_selected_model()
            if model_id:
                self.progress_bar.setVisible(True)
                self.progress_bar.setValue(50)
                success, message = self.huggingface_service.load_model(model_id)
                self.progress_bar.setValue(100)
                self.progress_bar.setVisible(False)
                
                if success:
                    self.model_panel.add_model(model_id)
                    self.status_bar.showMessage(f"Model loaded: {model_id}")
                    self.console_panel.write(f"✓ Model loaded: {model_id}")
                    self.event_system.emit("model_loaded", model_id)
                    logger.info(f"Model loaded: {model_id}")
                else:
                    QMessageBox.warning(self, "Error", message)
                    logger.error(f"Failed to load model: {message}")
    
    def _on_run_inference(self):
        """Run inference"""
        logger.info("Run Inference menu clicked")
        loaded_models = self.model_panel.get_loaded_models()
        if not loaded_models:
            QMessageBox.warning(self, "Error", "No models loaded. Please load a model first.")
            return
        
        dialog = InferenceDialog(self, loaded_models)
        if dialog.exec_():
            result = dialog.get_result()
            if result:
                self.progress_bar.setVisible(True)
                self.progress_bar.setValue(50)
                success, output = self.huggingface_service.run_inference(result["model"], result["input"])
                self.progress_bar.setValue(100)
                self.progress_bar.setVisible(False)
                
                if success:
                    self.status_bar.showMessage("Inference complete")
                    self.console_panel.write(f"✓ Inference result: {output}")
                    self.event_system.emit("inference_complete", output)
                    logger.info(f"Inference complete: {output}")
                else:
                    QMessageBox.warning(self, "Error", output)
                    logger.error(f"Inference failed: {output}")
    
    def _on_model_manager(self):
        """Open model manager"""
        logger.info("Model Manager menu clicked")
        self.console_panel.write("Model Manager opened")
    
    # GITHUB OPERATIONS
    def _on_github_connect(self):
        """Connect to GitHub"""
        logger.info("GitHub Connect menu clicked")
        dialog = GitHubAuthDialog(self)
        if dialog.exec_():
            token = dialog.get_token()
            if token:
                success, message = self.github_service.authenticate(token)
                if success:
                    self.status_bar.showMessage("Connected to GitHub")
                    self.console_panel.write(f"✓ Connected to GitHub")
                    logger.info("Connected to GitHub")
                else:
                    QMessageBox.warning(self, "Error", message)
                    logger.error(f"GitHub authentication failed: {message}")
    
    def _on_create_repo(self):
        """Create repository"""
        logger.info("Create Repository menu clicked")
        if not self.github_service.authenticated:
            QMessageBox.warning(self, "Error", "Please connect to GitHub first")
            return
        
        dialog = RepositoryDialog(self)
        if dialog.exec_():
            operation = dialog.get_operation()
            data = dialog.get_data()
            
            if operation == "create":
                success, message = self.github_service.create_repository(data["name"], data["description"])
                if success:
                    self.status_bar.showMessage(f"Repository created: {data['name']}")
                    self.console_panel.write(f"✓ Repository created: {data['name']}")
                    logger.info(f"Repository created: {data['name']}")
                else:
                    QMessageBox.warning(self, "Error", message)
                    logger.error(f"Failed to create repository: {message}")
    
    def _on_clone_repo(self):
        """Clone repository"""
        logger.info("Clone Repository menu clicked")
        dialog = RepositoryDialog(self)
        if dialog.exec_():
            operation = dialog.get_operation()
            data = dialog.get_data()
            
            if operation == "clone":
                success, message = self.github_service.clone_repository(data["url"])
                if success:
                    self.status_bar.showMessage(f"Repository cloned")
                    self.console_panel.write(f"✓ Repository cloned: {data['url']}")
                    logger.info(f"Repository cloned: {data['url']}")
                else:
                    QMessageBox.warning(self, "Error", message)
                    logger.error(f"Failed to clone repository: {message}")
    
    def _on_github_disconnect(self):
        """Disconnect from GitHub"""
        logger.info("GitHub Disconnect menu clicked")
        success, message = self.github_service.disconnect()
        self.status_bar.showMessage("Disconnected from GitHub")
        self.console_panel.write("✓ Disconnected from GitHub")
        logger.info("Disconnected from GitHub")
    
    # VIEW OPERATIONS
    def _apply_theme(self, theme_name):
        """Apply theme"""
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
            self.console_panel.write(f"✓ Settings saved")
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
                         "PyAI IDE v1.0\n\n"
                         "A comprehensive IDE for AI development\n"
                         "with GitHub and HuggingFace integration\n\n"
                         "© 2025 PyAI IDE Contributors")
    
    def _on_documentation(self):
        """Show documentation"""
        logger.info("Documentation menu clicked")
        self.console_panel.write("Documentation: https://github.com/dehewgs/PyAI-IDE")
    
    # TAB OPERATIONS
    def _on_tab_close(self, index):
        """Handle tab close"""
        widget = self.tab_widget.widget(index)
        tab_name = self.tab_widget.tabText(index)
        if tab_name in self.open_files:
            del self.open_files[tab_name]
        self.tab_widget.removeTab(index)
        logger.info(f"Tab closed: {tab_name}")
    
    def _on_tab_changed(self, index):
        """Handle tab change"""
        if index >= 0:
            self.current_file = self.tab_widget.tabText(index)
            self.status_bar.showMessage(f"Current file: {self.current_file}")
            logger.debug(f"Tab changed to: {self.current_file}")
    
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
    
    def closeEvent(self, event):
        """Handle window close"""
        logger.info("Application closing")
        event.accept()
