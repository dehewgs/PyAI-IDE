"""
PyAI IDE - Main Application Entry Point
A lightweight, fully-featured Python IDE with HuggingFace and GitHub integration
"""

import sys
import traceback
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from PyQt5.QtWidgets import QApplication, QMessageBox
    from ui.main_window import MainWindow
except ImportError as e:
    print(f"Error: Failed to import required modules: {e}")
    print("\nPlease ensure all dependencies are installed:")
    print("  pip install -r requirements.txt")
    sys.exit(1)


def main():
    """Main application entry point"""
    try:
        app = QApplication(sys.argv)
        
        # Set application metadata
        app.setApplicationName("PyAI IDE")
        app.setApplicationVersion("1.0.0")
        
        # Create and show main window
        window = MainWindow()
        window.show()
        
        # Run application
        sys.exit(app.exec_())
        
    except Exception as e:
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
                f"Please check the console output for more details."
            )
        except:
            pass
        
        sys.exit(1)


if __name__ == '__main__':
    main()
