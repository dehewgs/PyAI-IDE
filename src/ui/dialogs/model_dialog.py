"""
Model Loading Dialog for PyAI IDE
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox,
    QPushButton, QMessageBox, QProgressBar, QCheckBox
)
from PyQt5.QtCore import Qt, pyqtSignal, QThread
from utils.logger import logger


class ModelLoadDialog(QDialog):
    """Dialog for loading HuggingFace models"""
    
    model_loaded = pyqtSignal(str)  # Signal emitted when model is loaded
    
    def __init__(self, parent=None, available_models=None):
        super().__init__(parent)
        self.setWindowTitle("Load Model")
        self.setGeometry(100, 100, 400, 250)
        self.available_models = available_models or [
            "gpt2",
            "bert-base-uncased",
            "distilbert-base-uncased",
            "roberta-base",
            "t5-small"
        ]
        self.selected_model = None
        self._create_ui()
    
    def _create_ui(self):
        """Create dialog UI"""
        layout = QVBoxLayout(self)
        
        # Model selection
        model_layout = QHBoxLayout()
        model_layout.addWidget(QLabel("Model:"))
        self.model_combo = QComboBox()
        self.model_combo.addItems(self.available_models)
        model_layout.addWidget(self.model_combo)
        layout.addLayout(model_layout)
        
        # Custom model input
        custom_layout = QHBoxLayout()
        custom_layout.addWidget(QLabel("Or enter custom model ID:"))
        self.custom_model_input = QLineEdit()
        self.custom_model_input.setPlaceholderText("e.g., gpt2-medium")
        custom_layout.addWidget(self.custom_model_input)
        layout.addLayout(custom_layout)
        
        # Options
        self.use_cache_checkbox = QCheckBox("Use cached model if available")
        self.use_cache_checkbox.setChecked(True)
        layout.addWidget(self.use_cache_checkbox)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.load_btn = QPushButton("Load")
        self.load_btn.clicked.connect(self._on_load)
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.load_btn)
        button_layout.addWidget(self.cancel_btn)
        layout.addLayout(button_layout)
    
    def _on_load(self):
        """Handle load button click"""
        # Get model ID
        if self.custom_model_input.text():
            model_id = self.custom_model_input.text()
        else:
            model_id = self.model_combo.currentText()
        
        if not model_id:
            QMessageBox.warning(self, "Error", "Please select or enter a model ID")
            return
        
        logger.info(f"Loading model: {model_id}")
        self.selected_model = model_id
        self.model_loaded.emit(model_id)
        self.accept()
    
    def get_selected_model(self):
        """Get the selected model ID"""
        return self.selected_model
