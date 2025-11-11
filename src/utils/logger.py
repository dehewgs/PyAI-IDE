"""
Comprehensive logging system for PyAI IDE
Provides detailed debugging and runtime information
"""

import sys
import traceback
from datetime import datetime
from pathlib import Path
from typing import Optional


class Logger:
    """Comprehensive logging system with multiple output levels"""
    
    # Log levels
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4
    
    LEVEL_NAMES = {
        DEBUG: "DEBUG",
        INFO: "INFO",
        WARNING: "WARNING",
        ERROR: "ERROR",
        CRITICAL: "CRITICAL",
    }
    
    LEVEL_COLORS = {
        DEBUG: "\033[36m",      # Cyan
        INFO: "\033[32m",       # Green
        WARNING: "\033[33m",    # Yellow
        ERROR: "\033[31m",      # Red
        CRITICAL: "\033[35m",   # Magenta
    }
    
    RESET_COLOR = "\033[0m"
    
    def __init__(self, name: str = "PyAI-IDE", log_file: Optional[Path] = None):
        """
        Initialize logger.
        
        Args:
            name: Logger name
            log_file: Optional file to write logs to
        """
        self.name = name
        self.log_file = log_file
        self.min_level = self.DEBUG
        self.logs = []
        self.max_logs = 10000
        
        # Create log file if specified
        if self.log_file:
            self.log_file = Path(self.log_file)
            self.log_file.parent.mkdir(parents=True, exist_ok=True)
    
    def _format_message(self, level: int, message: str, extra: Optional[str] = None) -> str:
        """Format log message with timestamp and level"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        level_name = self.LEVEL_NAMES.get(level, "UNKNOWN")
        
        formatted = f"[{timestamp}] [{level_name}] {message}"
        
        if extra:
            formatted += f"\n{extra}"
        
        return formatted
    
    def _write_log(self, level: int, message: str, extra: Optional[str] = None) -> None:
        """Write log to file and memory"""
        formatted = self._format_message(level, message, extra)
        
        # Store in memory
        self.logs.append(formatted)
        if len(self.logs) > self.max_logs:
            self.logs = self.logs[-self.max_logs:]
        
        # Write to file if specified
        if self.log_file:
            try:
                with open(self.log_file, 'a', encoding='utf-8') as f:
                    f.write(formatted + "\n")
            except Exception as e:
                print(f"Failed to write to log file: {e}")
    
    def _print_colored(self, level: int, message: str, extra: Optional[str] = None) -> None:
        """Print colored message to console"""
        formatted = self._format_message(level, message, extra)
        
        # Use colors if terminal supports it
        try:
            color = self.LEVEL_COLORS.get(level, "")
            if color:
                print(f"{color}{formatted}{self.RESET_COLOR}")
            else:
                print(formatted)
        except:
            print(formatted)
    
    def debug(self, message: str, extra: Optional[str] = None) -> None:
        """Log debug message"""
        if self.min_level <= self.DEBUG:
            self._write_log(self.DEBUG, message, extra)
            self._print_colored(self.DEBUG, message, extra)
    
    def info(self, message: str, extra: Optional[str] = None) -> None:
        """Log info message"""
        if self.min_level <= self.INFO:
            self._write_log(self.INFO, message, extra)
            self._print_colored(self.INFO, message, extra)
    
    def warning(self, message: str, extra: Optional[str] = None) -> None:
        """Log warning message"""
        if self.min_level <= self.WARNING:
            self._write_log(self.WARNING, message, extra)
            self._print_colored(self.WARNING, message, extra)
    
    def error(self, message: str, extra: Optional[str] = None) -> None:
        """Log error message"""
        if self.min_level <= self.ERROR:
            self._write_log(self.ERROR, message, extra)
            self._print_colored(self.ERROR, message, extra)
    
    def critical(self, message: str, extra: Optional[str] = None) -> None:
        """Log critical message"""
        if self.min_level <= self.CRITICAL:
            self._write_log(self.CRITICAL, message, extra)
            self._print_colored(self.CRITICAL, message, extra)
    
    def exception(self, message: str, exc: Optional[Exception] = None) -> None:
        """Log exception with traceback"""
        if exc is None:
            exc = sys.exc_info()[1]
        
        tb = traceback.format_exc() if exc else ""
        self.error(message, extra=tb)
    
    def set_level(self, level: int) -> None:
        """Set minimum log level"""
        self.min_level = level
    
    def get_logs(self, level: Optional[int] = None) -> list:
        """Get logs, optionally filtered by level"""
        if level is None:
            return self.logs.copy()
        
        level_name = self.LEVEL_NAMES.get(level, "")
        return [log for log in self.logs if f"[{level_name}]" in log]
    
    def clear_logs(self) -> None:
        """Clear in-memory logs"""
        self.logs.clear()
    
    def get_log_file_path(self) -> Optional[Path]:
        """Get log file path"""
        return self.log_file


# Global logger instance
_logger: Optional[Logger] = None


def get_logger(name: str = "PyAI-IDE", log_file: Optional[Path] = None) -> Logger:
    """Get or create global logger instance"""
    global _logger
    
    if _logger is None:
        _logger = Logger(name, log_file)
    
    return _logger

# Create default logger instance for module-level import
logger = get_logger()
