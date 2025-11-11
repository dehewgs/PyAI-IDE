"""
Repository Dialog for PyAI IDE
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QRadioButton, QButtonGroup
)
from utils.logger import logger


class RepositoryDialog(QDialog):
    """Dialog for repository operations"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Repository Operations")
        self.setGeometry(100, 100, 400, 250)
        self.operation = None
        self.data = None
        self._create_ui()
    
    def _create_ui(self):
        """Create dialog UI"""
        layout = QVBoxLayout(self)
        
        # Operation selection
        layout.addWidget(QLabel("Select Operation:"))
        self.operation_group = QButtonGroup()
        
        self.create_radio = QRadioButton("Create Repository")
        self.create_radio.setChecked(True)
        self.create_radio.toggled.connect(self._on_operation_changed)
        self.operation_group.addButton(self.create_radio)
        layout.addWidget(self.create_radio)
        
        self.clone_radio = QRadioButton("Clone Repository")
        self.clone_radio.toggled.connect(self._on_operation_changed)
        self.operation_group.addButton(self.clone_radio)
        layout.addWidget(self.clone_radio)
        
        # Input fields
        layout.addWidget(QLabel("Repository Name/URL:"))
        self.repo_input = QLineEdit()
        self.repo_input.setPlaceholderText("my-repo or https://github.com/user/repo")
        layout.addWidget(self.repo_input)
        
        layout.addWidget(QLabel("Description (optional):"))
        self.desc_input = QLineEdit()
        self.desc_input.setPlaceholderText("Repository description")
        layout.addWidget(self.desc_input)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.ok_btn = QPushButton("OK")
        self.ok_btn.clicked.connect(self._on_ok)
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.ok_btn)
        button_layout.addWidget(self.cancel_btn)
        layout.addLayout(button_layout)
    
    def _on_operation_changed(self):
        """Handle operation change"""
        if self.create_radio.isChecked():
            self.repo_input.setPlaceholderText("my-repo")
            self.desc_input.setVisible(True)
        else:
            self.repo_input.setPlaceholderText("https://github.com/user/repo")
            self.desc_input.setVisible(False)
    
    def _on_ok(self):
        """Handle OK button click"""
        repo_name = self.repo_input.text()
        if not repo_name:
            QMessageBox.warning(self, "Error", "Please enter repository name/URL")
            return
        
        if self.create_radio.isChecked():
            self.operation = "create"
            self.data = {
                "name": repo_name,
                "description": self.desc_input.text()
            }
            logger.info(f"Creating repository: {repo_name}")
        else:
            self.operation = "clone"
            self.data = {"url": repo_name}
            logger.info(f"Cloning repository: {repo_name}")
        
        self.accept()
    
    def get_operation(self):
        """Get the operation type"""
        return self.operation
    
    def get_data(self):
        """Get the operation data"""
        return self.data
