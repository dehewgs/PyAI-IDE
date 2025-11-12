"""
Main Window for PyAI IDE - Fully Integrated with All Components
Includes: AppData management, Code execution, Keyboard shortcuts, Enhanced project tree
"""

import sys
import os
from pathlib import Path
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter, QTabWidget,
    QMessageBox, QInputDialog, QFileDialog, QStatusBar, QProgressBar, QShortcut
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer, QEvent
from PyQt5.QtGui import QIcon, QFont, QKeySequence

from utils.logger import logger
from core.config_manager import ConfigManager
from core.event_system import EventSystem
from core.plugin_system import PluginManager
from core.app_data_manager import AppDataManager
from core.code_executor import CodeExecutor
from core.shortcuts_manager import ShortcutsManager, ShortcutHandler
from services.github_service import GitHubService
from services.huggingface_service import HuggingFaceService

# Import UI components
from ui.editor.code_editor import CodeEditor
from ui.panels.console_panel import ConsolePanel
from ui.panels.enhanced_project_panel import EnhancedProjectPanel
from ui.panels.model_panel import ModelPanel
from ui.dialogs.model_dialog import ModelLoadDialog
from ui.dialogs.inference_dialog import InferenceDialog
from ui.dialogs.github_dialog import GitHubAuthDialog
from ui.dialogs.repository_dialog import RepositoryDialog
from ui.dialogs.project_dialog import ProjectDialog
from ui.dialogs.settings_dialog_enhanced import EnhancedSettingsDialog
from ui.styles.theme_manager_enhanced import EnhancedThemeManager


class MainWindow(QMainWindow):
    """Main application window with full feature integration"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyAI IDE")
        self.setGeometry(100, 100, 1400, 900)
        
        logger.info("Initializing PyAI IDE Main Window")
        
        # Initialize managers
        self.app_data_manager = AppDataManager()
        self.config = ConfigManager()
        self.event_system = EventSystem()
        self.plugin_manager = PluginManager()
        self.github_service = GitHubService()
        self.huggingface_service = HuggingFaceService()
        self.theme_manager = EnhancedThemeManager()
        
        # Initialize execution and shortcuts
        self.code_executor = CodeExecutor()
        self.shortcuts_manager = ShortcutsManager(self.app_data_manager)
        self.shortcut_handler = ShortcutHandler(self.shortcuts_manager)
        
        # State
        self.current_project = None
        self.open_files = {}
        self.current_file = None
        
        # Create UI
        self._create_ui()
        self._create_menu_bar()
        self._setup_shortcuts()
        self._connect_signals()
        self._restore_window_state()
        
        # Apply saved theme
        saved_theme = self.app_data_manager.get_config_value('theme', 'dark')
        self._apply_theme(saved_theme)
        
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
        
        # Enhanced Project panel with file operations
        self.project_panel = EnhancedProjectPanel(theme_manager=self.theme_manager)
        self.theme_manager.register_component(self.project_panel)
        self.project_panel.file_selected.connect(self._on_file_selected)
        self.project_panel.file_created.connect(self._on_file_created)
        self.project_panel.file_deleted.connect(self._on_file_deleted)
        left_layout.addWidget(self.project_panel)
        
        # Model panel
        self.model_panel = ModelPanel(theme_manager=self.theme_manager)
        self.theme_manager.register_component(self.model_panel)
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
        center_layout.addWidget(self.tab_widget)
        
        # Console panel
        self.console_panel = ConsolePanel(theme_manager=self.theme_manager)
        self.theme_manager.register_component(self.console_panel)
        center_layout.addWidget(self.console_panel, 1)
        
        # RIGHT PANEL: Placeholder for future features
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        # Add panels to splitter
        main_splitter.addWidget(left_panel)
        main_splitter.addWidget(center_panel)
        main_splitter.addWidget(right_panel)
        main_splitter.setStretchFactor(0, 1)
        main_splitter.setStretchFactor(1, 2)
        main_splitter.setStretchFactor(2, 1)
        
        main_layout.addWidget(main_splitter)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
        # Connect code executor signals
        self.code_executor.output_received.connect(self._on_execution_output)
        self.code_executor.error_received.connect(self._on_execution_error)
        self.code_executor.execution_finished.connect(self._on_execution_finished)
    
    def _create_menu_bar(self):
        """Create menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        file_menu.addAction("New File", self._on_new_file)
        file_menu.addAction("Open Project", self._on_open_project)
        file_menu.addAction("Save", self._on_save)
        file_menu.addAction("Save All", self._on_save_all)
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
        edit_menu.addSeparator()
        edit_menu.addAction("Find", self._on_find)
        edit_menu.addAction("Replace", self._on_replace)
        
        # Run menu
        run_menu = menubar.addMenu("Run")
        run_menu.addAction("Run Project", self._on_run_project)
        run_menu.addAction("Stop Execution", self._on_stop_execution)
        
        # View menu
        view_menu = menubar.addMenu("View")
        view_menu.addAction("Toggle Project Tree", self._on_toggle_project_tree)
        view_menu.addAction("Toggle Console", self._on_toggle_console)
        
        # Tools menu
        tools_menu = menubar.addMenu("Tools")
        tools_menu.addAction("Load Model", self._on_load_model)
        tools_menu.addAction("Run Inference", self._on_run_inference)
        tools_menu.addSeparator()
        tools_menu.addAction("GitHub Auth", self._on_github_auth)
        tools_menu.addAction("Repository", self._on_repository)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        help_menu.addAction("Settings", self._on_settings)
        help_menu.addAction("Plugin Manager", self._on_plugin_manager)
        help_menu.addSeparator()
        help_menu.addAction("About", self._on_about)
        help_menu.addAction("Documentation", self._on_documentation)
    
    def _setup_shortcuts(self):
        """Setup keyboard shortcuts"""
        # Register actions with shortcuts manager
        self.shortcuts_manager.register_action('new_file', self._on_new_file)
        self.shortcuts_manager.register_action('open_project', self._on_open_project)
        self.shortcuts_manager.register_action('save_file', self._on_save)
        self.shortcuts_manager.register_action('save_all', self._on_save_all)
        self.shortcuts_manager.register_action('quick_search', self._on_quick_search)
        self.shortcuts_manager.register_action('toggle_comment', self._on_toggle_comment)
        self.shortcuts_manager.register_action('global_search', self._on_global_search)
        self.shortcuts_manager.register_action('toggle_project_tree', self._on_toggle_project_tree)
        self.shortcuts_manager.register_action('run_project', self._on_run_project)
        self.shortcuts_manager.register_action('find', self._on_find)
        self.shortcuts_manager.register_action('replace', self._on_replace)
        
        # Create Qt shortcuts for all registered actions
        for action_id, shortcut_str in self.shortcuts_manager.get_all_shortcuts().items():
            try:
                QShortcut(QKeySequence(shortcut_str), self, 
                         lambda aid=action_id: self.shortcuts_manager.trigger_action(aid))
            except Exception as e:
                logger.warning(f"Failed to register shortcut {action_id}: {e}")
    
    def _connect_signals(self):
        """Connect signals"""
        self.event_system.model_loaded.connect(self._on_model_loaded_event)
        self.event_system.inference_complete.connect(self._on_inference_complete_event)
        self.event_system.file_saved.connect(self._on_file_saved_event)
    
    def _restore_window_state(self):
        """Restore window geometry and state"""
        geometry = self.app_data_manager.get_config_value('window_geometry')
        state = self.app_data_manager.get_config_value('window_state')
        
        if geometry:
            self.restoreGeometry(geometry)
        if state:
            self.restoreState(state)
        
        # Restore last project
        last_project = self.app_data_manager.get_config_value('last_project')
        if last_project and Path(last_project).exists():
            self._open_project_path(last_project)
    
    # File operations
    def _on_new_file(self):
        """Create new file"""
        name, ok = QInputDialog.getText(self, "New File", "File name:")
        if ok and name:
            editor = CodeEditor(theme_manager=self.theme_manager)
            self.theme_manager.register_component(editor)
            self.open_files[name] = editor
            self.tab_widget.addTab(editor, name)
            self.tab_widget.setCurrentWidget(editor)
            self.current_file = name
    
    def _on_open_project(self):
        """Open project"""
        project_dir = QFileDialog.getExistingDirectory(self, "Open Project")
        if project_dir:
            self._open_project_path(project_dir)
    
    def _open_project_path(self, project_path: str):
        """Open project from path"""
        self.current_project = project_path
        self.project_panel.set_project_root(project_path)
        self.app_data_manager.add_recent_project(project_path)
        self.status_bar.showMessage(f"Project: {Path(project_path).name}")
        logger.info(f"Project opened: {project_path}")
    
    def _on_file_selected(self, file_path: str):
        """Handle file selection from project tree"""
        try:
            file_path = Path(file_path)
            if not file_path.is_file():
                return
            
            # Check if already open
            for tab_name, editor in self.open_files.items():
                if tab_name == str(file_path):
                    self.tab_widget.setCurrentWidget(editor)
                    return
            
            # Open new file
            with open(file_path, 'r') as f:
                content = f.read()
            
            editor = CodeEditor(theme_manager=self.theme_manager)
            self.theme_manager.register_component(editor)
            editor.setPlainText(content)
            
            tab_name = file_path.name
            self.open_files[str(file_path)] = editor
            self.tab_widget.addTab(editor, tab_name)
            self.tab_widget.setCurrentWidget(editor)
            self.current_file = str(file_path)
            
            logger.info(f"File opened: {file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open file: {e}")
            logger.error(f"Failed to open file: {e}")
    
    def _on_file_created(self, file_path: str):
        """Handle file creation"""
        logger.info(f"File created: {file_path}")
    
    def _on_file_deleted(self, file_path: str):
        """Handle file deletion"""
        # Close tab if open
        for tab_name, editor in list(self.open_files.items()):
            if tab_name == file_path:
                idx = self.tab_widget.indexOf(editor)
                if idx >= 0:
                    self.tab_widget.removeTab(idx)
                del self.open_files[tab_name]
        logger.info(f"File deleted: {file_path}")
    
    def _on_save(self):
        """Save current file"""
        if self.current_file and self.current_file in self.open_files:
            editor = self.open_files[self.current_file]
            try:
                with open(self.current_file, 'w') as f:
                    f.write(editor.toPlainText())
                self.status_bar.showMessage(f"Saved: {Path(self.current_file).name}")
                logger.info(f"File saved: {self.current_file}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save file: {e}")
    
    def _on_save_all(self):
        """Save all open files"""
        for file_path, editor in self.open_files.items():
            try:
                with open(file_path, 'w') as f:
                    f.write(editor.toPlainText())
            except Exception as e:
                logger.error(f"Failed to save {file_path}: {e}")
        self.status_bar.showMessage("All files saved")
    
    def _on_tab_changed(self, index):
        """Handle tab change"""
        if index >= 0:
            widget = self.tab_widget.widget(index)
            for file_path, editor in self.open_files.items():
                if editor == widget:
                    self.current_file = file_path
                    break
    
    def _on_tab_close(self, index):
        """Handle tab close"""
        widget = self.tab_widget.widget(index)
        for file_path, editor in list(self.open_files.items()):
            if editor == widget:
                del self.open_files[file_path]
                self.tab_widget.removeTab(index)
                break
    
    # Edit operations
    def _on_undo(self):
        """Undo"""
        if self.current_file in self.open_files:
            self.open_files[self.current_file].undo()
    
    def _on_redo(self):
        """Redo"""
        if self.current_file in self.open_files:
            self.open_files[self.current_file].redo()
    
    def _on_cut(self):
        """Cut"""
        if self.current_file in self.open_files:
            self.open_files[self.current_file].cut()
    
    def _on_copy(self):
        """Copy"""
        if self.current_file in self.open_files:
            self.open_files[self.current_file].copy()
    
    def _on_paste(self):
        """Paste"""
        if self.current_file in self.open_files:
            self.open_files[self.current_file].paste()
    
    def _on_find(self):
        """Find"""
        self.status_bar.showMessage("Find: Not yet implemented")
    
    def _on_replace(self):
        """Replace"""
        self.status_bar.showMessage("Replace: Not yet implemented")
    
    def _on_toggle_comment(self):
        """Toggle comment"""
        if self.current_file in self.open_files:
            editor = self.open_files[self.current_file]
            cursor = editor.textCursor()
            if cursor.hasSelection():
                text = cursor.selectedText()
                if text.startswith('#'):
                    text = text[1:]
                else:
                    text = '#' + text
                cursor.insertText(text)
    
    # Search operations
    def _on_quick_search(self):
        """Quick file search"""
        self.status_bar.showMessage("Quick Search: Not yet implemented")
    
    def _on_global_search(self):
        """Global search"""
        self.status_bar.showMessage("Global Search: Not yet implemented")
    
    # Run operations
    def _on_run_project(self):
        """Run project"""
        if not self.current_project:
            QMessageBox.warning(self, "No Project", "Please open a project first")
            return
        
        entry_point = Path(self.current_project) / "main.py"
        if not entry_point.exists():
            QMessageBox.warning(self, "No Entry Point", "main.py not found in project")
            return
        
        self.console_panel.clear()
        self.console_panel.append_output("Starting execution...\n")
        self.code_executor.execute_python(str(entry_point), self.current_project)
    
    def _on_stop_execution(self):
        """Stop execution"""
        self.code_executor.stop_execution()
        self.console_panel.append_output("\nExecution stopped\n")
    
    def _on_execution_output(self, output: str):
        """Handle execution output"""
        self.console_panel.append_output(output)
    
    def _on_execution_error(self, error: str):
        """Handle execution error"""
        self.console_panel.append_error(error)
    
    def _on_execution_finished(self, return_code: int):
        """Handle execution finished"""
        self.status_bar.showMessage(f"Execution finished with code {return_code}")
    
    # View operations
    def _on_toggle_project_tree(self):
        """Toggle project tree visibility"""
        self.project_panel.setVisible(not self.project_panel.isVisible())
    
    def _on_toggle_console(self):
        """Toggle console visibility"""
        self.console_panel.setVisible(not self.console_panel.isVisible())
    
    # Tools operations
    def _on_load_model(self):
        """Load model"""
        dialog = ModelLoadDialog(self)
        dialog.exec_()
    
    def _on_run_inference(self):
        """Run inference"""
        dialog = InferenceDialog(self)
        dialog.exec_()
    
    def _on_github_auth(self):
        """GitHub authentication"""
        dialog = GitHubAuthDialog(self)
        dialog.exec_()
    
    def _on_repository(self):
        """Repository dialog"""
        dialog = RepositoryDialog(self)
        dialog.exec_()
    
    # Help operations
    def _on_settings(self):
        """Open settings"""
        dialog = EnhancedSettingsDialog(self, self.app_data_manager, self.shortcuts_manager, self.theme_manager)
        dialog.exec_()
    
    def _on_plugin_manager(self):
        """Open plugin manager"""
        self.status_bar.showMessage("Plugin Manager: Not yet implemented")
    
    def _on_about(self):
        """About dialog"""
        QMessageBox.about(self, "About PyAI IDE", 
                         "PyAI IDE v1.0\n\nA powerful IDE for AI development")
    
    def _on_documentation(self):
        """Open documentation"""
        self.status_bar.showMessage("Documentation: Not yet implemented")
    
    # Event handlers
    def _on_model_loaded_event(self, data):
        """Handle model loaded event"""
        logger.info(f"Model loaded: {data}")
    
    def _on_inference_complete_event(self, data):
        """Handle inference complete event"""
        logger.info(f"Inference complete: {data}")
    
    def _on_file_saved_event(self, data):
        """Handle file saved event"""
        logger.info(f"File saved: {data}")
    
    # Theme operations
    def _apply_theme(self, theme_name):
        """Apply theme"""
        self.theme_manager.set_theme(theme_name)
        self.app_data_manager.set_config_value('theme', theme_name)
    
    # Window events
    def closeEvent(self, event):
        """Handle window close"""
        # Save window state
        self.app_data_manager.set_config_value('window_geometry', self.saveGeometry())
        self.app_data_manager.set_config_value('window_state', self.saveState())
        event.accept()
    
    def keyPressEvent(self, event):
        """Handle key press events"""
        if not self.shortcut_handler.handle_key_event(event):
            super().keyPressEvent(event)
