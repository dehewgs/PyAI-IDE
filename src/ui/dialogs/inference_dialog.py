"""
Inference Dialog for PyAI IDE
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit,
    QPushButton, QMessageBox, QComboBox
)
from utils.logger import logger


class InferenceDialog(QDialog):
    """Dialog for running inference"""
    
    def __init__(self, parent=None, loaded_models=None):
        super().__init__(parent)
        self.setWindowTitle("Run Inference")
        self.setGeometry(100, 100, 500, 400)
        self.loaded_models = loaded_models or []
        self.result = None
        self._create_ui()
    
    def _create_ui(self):
        """Create dialog UI"""
        layout = QVBoxLayout(self)
        
        # Model selection
        model_layout = QHBoxLayout()
        model_layout.addWidget(QLabel("Model:"))
        self.model_combo = QComboBox()
        self.model_combo.addItems(self.loaded_models or ["No models loaded"])
        model_layout.addWidget(self.model_combo)
        layout.addLayout(model_layout)
        
        # Input text
        layout.addWidget(QLabel("Input Text:"))
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("Enter text for inference...")
        self.input_text.setMinimumHeight(100)
        layout.addWidget(self.input_text)
        
        # Parameters
        param_layout = QHBoxLayout()
        param_layout.addWidget(QLabel("Max Length:"))
        self.max_length = QLineEdit()
        self.max_length.setText("100")
        param_layout.addWidget(self.max_length)
        layout.addLayout(param_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.run_btn = QPushButton("Run Inference")
        self.run_btn.clicked.connect(self._on_run)
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.run_btn)
        button_layout.addWidget(self.cancel_btn)
        layout.addLayout(button_layout)
    
    def _on_run(self):
        """Handle run button click"""
        if not self.input_text.toPlainText():
            QMessageBox.warning(self, "Error", "Please enter input text")
            return
        
        model = self.model_combo.currentText()
        text = self.input_text.toPlainText()
        
        logger.info(f"Running inference on {model} with text: {text[:50]}...")
        self.result = {"model": model, "input": text}
        self.accept()
    
    def get_result(self):
        """Get inference result"""
        return self.result
