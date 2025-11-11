"""
Project Panel for PyAI IDE
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTreeWidget, QTreeWidgetItem, QPushButton, QLabel
from PyQt5.QtCore import pyqtSignal
from utils.logger import logger


class ProjectPanel(QWidget):
    """Project panel for file browser"""
    
    file_selected = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._create_ui()
    
    def _create_ui(self):
        """Create project panel UI"""
        layout = QVBoxLayout(self)
        
        # Header
        header_layout = QHBoxLayout()
        header_layout.addWidget(QLabel("Project Files"))
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.refresh)
        header_layout.addStretch()
        header_layout.addWidget(self.refresh_btn)
        layout.addLayout(header_layout)
        
        # File tree
        self.tree = QTreeWidget()
        self.tree.setHeaderLabel("Files")
        self.tree.itemClicked.connect(self._on_item_clicked)
        layout.addWidget(self.tree)
    
    def add_file(self, filename, parent=None):
        """Add file to tree"""
        if parent is None:
            parent = self.tree.invisibleRootItem()
        
        item = QTreeWidgetItem(parent)
        item.setText(0, filename)
        logger.debug(f"Added file to project: {filename}")
        return item
    
    def add_folder(self, foldername, parent=None):
        """Add folder to tree"""
        if parent is None:
            parent = self.tree.invisibleRootItem()
        
        item = QTreeWidgetItem(parent)
        item.setText(0, foldername)
        logger.debug(f"Added folder to project: {foldername}")
        return item
    
    def _on_item_clicked(self, item, column):
        """Handle item click"""
        filename = item.text(0)
        self.file_selected.emit(filename)
        logger.debug(f"File selected: {filename}")
    
    def refresh(self):
        """Refresh project tree"""
        logger.info("Refreshing project tree")
    
    def clear(self):
        """Clear project tree"""
        self.tree.clear()
