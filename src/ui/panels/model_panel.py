"""
Model Panel for PyAI IDE
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, QPushButton, QLabel
from utils.logger import logger


class ModelPanel(QWidget):
    """Model panel for model management"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.loaded_models = []
        self._create_ui()
    
    def _create_ui(self):
        """Create model panel UI"""
        layout = QVBoxLayout(self)
        
        # Header
        header_layout = QHBoxLayout()
        header_layout.addWidget(QLabel("Loaded Models"))
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.refresh)
        header_layout.addStretch()
        header_layout.addWidget(self.refresh_btn)
        layout.addLayout(header_layout)
        
        # Model list
        self.model_list = QListWidget()
        layout.addWidget(self.model_list)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.unload_btn = QPushButton("Unload")
        self.unload_btn.clicked.connect(self._on_unload)
        button_layout.addWidget(self.unload_btn)
        layout.addLayout(button_layout)
    
    def add_model(self, model_id):
        """Add model to list"""
        if model_id not in self.loaded_models:
            self.loaded_models.append(model_id)
            item = QListWidgetItem(model_id)
            self.model_list.addItem(item)
            logger.info(f"Model added to panel: {model_id}")
    
    def remove_model(self, model_id):
        """Remove model from list"""
        if model_id in self.loaded_models:
            self.loaded_models.remove(model_id)
            for i in range(self.model_list.count()):
                if self.model_list.item(i).text() == model_id:
                    self.model_list.takeItem(i)
                    break
            logger.info(f"Model removed from panel: {model_id}")
    
    def _on_unload(self):
        """Handle unload button"""
        current_item = self.model_list.currentItem()
        if current_item:
            model_id = current_item.text()
            self.remove_model(model_id)
            logger.info(f"Unloaded model: {model_id}")
    
    def refresh(self):
        """Refresh model list"""
        logger.info("Refreshing model list")
    
    def get_loaded_models(self):
        """Get loaded models"""
        return self.loaded_models.copy()
