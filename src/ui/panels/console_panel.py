"""
Console Panel for PyAI IDE with Theme Support
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QLabel
from PyQt5.QtCore import pyqtSignal
from utils.logger import logger


class ConsolePanel(QWidget):
    """Console panel for output and debugging with theme support"""
    
    def __init__(self, parent=None, theme_manager=None):
        super().__init__(parent)
        self.output_lines = []
        self.theme_manager = theme_manager
        self._create_ui()
        
        # Connect to theme changes if theme manager available
        if self.theme_manager:
            self.theme_manager.theme_changed.connect(self._on_theme_changed)
    
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
        layout.addWidget(self.output)
        
        # Apply theme
        self._apply_theme()
    
    def _apply_theme(self):
        """Apply theme to console"""
        if self.theme_manager and self.theme_manager.current_config:
            bg_color = self.theme_manager.get_console_color("background", "#1e1e1e")
            fg_color = self.theme_manager.get_console_color("foreground", "#d4d4d4")
        else:
            bg_color = "#1e1e1e"
            fg_color = "#d4d4d4"
        
        self.output.setStyleSheet(f"""
            QTextEdit {{
                background-color: {bg_color};
                color: {fg_color};
                font-family: 'Courier New';
                font-size: 10px;
            }}
        """)
    
    def _on_theme_changed(self, theme_id):
        """Handle theme change
        
        Args:
            theme_id: New theme identifier
        """
        self._apply_theme()
    
    def write(self, text):
        """Write text to console
        
        Args:
            text: Text to write
        """
        self.output_lines.append(text)
        self.output.append(text)
        logger.debug(f"Console: {text}")
    
    def write_error(self, text):
        """Write error text to console
        
        Args:
            text: Error text to write
        """
        if self.theme_manager and self.theme_manager.current_config:
            error_color = self.theme_manager.get_console_color("error", "#f48771")
        else:
            error_color = "#f48771"
        
        self.output_lines.append(f"ERROR: {text}")
        self.output.append(f"<span style='color: {error_color};'><b>ERROR:</b> {text}</span>")
        logger.error(f"Console: {text}")
    
    def write_warning(self, text):
        """Write warning text to console
        
        Args:
            text: Warning text to write
        """
        if self.theme_manager and self.theme_manager.current_config:
            warning_color = self.theme_manager.get_console_color("warning", "#dcdcaa")
        else:
            warning_color = "#dcdcaa"
        
        self.output_lines.append(f"WARNING: {text}")
        self.output.append(f"<span style='color: {warning_color};'><b>WARNING:</b> {text}</span>")
        logger.warning(f"Console: {text}")
    
    def write_success(self, text):
        """Write success text to console
        
        Args:
            text: Success text to write
        """
        if self.theme_manager and self.theme_manager.current_config:
            success_color = self.theme_manager.get_console_color("success", "#6a9955")
        else:
            success_color = "#6a9955"
        
        self.output_lines.append(f"SUCCESS: {text}")
        self.output.append(f"<span style='color: {success_color};'><b>✓</b> {text}</span>")
        logger.info(f"Console: {text}")
    
    def write_info(self, text):
        """Write info text to console
        
        Args:
            text: Info text to write
        """
        if self.theme_manager and self.theme_manager.current_config:
            info_color = self.theme_manager.get_console_color("info", "#4ec9b0")
        else:
            info_color = "#4ec9b0"
        
        self.output_lines.append(f"INFO: {text}")
        self.output.append(f"<span style='color: {info_color};'><b>ℹ</b> {text}</span>")
        logger.info(f"Console: {text}")
    
    def clear(self):
        """Clear console"""
        self.output.clear()
        self.output_lines.clear()
        logger.info("Console cleared")
    
    def get_output(self):
        """Get all output
        
        Returns:
            All console output as string
        """
        return '\n'.join(self.output_lines)
