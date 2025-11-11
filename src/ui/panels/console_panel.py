"""
Console Panel for PyAI IDE
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QLabel
from PyQt5.QtCore import pyqtSignal
from utils.logger import logger


class ConsolePanel(QWidget):
    """Console panel for output and debugging"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.output_lines = []
        self._create_ui()
    
    def _create_ui(self):
        """Create console UI"""
        layout = QVBoxLayout(self)
        
        # Header
        header_layout = QHBoxLayout()
        header_layout.addWidget(QLabel("Console Output"))
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.clear)
        header_layout.addStretch()
        header_layout.addWidget(self.clear_btn)
        layout.addLayout(header_layout)
        
        # Output area
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                font-family: 'Courier New';
                font-size: 10px;
            }
        """)
        layout.addWidget(self.output)
    
    def write(self, text):
        """Write text to console"""
        self.output_lines.append(text)
        self.output.append(text)
        logger.debug(f"Console: {text}")
    
    def clear(self):
        """Clear console"""
        self.output.clear()
        self.output_lines.clear()
        logger.info("Console cleared")
    
    def get_output(self):
        """Get all output"""
        return '\n'.join(self.output_lines)
