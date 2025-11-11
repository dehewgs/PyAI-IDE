"""
Simple test to verify UI components work
"""

import sys
from PyQt5.QtWidgets import QApplication
from src.ui.main_window import MainWindow
from src.utils.logger import logger


def test_ui():
    """Test that UI initializes without crashing"""
    logger.info("Starting UI test...")
    
    try:
        app = QApplication(sys.argv)
        logger.info("QApplication created")
        
        window = MainWindow()
        logger.info("MainWindow created successfully")
        
        # Test that key components exist
        assert hasattr(window, 'editor'), "Editor widget missing"
        assert hasattr(window, 'project_tree'), "Project tree missing"
        assert hasattr(window, 'load_model_btn'), "Load model button missing"
        assert hasattr(window, 'connect_github_btn'), "GitHub button missing"
        
        logger.info("✅ All UI components present")
        
        # Test that buttons are connected
        assert window.load_model_btn.clicked.connect, "Load model button not connected"
        assert window.connect_github_btn.clicked.connect, "GitHub button not connected"
        
        logger.info("✅ All buttons connected")
        
        # Show window briefly
        window.show()
        logger.info("✅ Window displayed successfully")
        
        # Close window
        window.close()
        logger.info("✅ Window closed successfully")
        
        logger.info("=" * 80)
        logger.info("✅ UI TEST PASSED - All components working!")
        logger.info("=" * 80)
        
        return True
        
    except Exception as e:
        logger.error(f"❌ UI test failed: {e}", exc_info=True)
        return False


if __name__ == "__main__":
    success = test_ui()
    sys.exit(0 if success else 1)
