"""
Settings Dialog for PyAI IDE
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QCheckBox, QTabWidget, QWidget
)
from utils.logger import logger


class SettingsDialog(QDialog):
    """Dialog for application settings"""
    
    def __init__(self, parent=None, config=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setGeometry(100, 100, 500, 400)
        self.config = config
        self.settings = {}
        self._create_ui()
    
    def _create_ui(self):
        """Create dialog UI"""
        layout = QVBoxLayout(self)
        
        # Tabs
        tabs = QTabWidget()
        
        # General tab
        general_tab = QWidget()
        general_layout = QVBoxLayout(general_tab)
        
        general_layout.addWidget(QLabel("Theme:"))
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark", "Light"])
        general_layout.addWidget(self.theme_combo)
        
        self.auto_save_check = QCheckBox("Auto-save files")
        self.auto_save_check.setChecked(True)
        general_layout.addWidget(self.auto_save_check)
        
        general_layout.addStretch()
        tabs.addTab(general_tab, "General")
        
        # API tab
        api_tab = QWidget()
        api_layout = QVBoxLayout(api_tab)
        
        api_layout.addWidget(QLabel("HuggingFace Token:"))
        self.hf_token = QLineEdit()
        self.hf_token.setEchoMode(QLineEdit.Password)
        api_layout.addWidget(self.hf_token)
        
        api_layout.addWidget(QLabel("GitHub Token:"))
        self.gh_token = QLineEdit()
        self.gh_token.setEchoMode(QLineEdit.Password)
        api_layout.addWidget(self.gh_token)
        
        api_layout.addStretch()
        tabs.addTab(api_tab, "API Keys")
        
        layout.addWidget(tabs)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self._on_save)
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.cancel_btn)
        layout.addLayout(button_layout)
    
    def _on_save(self):
        """Handle save button click"""
        self.settings = {
            "theme": self.theme_combo.currentText(),
            "auto_save": self.auto_save_check.isChecked(),
            "hf_token": self.hf_token.text(),
            "gh_token": self.gh_token.text(),
        }
        logger.info("Settings saved")
        self.accept()
    
    def get_settings(self):
        """Get settings"""
        return self.settings
