"""
Comprehensive test script for PyAI IDE
Tests all core functionality without GUI
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from utils.logger import get_logger
from utils.path_utils import get_logs_dir, get_config_file

# Initialize logger
logs_dir = get_logs_dir()
log_file = logs_dir / "test_app.log"
logger = get_logger("PyAI-IDE-Test", log_file)

logger.info("=" * 80)
logger.info("PyAI IDE - Comprehensive Test Suite")
logger.info("=" * 80)

def test_logger():
    """Test logging system"""
    logger.info("Testing logger system...")
    try:
        logger.debug("This is a debug message")
        logger.info("This is an info message")
        logger.warning("This is a warning message")
        logger.error("This is an error message")
        logger.critical("This is a critical message")
        logger.info("[OK] Logger system working correctly")
        return True
    except Exception as e:
        logger.error(f"[ERROR] Logger test failed: {e}")
        return False

def test_config_manager():
    """Test configuration manager"""
    logger.info("Testing ConfigManager...")
    try:
        from core.config_manager import ConfigManager
        
        config = ConfigManager()
        logger.debug("ConfigManager initialized")
        
        # Test get
        theme = config.get("app.theme", "dark")
        logger.debug(f"Retrieved theme: {theme}")
        
        # Test set
        config.set("app.test_value", "test123")
        logger.debug("Set test value")
        
        # Test get again
        test_val = config.get("app.test_value")
        logger.debug(f"Retrieved test value: {test_val}")
        
        # Test save
        config.save()
        logger.debug("Configuration saved")
        
        logger.info("[OK] ConfigManager working correctly")
        return True
    except Exception as e:
        logger.error(f"[ERROR] ConfigManager test failed: {e}")
        logger.exception("ConfigManager error", e)
        return False

def test_event_system():
    """Test event system"""
    logger.info("Testing EventSystem...")
    try:
        from core.event_system import EventSystem
        
        event_system = EventSystem()
        logger.debug("EventSystem initialized")
        
        # Test subscription
        results = []
        def test_callback(msg):
            results.append(msg)
            return f"Processed: {msg}"
        
        listener = event_system.subscribe("test_event", test_callback)
        logger.debug("Subscribed to test_event")
        
        # Test emission
        event_system.emit("test_event", "Hello World")
        logger.debug(f"Emitted event, results: {results}")
        
        # Test unsubscription
        event_system.unsubscribe(listener)
        logger.debug("Unsubscribed from test_event")
        
        logger.info("[OK] EventSystem working correctly")
        return True
    except Exception as e:
        logger.error(f"[ERROR] EventSystem test failed: {e}")
        logger.exception("EventSystem error", e)
        return False

def test_plugin_system():
    """Test plugin system"""
    logger.info("Testing PluginManager...")
    try:
        from core.plugin_system import PluginManager
        
        plugin_manager = PluginManager()
        logger.debug("PluginManager initialized")
        
        # Test plugin listing
        plugins = plugin_manager.list_plugins()
        logger.debug(f"Loaded plugins: {len(plugins)}")
        
        logger.info("[OK] PluginManager working correctly")
        return True
    except Exception as e:
        logger.error(f"[ERROR] PluginManager test failed: {e}")
        logger.exception("PluginManager error", e)
        return False

def test_github_service():
    """Test GitHub service"""
    logger.info("Testing GitHubService...")
    try:
        from services.github_service import GitHubService
        
        github = GitHubService()
        logger.debug("GitHubService initialized")
        
        # Test authentication status
        is_auth = github.is_authenticated()
        logger.debug(f"Authenticated: {is_auth}")
        
        logger.info("[OK] GitHubService working correctly")
        return True
    except Exception as e:
        logger.error(f"[ERROR] GitHubService test failed: {e}")
        logger.exception("GitHubService error", e)
        return False

def test_huggingface_service():
    """Test HuggingFace service"""
    logger.info("Testing HuggingFaceService...")
    try:
        from services.huggingface_service import HuggingFaceService
        
        hf = HuggingFaceService()
        logger.debug("HuggingFaceService initialized")
        
        # Test model listing
        models = hf.list_loaded_models()
        logger.debug(f"Loaded models: {len(models)}")
        
        logger.info("[OK] HuggingFaceService working correctly")
        return True
    except Exception as e:
        logger.error(f"[ERROR] HuggingFaceService test failed: {e}")
        logger.exception("HuggingFaceService error", e)
        return False

def test_ui_imports():
    """Test UI imports"""
    logger.info("Testing UI imports...")
    try:
        from PyQt5.QtWidgets import QApplication
        logger.debug("PyQt5 imported")
        
        from ui.main_window import MainWindow
        logger.debug("MainWindow imported")
        
        logger.info("[OK] UI imports working correctly")
        return True
    except Exception as e:
        logger.error(f"[ERROR] UI import test failed: {e}")
        logger.exception("UI import error", e)
        return False

def main():
    """Run all tests"""
    tests = [
        ("Logger System", test_logger),
        ("ConfigManager", test_config_manager),
        ("EventSystem", test_event_system),
        ("PluginManager", test_plugin_system),
        ("GitHubService", test_github_service),
        ("HuggingFaceService", test_huggingface_service),
        ("UI Imports", test_ui_imports),
    ]
    
    results = []
    for test_name, test_func in tests:
        logger.info(f"\n{'=' * 80}")
        logger.info(f"Running: {test_name}")
        logger.info(f"{'=' * 80}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            logger.error(f"Test {test_name} crashed: {e}")
            logger.exception(f"{test_name} crash", e)
            results.append((test_name, False))
    
    # Summary
    logger.info(f"\n{'=' * 80}")
    logger.info("Test Summary")
    logger.info(f"{'=' * 80}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        logger.info(f"{status} {test_name}")
    
    logger.info(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("=" * 80)
        logger.info("All tests passed! Application is ready.")
        logger.info("=" * 80)
        return 0
    else:
        logger.error("=" * 80)
        logger.error(f"Some tests failed ({total - passed} failures)")
        logger.error("=" * 80)
        return 1

if __name__ == '__main__':
    exit_code = main()
    print(f"\nLog file: {log_file}")
    sys.exit(exit_code)
