"""
Terminal Panel for PyAI IDE
Provides terminal emulation and command execution interface
"""

import os
import sys
import subprocess
from pathlib import Path
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPlainTextEdit, QPushButton,
    QLabel, QLineEdit, QComboBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QProcess, QTimer
from PyQt5.QtGui import QFont, QColor, QTextCursor
from utils.logger import logger


class TerminalPanel(QWidget):
    """Terminal panel for command execution and output display"""
    
    output_received = pyqtSignal(str)
    error_received = pyqtSignal(str)
    
    def __init__(self, parent=None, theme_manager=None):
        super().__init__(parent)
        self.theme_manager = theme_manager
        self.current_directory = Path.home()
        self.process = None
        self.command_history = []
        self.history_index = -1
        
        self._create_ui()
        self._apply_theme()
    
    def _create_ui(self):
        """Create terminal UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header with directory and controls
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(8, 8, 8, 8)
        header_layout.setSpacing(8)
        
        self.dir_label = QLabel("Directory:")
        header_layout.addWidget(self.dir_label)
        
        self.dir_display = QLineEdit()
        self.dir_display.setText(str(self.current_directory))
        self.dir_display.setReadOnly(True)
        header_layout.addWidget(self.dir_display)
        
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.clear)
        header_layout.addWidget(self.clear_btn)
        
        layout.addLayout(header_layout)
        
        # Terminal output area
        self.output = QPlainTextEdit()
        self.output.setReadOnly(True)
        self.output.setFont(QFont("Courier New", 10))
        self.output.setMaximumHeight(200)
        layout.addWidget(self.output, 1)
        
        # Command input area
        input_layout = QHBoxLayout()
        input_layout.setContentsMargins(8, 8, 8, 8)
        input_layout.setSpacing(8)
        
        self.prompt_label = QLabel("$")
        input_layout.addWidget(self.prompt_label)
        
        self.command_input = QLineEdit()
        self.command_input.setPlaceholderText("Enter command...")
        self.command_input.returnPressed.connect(self._execute_command)
        self.command_input.keyPressEvent = self._handle_input_key
        input_layout.addWidget(self.command_input)
        
        self.execute_btn = QPushButton("Execute")
        self.execute_btn.clicked.connect(self._execute_command)
        input_layout.addWidget(self.execute_btn)
        
        layout.addLayout(input_layout)
    
    def _handle_input_key(self, event):
        """Handle keyboard events in command input"""
        if event.key() == Qt.Key_Up:
            # Navigate command history backwards
            if self.history_index < len(self.command_history) - 1:
                self.history_index += 1
                self.command_input.setText(self.command_history[-(self.history_index + 1)])
            event.accept()
        elif event.key() == Qt.Key_Down:
            # Navigate command history forwards
            if self.history_index > 0:
                self.history_index -= 1
                self.command_input.setText(self.command_history[-(self.history_index + 1)])
            elif self.history_index == 0:
                self.history_index = -1
                self.command_input.clear()
            event.accept()
        else:
            QLineEdit.keyPressEvent(self.command_input, event)
    
    def _execute_command(self):
        """Execute command in terminal"""
        command = self.command_input.text().strip()
        
        if not command:
            return
        
        # Add to history
        if not self.command_history or self.command_history[-1] != command:
            self.command_history.append(command)
        self.history_index = -1
        
        # Display command
        self.write(f"$ {command}\n")
        self.command_input.clear()
        
        # Handle built-in commands
        if command.startswith("cd "):
            self._handle_cd(command)
            return
        
        if command == "pwd":
            self.write(f"{self.current_directory}\n")
            return
        
        if command == "clear":
            self.clear()
            return
        
        # Execute external command
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=str(self.current_directory),
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.stdout:
                self.write(result.stdout)
            if result.stderr:
                self.write_error(result.stderr)
            
            if result.returncode != 0:
                self.write_error(f"Command exited with code {result.returncode}\n")
        
        except subprocess.TimeoutExpired:
            self.write_error("Command timed out (30 seconds)\n")
        except Exception as e:
            self.write_error(f"Error executing command: {e}\n")
    
    def _handle_cd(self, command: str):
        """Handle cd command"""
        try:
            path = command[3:].strip()
            
            if not path:
                new_dir = Path.home()
            else:
                new_dir = Path(path).expanduser()
                if not new_dir.is_absolute():
                    new_dir = self.current_directory / new_dir
            
            if new_dir.exists() and new_dir.is_dir():
                self.current_directory = new_dir
                self.dir_display.setText(str(self.current_directory))
                self.write(f"Changed directory to: {self.current_directory}\n")
            else:
                self.write_error(f"Directory not found: {path}\n")
        
        except Exception as e:
            self.write_error(f"Error changing directory: {e}\n")
    
    def write(self, text: str):
        """Write text to terminal output"""
        cursor = self.output.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.output.setTextCursor(cursor)
        self.output.ensureCursorVisible()
        self.output_received.emit(text)
    
    def write_error(self, text: str):
        """Write error text to terminal (in red)"""
        cursor = self.output.textCursor()
        cursor.movePosition(QTextCursor.End)
        
        # Create format for error text
        fmt = cursor.charFormat()
        fmt.setForeground(QColor(255, 0, 0))
        cursor.setCharFormat(fmt)
        cursor.insertText(text)
        
        self.output.setTextCursor(cursor)
        self.output.ensureCursorVisible()
        self.error_received.emit(text)
    
    def write_success(self, text: str):
        """Write success text to terminal (in green)"""
        cursor = self.output.textCursor()
        cursor.movePosition(QTextCursor.End)
        
        fmt = cursor.charFormat()
        fmt.setForeground(QColor(0, 200, 0))
        cursor.setCharFormat(fmt)
        cursor.insertText(text)
        
        self.output.setTextCursor(cursor)
        self.output.ensureCursorVisible()
    
    def write_warning(self, text: str):
        """Write warning text to terminal (in yellow)"""
        cursor = self.output.textCursor()
        cursor.movePosition(QTextCursor.End)
        
        fmt = cursor.charFormat()
        fmt.setForeground(QColor(255, 200, 0))
        cursor.setCharFormat(fmt)
        cursor.insertText(text)
        
        self.output.setTextCursor(cursor)
        self.output.ensureCursorVisible()
    
    def clear(self):
        """Clear terminal output"""
        self.output.clear()
        self.command_history.clear()
        self.history_index = -1
    
    def set_directory(self, directory: str):
        """Set current working directory"""
        path = Path(directory)
        if path.exists() and path.is_dir():
            self.current_directory = path
            self.dir_display.setText(str(self.current_directory))
        else:
            logger.warning(f"Invalid directory: {directory}")
    
    def get_directory(self) -> Path:
        """Get current working directory"""
        return self.current_directory
    
    def execute_command(self, command: str):
        """Execute a command programmatically"""
        self.command_input.setText(command)
        self._execute_command()
    
    def _apply_theme(self):
        """Apply theme to terminal"""
        if self.theme_manager:
            try:
                theme_name = self.theme_manager.current_theme
                
                # Set output area colors based on theme
                if theme_name == 'light':
                    bg_color = '#ffffff'
                    fg_color = '#333333'
                else:
                    bg_color = '#1e1e1e'
                    fg_color = '#d4d4d4'
                
                self.output.setStyleSheet(f"""
                    QPlainTextEdit {{
                        background-color: {bg_color};
                        color: {fg_color};
                        border: 1px solid {'#3e3e3e' if theme_name == 'dark' else '#cccccc'};
                    }}
                """)
                
                self.command_input.setStyleSheet(f"""
                    QLineEdit {{
                        background-color: {bg_color};
                        color: {fg_color};
                        border: 1px solid {'#3e3e3e' if theme_name == 'dark' else '#cccccc'};
                        padding: 4px;
                    }}
                """)
            except Exception as e:
                logger.error(f"Failed to apply theme to terminal: {e}")
    
    def set_theme(self, theme_name: str):
        """Set terminal theme"""
        self._apply_theme()
