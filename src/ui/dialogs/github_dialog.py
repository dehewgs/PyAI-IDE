"""
GitHub Authentication Dialog for PyAI IDE
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox
)
from PyQt5.QtGui import QFont
from utils.logger import logger


class GitHubAuthDialog(QDialog):
    """Dialog for GitHub authentication"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Connect to GitHub")
        self.setGeometry(100, 100, 400, 200)
        self.token = None
        self._create_ui()
    
    def _create_ui(self):
        """Create dialog UI"""
        layout = QVBoxLayout(self)
        
        # Instructions
        instructions = QLabel(
            "Enter your GitHub Personal Access Token.\n"
            "Get one at: https://github.com/settings/tokens"
        )
        instructions.setFont(QFont("Arial", 9))
        layout.addWidget(instructions)
        
        # Token input
        layout.addWidget(QLabel("GitHub Token:"))
        self.token_input = QLineEdit()
        self.token_input.setEchoMode(QLineEdit.Password)
        self.token_input.setPlaceholderText("ghp_xxxxxxxxxxxx")
        layout.addWidget(self.token_input)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.connect_btn = QPushButton("Connect")
        self.connect_btn.clicked.connect(self._on_connect)
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.connect_btn)
        button_layout.addWidget(self.cancel_btn)
        layout.addLayout(button_layout)
    
    def _on_connect(self):
        """Handle connect button click"""
        token = self.token_input.text()
        if not token:
            QMessageBox.warning(self, "Error", "Please enter a GitHub token")
            return
        
        logger.info("Authenticating with GitHub")
        self.token = token
        self.accept()
    
    def get_token(self):
        """Get the GitHub token"""
        return self.token
