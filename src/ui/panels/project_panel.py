"""
Project Panel for PyAI IDE
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTreeWidget, QTreeWidgetItem, QPushButton, QLabel
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QColor
from utils.logger import logger


class ProjectPanel(QWidget):
    """Project panel for file browser"""
    
    file_selected = pyqtSignal(str)
    
    def __init__(self, parent=None, theme_manager=None):
        super().__init__(parent)
        self.theme_manager = theme_manager
        self._create_ui()
    
    def _create_ui(self):
        """Create project panel UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(8, 8, 8, 8)
        header_layout.setSpacing(8)
        self.header_label = QLabel("Project Files")
        header_layout.addWidget(self.header_label)
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
    
    def _apply_theme(self):
        """Apply theme to panel"""
        if not self.theme_manager:
            return
        
        is_dark = self.theme_manager.current_theme == "dark"
        self.set_theme(is_dark)
    
    def set_theme(self, is_dark):
        """Set theme for the panel
        
        Args:
            is_dark: True for dark theme, False for light theme
        """
        if is_dark:
            # Dark theme
            bg_color = "#1e1e1e"
            fg_color = "#d4d4d4"
            border_color = "#3e3e3e"
            header_bg = "#252526"
        else:
            # Light theme
            bg_color = "#ffffff"
            fg_color = "#333333"
            border_color = "#cccccc"
            header_bg = "#f3f3f3"
        
        # Apply stylesheet to tree widget
        self.tree.setStyleSheet(f"""
            QTreeWidget {{
                background-color: {bg_color};
                color: {fg_color};
                border: none;
            }}
            QTreeWidget::item:selected {{
                background-color: #0e639c;
                color: #ffffff;
            }}
            QTreeWidget::item:hover {{
                background-color: {border_color};
            }}
        """)
        
        # Apply stylesheet to header label
        self.header_label.setStyleSheet(f"""
            QLabel {{
                color: {fg_color};
                background-color: {header_bg};
                padding: 4px 8px;
                font-weight: bold;
            }}
        """)
        
        # Apply stylesheet to buttons
        self.refresh_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #0e639c;
                color: #ffffff;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #1177bb;
            }}
            QPushButton:pressed {{
                background-color: #0d5a96;
            }}
        """)
        
        # Apply stylesheet to panel itself
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {bg_color};
                color: {fg_color};
            }}
        """)
    
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
