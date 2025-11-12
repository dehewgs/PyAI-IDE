"""
Shortcuts Configuration Dialog
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLabel, QKeySequenceEdit, QMessageBox
)
from PyQt5.QtCore import Qt
from utils.logger import logger


class ShortcutsDialog(QDialog):
    """Dialog for configuring keyboard shortcuts"""
    
    def __init__(self, parent=None, shortcuts_manager=None):
        super().__init__(parent)
        self.shortcuts_manager = shortcuts_manager
        self.setWindowTitle("Keyboard Shortcuts")
        self.setGeometry(100, 100, 600, 500)
        self._create_ui()
    
    def _create_ui(self):
        """Create UI"""
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Customize Keyboard Shortcuts")
        layout.addWidget(title)
        
        # Shortcuts table
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Action", "Shortcut"])
        self.table.horizontalHeader().setStretchLastSection(False)
        self.table.setColumnWidth(0, 300)
        self.table.setColumnWidth(1, 200)
        
        # Populate table
        shortcuts = self.shortcuts_manager.get_all_shortcuts()
        self.table.setRowCount(len(shortcuts))
        
        for row, (action_id, shortcut) in enumerate(shortcuts.items()):
            # Action name
            action_item = QTableWidgetItem(action_id)
            action_item.setFlags(action_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 0, action_item)
            
            # Shortcut
            shortcut_item = QTableWidgetItem(shortcut)
            self.table.setItem(row, 1, shortcut_item)
        
        layout.addWidget(self.table)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        reset_btn = QPushButton("Reset to Defaults")
        reset_btn.clicked.connect(self._on_reset)
        button_layout.addWidget(reset_btn)
        
        button_layout.addStretch()
        
        apply_btn = QPushButton("Apply")
        apply_btn.clicked.connect(self._on_apply)
        button_layout.addWidget(apply_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
    
    def _on_reset(self):
        """Reset shortcuts to defaults"""
        reply = QMessageBox.question(
            self, "Reset Shortcuts",
            "Reset all shortcuts to defaults?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.shortcuts_manager.reset_shortcuts()
            self._refresh_table()
    
    def _on_apply(self):
        """Apply changes"""
        try:
            # Get all shortcuts from table
            shortcuts = {}
            for row in range(self.table.rowCount()):
                action_item = self.table.item(row, 0)
                shortcut_item = self.table.item(row, 1)
                
                action_id = action_item.text()
                shortcut = shortcut_item.text()
                
                shortcuts[action_id] = shortcut
            
            # Import shortcuts
            if self.shortcuts_manager.import_shortcuts(shortcuts):
                QMessageBox.information(self, "Success", "Shortcuts updated successfully")
                self.accept()
            else:
                QMessageBox.warning(self, "Error", "Failed to update shortcuts")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error applying shortcuts: {e}")
            logger.error(f"Error applying shortcuts: {e}")
    
    def _refresh_table(self):
        """Refresh table with current shortcuts"""
        shortcuts = self.shortcuts_manager.get_all_shortcuts()
        self.table.setRowCount(len(shortcuts))
        
        for row, (action_id, shortcut) in enumerate(shortcuts.items()):
            action_item = QTableWidgetItem(action_id)
            action_item.setFlags(action_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 0, action_item)
            
            shortcut_item = QTableWidgetItem(shortcut)
            self.table.setItem(row, 1, shortcut_item)
