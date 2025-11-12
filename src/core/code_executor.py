"""
Code Executor for PyAI IDE
Handles execution of user code with output capture
"""

import subprocess
import sys
import threading
from pathlib import Path
from typing import Callable, Optional
from PyQt5.QtCore import QObject, pyqtSignal
from utils.logger import logger


class CodeExecutor(QObject):
    """Executes code and captures output"""
    
    # Signals
    output_received = pyqtSignal(str)  # stdout
    error_received = pyqtSignal(str)   # stderr
    execution_finished = pyqtSignal(int)  # return code
    execution_started = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.process: Optional[subprocess.Popen] = None
        self.is_running = False
    
    def execute(self, file_path: str, working_dir: Optional[str] = None):
        """Alias for execute_python for backward compatibility"""
        return self.execute_python(file_path, working_dir)
    
    def execute_python(self, file_path: str, working_dir: Optional[str] = None):
        """Execute Python file
        
        Args:
            file_path: Path to Python file to execute
            working_dir: Working directory for execution
        """
        if self.is_running:
            self.error_received.emit("Execution already in progress")
            return
        
        file_path = Path(file_path)
        if not file_path.exists():
            self.error_received.emit(f"File not found: {file_path}")
            return
        
        if working_dir is None:
            working_dir = str(file_path.parent)
        
        self.execution_started.emit()
        self.is_running = True
        
        # Run in separate thread to avoid blocking UI
        thread = threading.Thread(
            target=self._execute_python_thread,
            args=(str(file_path), working_dir)
        )
        thread.daemon = True
        thread.start()
    
    def _execute_python_thread(self, file_path: str, working_dir: str):
        """Execute Python file in separate thread"""
        try:
            self.output_received.emit(f"Executing: {file_path}\n")
            self.output_received.emit(f"Working directory: {working_dir}\n")
            self.output_received.emit("-" * 60 + "\n")
            
            # Create process
            self.process = subprocess.Popen(
                [sys.executable, file_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=working_dir,
                bufsize=1
            )
            
            # Read output in real-time
            while True:
                output = self.process.stdout.readline()
                if output:
                    self.output_received.emit(output)
                else:
                    break
            
            # Read any remaining stderr
            stderr = self.process.stderr.read()
            if stderr:
                self.error_received.emit(stderr)
            
            # Wait for process to finish
            return_code = self.process.wait()
            
            self.output_received.emit("-" * 60 + "\n")
            self.output_received.emit(f"Process exited with code: {return_code}\n")
            self.execution_finished.emit(return_code)
            
        except Exception as e:
            self.error_received.emit(f"Execution error: {str(e)}\n")
            self.execution_finished.emit(-1)
        finally:
            self.is_running = False
            self.process = None
    
    def execute_project(self, project_dir: str, entry_point: str = "main.py"):
        """Execute project from directory
        
        Args:
            project_dir: Project directory path
            entry_point: Entry point file (default: main.py)
        """
        project_path = Path(project_dir)
        entry_file = project_path / entry_point
        
        if not entry_file.exists():
            self.error_received.emit(f"Entry point not found: {entry_file}")
            return
        
        self.execute_python(str(entry_file), str(project_path))
    
    def stop(self):
        """Alias for stop_execution for backward compatibility"""
        return self.stop_execution()
    
    def stop_execution(self):
        """Stop current execution"""
        if self.process and self.is_running:
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
                self.output_received.emit("\nExecution terminated by user\n")
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.output_received.emit("\nExecution forcefully terminated\n")
            finally:
                self.is_running = False
                self.process = None
    
    def is_executing(self) -> bool:
        """Check if code is currently executing"""
        return self.is_running


class LanguageExecutor:
    """Factory for language-specific executors"""
    
    _executors = {}
    
    @classmethod
    def register_executor(cls, language: str, executor_class):
        """Register executor for language"""
        cls._executors[language] = executor_class
    
    @classmethod
    def get_executor(cls, language: str) -> Optional[CodeExecutor]:
        """Get executor for language"""
        executor_class = cls._executors.get(language)
        if executor_class:
            return executor_class()
        return None
    
    @classmethod
    def get_supported_languages(cls) -> list:
        """Get list of supported languages"""
        return list(cls._executors.keys())


# Register default Python executor
LanguageExecutor.register_executor('python', CodeExecutor)
