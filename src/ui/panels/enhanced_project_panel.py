"""
Enhanced Project Panel with file operations
"""

import os
import shutil
from pathlib import Path
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTreeWidget, QTreeWidgetItem,
    QPushButton, QLabel, QMenu, QInputDialog, QMessageBox, QFileDialog
)
from PyQt5.QtCore import pyqtSignal, Qt, QTimer
from PyQt5.QtGui import QIcon, QColor
from utils.logger import logger


class EnhancedProjectPanel(QWidget):
    """Enhanced project panel with file operations"""
    
    file_selected = pyqtSignal(str)
    file_created = pyqtSignal(str)
    file_deleted = pyqtSignal(str)
    file_renamed = pyqtSignal(str, str)
    
    def __init__(self, parent=None, theme_manager=None):
        super().__init__(parent)
        self.theme_manager = theme_manager
        self.project_root = None
        self.file_watcher_timer = None
        self._create_ui()
        self._setup_file_watcher()
    
    def _create_ui(self):
        """Create UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(8, 8, 8, 8)
        header_layout.setSpacing(8)
        
        self.header_label = QLabel("Project Files")
        header_layout.addWidget(self.header_label)
        
        self.new_file_btn = QPushButton("New File")
        self.new_file_btn.clicked.connect(self._on_new_file)
        header_layout.addWidget(self.new_file_btn)
        
        self.new_folder_btn = QPushButton("New Folder")
        self.new_folder_btn.clicked.connect(self._on_new_folder)
        header_layout.addWidget(self.new_folder_btn)
        
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.refresh)
        header_layout.addStretch()
        header_layout.addWidget(self.refresh_btn)
        
        layout.addLayout(header_layout)
        
        # File tree
        self.tree = QTreeWidget()
        self.tree.setHeaderLabel("Files")
        self.tree.itemClicked.connect(self._on_item_clicked)
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self._on_context_menu)
        layout.addWidget(self.tree)
        
        self._apply_theme()
    
    def set_project_root(self, project_path: str):
        """Set project root directory
        
        Args:
            project_path: Path to project root
        """
        self.project_root = Path(project_path)
        self.refresh()
    
    def refresh(self):
        """Refresh file tree"""
        if not self.project_root:
            self.tree.clear()
            return
        
        self.tree.clear()
        root_item = QTreeWidgetItem(self.tree)
        root_item.setText(0, self.project_root.name)
        root_item.setData(0, Qt.UserRole, str(self.project_root))
        
        self._populate_tree(self.project_root, root_item)
        self.tree.expandItem(root_item)
    
    def _populate_tree(self, directory: Path, parent_item: QTreeWidgetItem):
        """Recursively populate tree
        
        Args:
            directory: Directory to populate
            parent_item: Parent tree item
        """
        try:
            items = sorted(directory.iterdir(), key=lambda x: (not x.is_dir(), x.name))
            
            for item in items:
                if item.name.startswith('.'):
                    continue
                
                tree_item = QTreeWidgetItem(parent_item)
                tree_item.setText(0, item.name)
                tree_item.setData(0, Qt.UserRole, str(item))
                
                if item.is_dir():
                    self._populate_tree(item, tree_item)
        except Exception as e:
            logger.error(f"Error populating tree: {e}")
    
    def _on_item_clicked(self, item: QTreeWidgetItem, column: int):
        """Handle item click"""
        file_path = item.data(0, Qt.UserRole)
        if file_path and Path(file_path).is_file():
            self.file_selected.emit(file_path)
    
    def _on_context_menu(self, position):
        """Show context menu"""
        item = self.tree.itemAt(position)
        if not item:
            return
        
        file_path = item.data(0, Qt.UserRole)
        if not file_path:
            return
        
        menu = QMenu()
        
        path_obj = Path(file_path)
        
        if path_obj.is_file():
            menu.addAction("Open", lambda: self.file_selected.emit(file_path))
            menu.addSeparator()
        
        menu.addAction("Rename", lambda: self._rename_item(item, file_path))
        menu.addAction("Delete", lambda: self._delete_item(item, file_path))
        
        if path_obj.is_dir():
            menu.addSeparator()
            menu.addAction("New File", lambda: self._new_file_in_dir(file_path))
            menu.addAction("New Folder", lambda: self._new_folder_in_dir(file_path))
        
        menu.exec_(self.tree.mapToGlobal(position))
    
    def _on_new_file(self):
        """Create new file in project root"""
        if not self.project_root:
            QMessageBox.warning(self, "No Project", "Please open a project first")
            return
        self._new_file_in_dir(str(self.project_root))
    
    def _on_new_folder(self):
        """Create new folder in project root"""
        if not self.project_root:
            QMessageBox.warning(self, "No Project", "Please open a project first")
            return
        self._new_folder_in_dir(str(self.project_root))
    
    def _new_file_in_dir(self, directory: str):
        """Create new file in directory"""
        name, ok = QInputDialog.getText(self, "New File", "File name:")
        if ok and name:
            try:
                file_path = Path(directory) / name
                file_path.touch()
                self.file_created.emit(str(file_path))
                self.refresh()
                logger.info(f"File created: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to create file: {e}")
                logger.error(f"Failed to create file: {e}")
    
    def _new_folder_in_dir(self, directory: str):
        """Create new folder in directory"""
        name, ok = QInputDialog.getText(self, "New Folder", "Folder name:")
        if ok and name:
            try:
                folder_path = Path(directory) / name
                folder_path.mkdir()
                self.refresh()
                logger.info(f"Folder created: {folder_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to create folder: {e}")
                logger.error(f"Failed to create folder: {e}")
    
    def _rename_item(self, item: QTreeWidgetItem, file_path: str):
        """Rename file or folder"""
        old_name = Path(file_path).name
        new_name, ok = QInputDialog.getText(self, "Rename", "New name:", text=old_name)
        
        if ok and new_name and new_name != old_name:
            try:
                old_path = Path(file_path)
                new_path = old_path.parent / new_name
                old_path.rename(new_path)
                self.file_renamed.emit(file_path, str(new_path))
                self.refresh()
                logger.info(f"Renamed: {file_path} -> {new_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to rename: {e}")
                logger.error(f"Failed to rename: {e}")
    
    def _delete_item(self, item: QTreeWidgetItem, file_path: str):
        """Delete file or folder"""
        reply = QMessageBox.question(
            self, "Delete",
            f"Delete {Path(file_path).name}?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                path = Path(file_path)
                if path.is_dir():
                    shutil.rmtree(path)
                else:
                    path.unlink()
                self.file_deleted.emit(file_path)
                self.refresh()
                logger.info(f"Deleted: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete: {e}")
                logger.error(f"Failed to delete: {e}")
    
    def _setup_file_watcher(self):
        """Setup file system watcher"""
        self.file_watcher_timer = QTimer()
        self.file_watcher_timer.timeout.connect(self._check_file_changes)
        self.file_watcher_timer.start(2000)  # Check every 2 seconds
    
    def _check_file_changes(self):
        """Check for external file changes"""
        if self.project_root and self.project_root.exists():
            # Simple check - could be enhanced with proper file watching
            pass
    
    def _apply_theme(self):
        """Apply theme to panel"""
        if not self.theme_manager:
            return
        
        is_dark = self.theme_manager.current_theme == "dark"
        self.set_theme(is_dark)
    
    def set_theme(self, is_dark):
        """Set theme for the panel"""
        if is_dark:
            bg_color = "#1e1e1e"
            fg_color = "#d4d4d4"
            border_color = "#3e3e3e"
        else:
            bg_color = "#ffffff"
            fg_color = "#333333"
            border_color = "#cccccc"
        
        self.tree.setStyleSheet(f"""
            QTreeWidget {{
                background-color: {bg_color};
                color: {fg_color};
                border: none;
            }}
            QTreeWidget::item:selected {{
                background-color: #0e639c;
            }}
        """)
