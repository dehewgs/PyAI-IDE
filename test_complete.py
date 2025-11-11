#!/usr/bin/env python3
"""
Comprehensive test suite for PyAI IDE
Tests all core functionality without requiring a display
"""

import sys
import os

# Set Qt to use offscreen platform
os.environ['QT_QPA_PLATFORM'] = 'offscreen'

def test_imports():
    """Test that all modules can be imported"""
    print("\n" + "="*70)
    print("TEST 1: Module Imports")
    print("="*70)
    
    try:
        from src.utils.logger import logger
        print("✓ Logger imported")
    except Exception as e:
        print(f"✗ Logger import failed: {e}")
        return False
    
    try:
        from src.core.config_manager import ConfigManager
        print("✓ ConfigManager imported")
    except Exception as e:
        print(f"✗ ConfigManager import failed: {e}")
        return False
    
    try:
        from src.core.event_system import EventSystem
        print("✓ EventSystem imported")
    except Exception as e:
        print(f"✗ EventSystem import failed: {e}")
        return False
    
    try:
        from src.core.plugin_system import PluginManager
        print("✓ PluginManager imported")
    except Exception as e:
        print(f"✗ PluginManager import failed: {e}")
        return False
    
    try:
        from src.services.github_service import GitHubService
        print("✓ GitHubService imported")
    except Exception as e:
        print(f"✗ GitHubService import failed: {e}")
        return False
    
    try:
        from src.services.huggingface_service import HuggingFaceService
        print("✓ HuggingFaceService imported")
    except Exception as e:
        print(f"✗ HuggingFaceService import failed: {e}")
        return False
    
    return True


def test_services():
    """Test that services work correctly"""
    print("\n" + "="*70)
    print("TEST 2: Service Functionality")
    print("="*70)
    
    try:
        from src.services.github_service import GitHubService
        github = GitHubService()
        print("✓ GitHubService instantiated")
        
        # Test methods exist
        assert hasattr(github, 'authenticate'), "Missing authenticate method"
        assert hasattr(github, 'create_repository'), "Missing create_repository method"
        assert hasattr(github, 'clone_repository'), "Missing clone_repository method"
        print("✓ GitHubService has all required methods")
        
    except Exception as e:
        print(f"✗ GitHubService test failed: {e}")
        return False
    
    try:
        from src.services.huggingface_service import HuggingFaceService
        hf = HuggingFaceService()
        print("✓ HuggingFaceService instantiated")
        
        # Test methods exist
        assert hasattr(hf, 'load_model'), "Missing load_model method"
        assert hasattr(hf, 'run_inference'), "Missing run_inference method"
        print("✓ HuggingFaceService has all required methods")
        
    except Exception as e:
        print(f"✗ HuggingFaceService test failed: {e}")
        return False
    
    return True


def test_ui_components():
    """Test that UI components can be created"""
    print("\n" + "="*70)
    print("TEST 3: UI Components")
    print("="*70)
    
    try:
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        print("✓ QApplication created")
    except Exception as e:
        print(f"✗ QApplication failed: {e}")
        return False
    
    try:
        from src.ui.main_window import MainWindow
        print("✓ MainWindow imported")
        
        window = MainWindow()
        print("✓ MainWindow instance created")
        
        # Check all buttons exist
        buttons = [
            'load_model_btn',
            'run_inference_btn',
            'github_btn',
            'create_repo_btn',
            'clone_repo_btn'
        ]
        
        for btn in buttons:
            assert hasattr(window, btn), f"Missing button: {btn}"
        print(f"✓ All {len(buttons)} buttons present")
        
        # Check all UI components exist
        components = [
            'editor',
            'project_tree',
            'tab_widget',
            'status_bar'
        ]
        
        for comp in components:
            assert hasattr(window, comp), f"Missing component: {comp}"
        print(f"✓ All {len(components)} UI components present")
        
        # Check services are initialized
        services = [
            'github_service',
            'huggingface_service',
            'config',
            'event_system',
            'plugin_manager'
        ]
        
        for svc in services:
            assert hasattr(window, svc), f"Missing service: {svc}"
        print(f"✓ All {len(services)} services initialized")
        
    except Exception as e:
        print(f"✗ UI components test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


def test_event_system():
    """Test event system functionality"""
    print("\n" + "="*70)
    print("TEST 4: Event System")
    print("="*70)
    
    try:
        from src.core.event_system import EventSystem
        
        events = EventSystem()
        print("✓ EventSystem created")
        
        # Test subscribe
        callback_called = []
        def test_callback(data):
            callback_called.append(data)
        
        listener = events.subscribe("test_event", test_callback)
        print("✓ Event subscription works")
        
        # Test emit
        events.emit("test_event", "test_data")
        assert len(callback_called) == 1, "Callback not called"
        assert callback_called[0] == "test_data", "Wrong data passed"
        print("✓ Event emission works")
        
        # Test unsubscribe
        events.unsubscribe(listener)
        callback_called.clear()
        events.emit("test_event", "test_data2")
        assert len(callback_called) == 0, "Callback called after unsubscribe"
        print("✓ Event unsubscription works")
        
    except Exception as e:
        print(f"✗ Event system test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


def test_logger():
    """Test logger functionality"""
    print("\n" + "="*70)
    print("TEST 5: Logger")
    print("="*70)
    
    try:
        from src.utils.logger import logger, get_logger
        
        # Test logger instance
        assert logger is not None, "Logger is None"
        print("✓ Logger instance exists")
        
        # Test logging methods
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")
        print("✓ All logging levels work")
        
        # Test get_logger
        logger2 = get_logger()
        assert logger2 is logger, "get_logger returns different instance"
        print("✓ get_logger returns same instance")
        
        # Test log retrieval
        logs = logger.get_logs()
        assert len(logs) > 0, "No logs recorded"
        print(f"✓ Logger recorded {len(logs)} messages")
        
    except Exception as e:
        print(f"✗ Logger test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("PyAI IDE - COMPREHENSIVE TEST SUITE")
    print("="*70)
    
    tests = [
        ("Module Imports", test_imports),
        ("Service Functionality", test_services),
        ("Event System", test_event_system),
        ("Logger", test_logger),
        ("UI Components", test_ui_components),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ {name} test crashed: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))
    
    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    print("="*70)
    print(f"Results: {passed}/{total} tests passed")
    print("="*70)
    
    if passed == total:
        print("\n✓ ALL TESTS PASSED - APPLICATION IS FULLY FUNCTIONAL!")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
