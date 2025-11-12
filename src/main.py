"""
PyAI IDE - Main Application Entry Point
A lightweight, fully-featured Python IDE with HuggingFace and GitHub integration
"""

import sys
import traceback
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Initialize logger first
from utils.logger import get_logger
from utils.path_utils import get_logs_dir

# Create logger with file output
logs_dir = get_logs_dir()
log_file = logs_dir / "pyai_ide.log"
logger = get_logger("PyAI-IDE", log_file)

logger.info("=" * 80)
logger.info("PyAI IDE - Application Starting")
logger.info("=" * 80)
logger.info(f"Python version: {sys.version}")
logger.info(f"Log file: {log_file}")

try:
    logger.debug("Importing PyQt5...")
    from PyQt5.QtWidgets import QApplication, QMessageBox
    logger.debug("PyQt5 imported successfully")
    
    logger.debug("Importing MainWindow...")
    from ui.main_window import MainWindow
    logger.debug("MainWindow imported successfully")
    
except ImportError as e:
    logger.critical(f"Failed to import required modules: {e}")
    logger.exception("Import error", e)
    print(f"Error: Failed to import required modules: {e}")
    print("\nPlease ensure all dependencies are installed:")
    print("  pip install -r requirements.txt")
    sys.exit(1)


def main():
    """Main application entry point"""
    try:
        logger.info("Creating QApplication...")
        # Initialize AppData manager first to ensure directories exist
        from core.app_data_manager import AppDataManager
        app_data_manager = AppDataManager()
        logger.info(f"AppData initialized at: {app_data_manager.get_app_data_path()}")
        
        app = QApplication(sys.argv)
        
        # Set application metadata
        app.setApplicationName("PyAI IDE")
        app.setApplicationVersion("1.0.0")
        logger.debug("Application metadata set")
        
        # Set application style to Fusion to ensure stylesheets work properly
        from PyQt5.QtWidgets import QStyleFactory
        app.setStyle(QStyleFactory.create('Fusion'))
        logger.debug("Application style set to Fusion")
        
        # Create and show main window
        logger.info("Creating MainWindow...")
        window = MainWindow(app)
        logger.info("MainWindow created successfully")
        
        logger.info("Showing MainWindow...")
        window.show()
        logger.info("MainWindow displayed")
        
        # Run application
        logger.info("Starting event loop...")
        exit_code = app.exec_()
        logger.info(f"Event loop exited with code: {exit_code}")
        
        sys.exit(exit_code)
        
    except Exception as e:
        logger.critical(f"Fatal Error: {e}")
        logger.exception("Fatal application error", e)
        print(f"Fatal Error: {e}")
        print("\nTraceback:")
        traceback.print_exc()
        
        # Try to show error dialog if possible
        try:
            app = QApplication.instance()
            if app is None:
                app = QApplication(sys.argv)
            
            QMessageBox.critical(
                None,
                "PyAI IDE - Fatal Error",
                f"An error occurred while starting the application:\n\n{str(e)}\n\n"
                f"Please check the console output and log file for more details.\n"
                f"Log file: {log_file}"
            )
        except Exception as dialog_error:
            logger.error(f"Failed to show error dialog: {dialog_error}")
        
        sys.exit(1)


if __name__ == '__main__':
    main()
