"""
Console Panel for PyAI IDE
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QTextCursor, QColor, QTextCharFormat


class ConsolePanel(QWidget):
    """Console panel for displaying output"""
    
    def __init__(self, theme_manager=None):
        super().__init__()
        self.theme_manager = theme_manager
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup UI"""
        layout = QVBoxLayout()
        
        # Console output
        self.console_output = QTextEdit()
        self.console_output.setReadOnly(True)
        self.console_output.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                border: none;
                font-family: 'Courier New', monospace;
                font-size: 10pt;
            }
        """)
        
        layout.addWidget(self.console_output)
        
        # Clear button
        button_layout = QHBoxLayout()
        clear_btn = QPushButton("Clear")
        clear_btn.clicked.connect(self.clear)
        button_layout.addStretch()
        button_layout.addWidget(clear_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def write(self, text, color="#d4d4d4"):
        """Write text to console
        
        Args:
            text: Text to write
            color: Text color (hex)
        """
        cursor = self.console_output.textCursor()
        cursor.movePosition(QTextCursor.End)
        
        fmt = QTextCharFormat()
        fmt.setForeground(QColor(color))
        
        cursor.setCharFormat(fmt)
        cursor.insertText(text)
        
        self.console_output.setTextCursor(cursor)
        self.console_output.ensureCursorVisible()
    
    def write_error(self, text):
        """Write error message
        
        Args:
            text: Error message
        """
        self.write(text + "\n", "#f48771")
    
    def write_warning(self, text):
        """Write warning message
        
        Args:
            text: Warning message
        """
        self.write(text + "\n", "#dcdcaa")
    
    def write_success(self, text):
        """Write success message
        
        Args:
            text: Success message
        """
        self.write(text + "\n", "#4ec9b0")
    
    def write_info(self, text):
        """Write info message
        
        Args:
            text: Info message
        """
        self.write(text + "\n", "#9cdcfe")
    
    def clear(self):
        """Clear console output"""
        self.console_output.clear()
