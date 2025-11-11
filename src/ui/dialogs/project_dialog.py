"""
Project Dialog for PyAI IDE
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QFileDialog
)
from utils.logger import logger


class ProjectDialog(QDialog):
    """Dialog for creating new projects"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create New Project")
        self.setGeometry(100, 100, 400, 200)
        self.project_data = None
        self._create_ui()
    
    def _create_ui(self):
        """Create dialog UI"""
        layout = QVBoxLayout(self)
        
        # Project name
        layout.addWidget(QLabel("Project Name:"))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("my-project")
        layout.addWidget(self.name_input)
        
        # Project location
        loc_layout = QHBoxLayout()
        loc_layout.addWidget(QLabel("Location:"))
        self.location_input = QLineEdit()
        self.location_input.setPlaceholderText("/path/to/projects")
        loc_layout.addWidget(self.location_input)
        self.browse_btn = QPushButton("Browse...")
        self.browse_btn.clicked.connect(self._on_browse)
        loc_layout.addWidget(self.browse_btn)
        layout.addLayout(loc_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.create_btn = QPushButton("Create")
        self.create_btn.clicked.connect(self._on_create)
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.create_btn)
        button_layout.addWidget(self.cancel_btn)
        layout.addLayout(button_layout)
    
    def _on_browse(self):
        """Handle browse button click"""
        path = QFileDialog.getExistingDirectory(self, "Select Project Location")
        if path:
            self.location_input.setText(path)
    
    def _on_create(self):
        """Handle create button click"""
        name = self.name_input.text()
        location = self.location_input.text()
        
        if not name:
            QMessageBox.warning(self, "Error", "Please enter project name")
            return
        
        logger.info(f"Creating project: {name} at {location}")
        self.project_data = {"name": name, "location": location}
        self.accept()
    
    def get_project_data(self):
        """Get project data"""
        return self.project_data
