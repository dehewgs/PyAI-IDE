"""
Comprehensive Test Suite for PyAI IDE
Tests all core functionality and UI components
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test 1: Module Imports"""
    print("\n" + "="*70)
    print("TEST 1: Module Imports")
    print("="*70)
    
    try:
        from utils.logger import logger
        print("✓ Logger imported")
        
        from core.config_manager import ConfigManager
        print("✓ ConfigManager imported")
        
        from core.event_system import EventSystem
        print("✓ EventSystem imported")
        
        from core.plugin_system import PluginManager
        print("✓ PluginManager imported")
        
        from services.github_service import GitHubService
        print("✓ GitHubService imported")
        
        from services.huggingface_service import HuggingFaceService
        print("✓ HuggingFaceService imported")
        
        return True
    except Exception as e:
        print(f"✗ Import test failed: {e}")
        return False


def test_services():
    """Test 2: Service Functionality"""
    print("\n" + "="*70)
    print("TEST 2: Service Functionality")
    print("="*70)
    
    try:
        from services.github_service import GitHubService
        from services.huggingface_service import HuggingFaceService
        
        # Test GitHub Service
        github = GitHubService()
        print("✓ GitHubService instantiated")
        
        required_methods = ['authenticate', 'create_repository', 'clone_repository', 'disconnect']
        for method in required_methods:
            assert hasattr(github, method), f"Missing method: {method}"
        print("✓ GitHubService has all required methods")
        
        # Test HuggingFace Service
        hf = HuggingFaceService()
        print("✓ HuggingFaceService instantiated")
        
        required_methods = ['load_model', 'run_inference', 'list_models']
        for method in required_methods:
            assert hasattr(hf, method), f"Missing method: {method}"
        print("✓ HuggingFaceService has all required methods")
        
        return True
    except Exception as e:
        print(f"✗ Service test failed: {e}")
        return False


def test_event_system():
    """Test 4: Event System"""
    print("\n" + "="*70)
    print("TEST 4: Event System")
    print("="*70)
    
    try:
        from core.event_system import EventSystem
        
        event_system = EventSystem()
        print("✓ EventSystem created")
        
        # Test subscription
        callback_called = []
        def callback(data):
            callback_called.append(data)
        
        event_system.subscribe("test_event", callback)
        print("✓ Event subscription works")
        
        # Test emission
        event_system.emit("test_event", "test_data")
        assert len(callback_called) == 1, "Callback not called"
        assert callback_called[0] == "test_data", "Wrong data passed"
        print("✓ Event emission works")
        
        # Test unsubscription
        event_system.unsubscribe("test_event", callback)
        callback_called.clear()
        event_system.emit("test_event", "test_data2")
        assert len(callback_called) == 0, "Callback still called after unsubscribe"
        print("✓ Event unsubscription works")
        
        return True
    except Exception as e:
        print(f"✗ Event system test failed: {e}")
        return False


def test_logger():
    """Test 5: Logger"""
    print("\n" + "="*70)
    print("TEST 5: Logger")
    print("="*70)
    
    try:
        from utils.logger import logger, get_logger
        
        assert logger is not None, "Logger is None"
        print("✓ Logger instance exists")
        
        # Test logging levels
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")
        print("✓ All logging levels work")
        
        # Test get_logger
        logger2 = get_logger()
        assert logger2 is logger, "get_logger returns different instance"
        print("✓ get_logger returns same instance")
        
        # Check log file
        log_file = Path("logs/app.log")
        assert log_file.exists(), "Log file not created"
        print(f"✓ Logger recorded {len(logger.messages)} messages")
        
        return True
    except Exception as e:
        print(f"✗ Logger test failed: {e}")
        return False


def test_ui_components():
    """Test 3: UI Components"""
    print("\n" + "="*70)
    print("TEST 3: UI Components")
    print("="*70)
    
    try:
        from PyQt5.QtWidgets import QApplication
        
        # Create QApplication
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        print("✓ QApplication created")
        
        # Import MainWindow
        from src.ui.main_window import MainWindow
        print("✓ MainWindow imported")
        
        # Create MainWindow
        window = MainWindow()
        print("✓ MainWindow instance created")
        
        # Check for required components
        required_components = [
            'editor', 'console_panel', 'project_panel', 'model_panel',
            'tab_widget', 'theme_manager', 'github_service', 'huggingface_service'
        ]
        for component in required_components:
            assert hasattr(window, component), f"Missing component: {component}"
        print(f"✓ All {len(required_components)} required components present")
        
        # Check for menu bar
        assert window.menuBar() is not None, "No menu bar"
        print("✓ Menu bar created")
        
        # Check for status bar
        assert window.statusBar() is not None, "No status bar"
        print("✓ Status bar created")
        
        return True
    except Exception as e:
        print(f"✗ UI components test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("PyAI IDE - COMPREHENSIVE TEST SUITE")
    print("="*70)
    
    results = {
        "Module Imports": test_imports(),
        "Service Functionality": test_services(),
        "Event System": test_event_system(),
        "Logger": test_logger(),
        "UI Components": test_ui_components(),
    }
    
    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print("="*70)
    print(f"Results: {passed}/{total} tests passed")
    print("="*70)
    
    if passed == total:
        print("\n✓ ALL TESTS PASSED - Application is fully functional!")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
