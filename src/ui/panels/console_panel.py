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
        self.is_dark = True
        self._setup_ui()
        self._apply_theme()
    
    def _setup_ui(self):
        """Setup UI"""
        layout = QVBoxLayout()
        
        # Console output
        self.console_output = QTextEdit()
        self.console_output.setReadOnly(True)
        
        layout.addWidget(self.console_output)
        
        # Clear button
        button_layout = QHBoxLayout()
        clear_btn = QPushButton("Clear")
        clear_btn.clicked.connect(self.clear)
        button_layout.addStretch()
        button_layout.addWidget(clear_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def _apply_theme(self):
        """Apply theme to console"""
        if self.theme_manager:
            bg = self.theme_manager.get_color("background", "#1e1e1e")
            fg = self.theme_manager.get_color("foreground", "#d4d4d4")
            # Determine if dark theme based on background brightness
            bg_color = QColor(bg)
            brightness = (bg_color.red() + bg_color.green() + bg_color.blue()) / 3
            self.is_dark = brightness < 128
        else:
            bg = "#1e1e1e"
            fg = "#d4d4d4"
            self.is_dark = True
        
        self.console_output.setStyleSheet(f"""
            QTextEdit {{
                background-color: {bg};
                color: {fg};
                border: none;
                font-family: 'Courier New', monospace;
                font-size: 10pt;
            }}
        """)
    
    def write(self, text, color=None):
        """Write text to console
        
        Args:
            text: Text to write
            color: Text color (hex) - if None, uses foreground color
        """
        cursor = self.console_output.textCursor()
        cursor.movePosition(QTextCursor.End)
        
        fmt = QTextCharFormat()
        if color:
            fmt.setForeground(QColor(color))
        else:
            # Use foreground color from theme
            if self.theme_manager:
                fg = self.theme_manager.get_color("foreground", "#d4d4d4")
            else:
                fg = "#d4d4d4"
            fmt.setForeground(QColor(fg))
        
        cursor.setCharFormat(fmt)
        cursor.insertText(text)
        
        self.console_output.setTextCursor(cursor)
        self.console_output.ensureCursorVisible()
    
    def write_error(self, text):
        """Write error message
        
        Args:
            text: Error message
        """
        if self.is_dark:
            color = "#f48771"
        else:
            color = "#cb2431"
        self.write(text + "\n", color)
    
    def write_warning(self, text):
        """Write warning message
        
        Args:
            text: Warning message
        """
        if self.is_dark:
            color = "#dcdcaa"
        else:
            color = "#d18616"
        self.write(text + "\n", color)
    
    def write_success(self, text):
        """Write success message
        
        Args:
            text: Success message
        """
        if self.is_dark:
            color = "#4ec9b0"
        else:
            color = "#28a745"
        self.write(text + "\n", color)
    
    def write_info(self, text):
        """Write info message
        
        Args:
            text: Info message
        """
        if self.is_dark:
            color = "#9cdcfe"
        else:
            color = "#0066cc"
        self.write(text + "\n", color)
    
    def clear(self):
        """Clear console output"""
        self.console_output.clear()
    
    def set_theme(self, is_dark):
        """Update theme
        
        Args:
            is_dark: True for dark theme, False for light theme
        """
        self.is_dark = is_dark
        self._apply_theme()
