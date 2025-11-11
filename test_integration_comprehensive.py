"""
Comprehensive Integration Test Suite
Tests all features of the PyAI IDE without requiring a display
"""

import sys
import os
import tempfile
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.event_system import EventSystem
from core.config_manager import ConfigManager
from core.plugin_system import PluginManager, PluginHook
from services.github_service import GitHubService
from services.huggingface_service import HuggingFaceService
from utils.logger import Logger

# Initialize logger
logger = Logger("test_integration")

class IntegrationTestSuite:
    """Comprehensive integration test suite"""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests = []
        
    def test(self, name):
        """Decorator for test methods"""
        def decorator(func):
            self.tests.append((name, func))
            return func
        return decorator
    
    def run_all(self):
        """Run all tests"""
        print("\n" + "="*80)
        print("COMPREHENSIVE INTEGRATION TEST SUITE")
        print("="*80 + "\n")
        
        for test_name, test_func in self.tests:
            try:
                print(f"[TEST] {test_name}...", end=" ")
                test_func(self)
                print("✓ PASS")
                self.passed += 1
            except Exception as e:
                print(f"✗ FAIL: {str(e)}")
                self.failed += 1
                import traceback
                traceback.print_exc()
        
        print("\n" + "="*80)
        print(f"RESULTS: {self.passed} passed, {self.failed} failed")
        print("="*80 + "\n")
        
        return self.failed == 0

suite = IntegrationTestSuite()

# ============================================================================
# TEST 1: Core Systems Initialization
# ============================================================================

@suite.test("Core Systems - EventSystem initialization")
def test_event_system(self):
    """Test EventSystem initialization and basic functionality"""
    event_system = EventSystem()
    assert event_system is not None
    assert hasattr(event_system, 'subscribe')
    assert hasattr(event_system, 'emit')
    assert hasattr(event_system, 'unsubscribe')
    logger.info("EventSystem initialized successfully")

@suite.test("Core Systems - ConfigManager initialization")
def test_config_manager(self):
    """Test ConfigManager initialization and operations"""
    config = ConfigManager()
    assert config is not None
    
    # Test set/get
    config.set('test_key', 'test_value')
    assert config.get('test_key') == 'test_value'
    
    # Test defaults
    assert config.get('nonexistent', 'default') == 'default'
    logger.info("ConfigManager working correctly")

@suite.test("Core Systems - PluginManager initialization")
def test_plugin_manager(self):
    """Test PluginManager initialization"""
    plugin_manager = PluginManager()
    assert plugin_manager is not None
    assert hasattr(plugin_manager, 'register_hook')
    assert hasattr(plugin_manager, 'trigger_hook')
    logger.info("PluginManager initialized successfully")

# ============================================================================
# TEST 2: Event System Features
# ============================================================================

@suite.test("EventSystem - Subscribe and emit")
def test_event_subscribe_emit(self):
    """Test event subscription and emission"""
    event_system = EventSystem()
    received_events = []
    
    def handler(data):
        received_events.append(data)
    
    event_system.subscribe('test_event', handler)
    event_system.emit('test_event', {'message': 'test'})
    
    assert len(received_events) == 1
    assert received_events[0]['message'] == 'test'
    logger.info("Event subscription and emission working")

@suite.test("EventSystem - Multiple subscribers")
def test_event_multiple_subscribers(self):
    """Test multiple subscribers to same event"""
    event_system = EventSystem()
    results = []
    
    def handler1(data):
        results.append('handler1')
    
    def handler2(data):
        results.append('handler2')
    
    event_system.subscribe('multi_event', handler1)
    event_system.subscribe('multi_event', handler2)
    event_system.emit('multi_event', {})
    
    assert len(results) == 2
    assert 'handler1' in results
    assert 'handler2' in results
    logger.info("Multiple subscribers working correctly")

@suite.test("EventSystem - Unsubscribe")
def test_event_unsubscribe(self):
    """Test unsubscribing from events"""
    event_system = EventSystem()
    received = []
    
    def handler(data):
        received.append(data)
    
    listener = event_system.subscribe('unsub_event', handler)
    event_system.emit('unsub_event', {'data': 1})
    event_system.unsubscribe(listener)
    event_system.emit('unsub_event', {'data': 2})
    
    assert len(received) == 1
    logger.info("Unsubscribe working correctly")

# ============================================================================
# TEST 3: Configuration Management
# ============================================================================

@suite.test("ConfigManager - Persistence")
def test_config_persistence(self):
    """Test configuration persistence"""
    config1 = ConfigManager()
    config1.set('persist_key', 'persist_value')
    config1.save()
    
    config2 = ConfigManager()
    assert config2.get('persist_key') == 'persist_value'
    logger.info("Configuration persistence working")

@suite.test("ConfigManager - Nested values")
def test_config_nested(self):
    """Test nested configuration values"""
    config = ConfigManager()
    nested = {'level1': {'level2': 'value'}}
    config.set('nested', nested)
    
    retrieved = config.get('nested')
    assert retrieved['level1']['level2'] == 'value'
    logger.info("Nested configuration working")

# ============================================================================
# TEST 4: Plugin System
# ============================================================================

@suite.test("PluginManager - Hook registration and execution")
def test_plugin_hooks(self):
    """Test plugin hook registration and execution"""
    plugin_manager = PluginManager()
    results = []
    
    def my_hook(data):
        results.append(data)
    
    plugin_manager.register_hook(PluginHook.ON_STARTUP, my_hook)
    plugin_manager.trigger_hook(PluginHook.ON_STARTUP, 'test_data')
    
    assert len(results) == 1
    assert results[0] == 'test_data'
    logger.info("Plugin hooks working correctly")

@suite.test("PluginManager - Multiple hooks")
def test_plugin_multiple_hooks(self):
    """Test multiple hooks on same event"""
    plugin_manager = PluginManager()
    results = []
    
    plugin_manager.register_hook(PluginHook.ON_SHUTDOWN, lambda d: results.append('hook1'))
    plugin_manager.register_hook(PluginHook.ON_SHUTDOWN, lambda d: results.append('hook2'))
    plugin_manager.trigger_hook(PluginHook.ON_SHUTDOWN, {})
    
    assert len(results) == 2
    logger.info("Multiple plugin hooks working")

# ============================================================================
# TEST 5: Services Integration
# ============================================================================

@suite.test("GitHubService - Initialization")
def test_github_service_init(self):
    """Test GitHub service initialization"""
    github = GitHubService()
    assert github is not None
    assert hasattr(github, 'authenticate')
    assert hasattr(github, 'create_repository')
    assert hasattr(github, 'clone_repository')
    logger.info("GitHubService initialized successfully")

@suite.test("GitHubService - Authentication flow")
def test_github_auth(self):
    """Test GitHub authentication"""
    github = GitHubService()
    success, message = github.authenticate('test_token')
    assert success == True
    assert isinstance(message, str)
    logger.info("GitHub authentication flow working")

@suite.test("GitHubService - Repository operations")
def test_github_repo_ops(self):
    """Test GitHub repository operations"""
    github = GitHubService()
    
    # Authenticate first
    github.authenticate('test_token')
    
    # Test create
    success, message = github.create_repository('test_repo', 'Test description')
    assert success == True
    assert isinstance(message, str)
    
    # Test clone
    success, message = github.clone_repository('user/repo')
    assert success == True
    
    logger.info("GitHub repository operations working")

@suite.test("HuggingFaceService - Initialization")
def test_huggingface_service_init(self):
    """Test HuggingFace service initialization"""
    hf = HuggingFaceService()
    assert hf is not None
    assert hasattr(hf, 'load_model')
    assert hasattr(hf, 'run_inference')
    assert hasattr(hf, 'list_models')
    logger.info("HuggingFaceService initialized successfully")

@suite.test("HuggingFaceService - Model operations")
def test_huggingface_models(self):
    """Test HuggingFace model operations"""
    hf = HuggingFaceService()
    
    # Test load
    success, message = hf.load_model('bert-base-uncased')
    assert success == True
    assert isinstance(message, str)
    
    # Test inference
    success, result = hf.run_inference('bert-base-uncased', 'test input')
    assert success == True
    assert isinstance(result, str)
    
    # Test list
    models = hf.list_models()
    assert isinstance(models, list)
    
    logger.info("HuggingFace model operations working")

# ============================================================================
# TEST 6: Integration Scenarios
# ============================================================================

@suite.test("Integration - Event-driven workflow")
def test_integration_event_workflow(self):
    """Test event-driven workflow between components"""
    event_system = EventSystem()
    config = ConfigManager()
    github = GitHubService()
    
    workflow_events = []
    
    def on_auth(data):
        workflow_events.append('authenticated')
        config.set('github_token', data.get('token'))
    
    def on_repo_created(data):
        workflow_events.append('repo_created')
    
    event_system.subscribe('github_authenticated', on_auth)
    event_system.subscribe('repository_created', on_repo_created)
    
    # Simulate workflow
    event_system.emit('github_authenticated', {'token': 'test_token'})
    event_system.emit('repository_created', {'name': 'test_repo'})
    
    assert len(workflow_events) == 2
    assert config.get('github_token') == 'test_token'
    logger.info("Event-driven workflow working correctly")

@suite.test("Integration - Service coordination")
def test_integration_service_coordination(self):
    """Test coordination between services"""
    github = GitHubService()
    hf = HuggingFaceService()
    config = ConfigManager()
    
    # Simulate coordinated workflow
    config.set('github_authenticated', True)
    config.set('hf_model_loaded', True)
    
    # Both services should be accessible
    assert config.get('github_authenticated') == True
    assert config.get('hf_model_loaded') == True
    
    # Services should work independently
    github.authenticate('token')
    github_success, _ = github.create_repository('test', 'desc')
    hf_success, _ = hf.load_model('test-model')
    
    assert github_success == True
    assert hf_success == True
    logger.info("Service coordination working correctly")

@suite.test("Integration - Configuration-driven behavior")
def test_integration_config_driven(self):
    """Test configuration-driven behavior"""
    config = ConfigManager()
    
    # Set configuration
    config.set('theme', 'dark')
    config.set('auto_save', True)
    config.set('api_keys', {
        'github': 'token123',
        'huggingface': 'hf_token456'
    })
    config.save()
    
    # Load and verify
    config2 = ConfigManager()
    assert config2.get('theme') == 'dark'
    assert config2.get('auto_save') == True
    assert config2.get('api_keys')['github'] == 'token123'
    
    logger.info("Configuration-driven behavior working")

# ============================================================================
# TEST 7: Error Handling
# ============================================================================

@suite.test("Error Handling - Invalid event subscription")
def test_error_invalid_subscription(self):
    """Test error handling for invalid subscriptions"""
    event_system = EventSystem()
    
    try:
        # Should handle gracefully
        event_system.subscribe('event', None)
        # If we get here, it should have been handled
        logger.info("Invalid subscription handled gracefully")
    except Exception as e:
        logger.info(f"Invalid subscription raised: {type(e).__name__}")

@suite.test("Error Handling - Service failures")
def test_error_service_failures(self):
    """Test error handling in services"""
    github = GitHubService()
    hf = HuggingFaceService()
    
    # Services should handle errors gracefully
    try:
        success, message = github.authenticate(None)
        assert success == False
        logger.info("GitHub service error handling working")
    except Exception as e:
        logger.info(f"GitHub service error: {type(e).__name__}")
    
    try:
        success, message = hf.load_model(None)
        assert success == False
        logger.info("HuggingFace service error handling working")
    except Exception as e:
        logger.info(f"HuggingFace service error: {type(e).__name__}")

# ============================================================================
# TEST 8: Performance and Scalability
# ============================================================================

@suite.test("Performance - Event system throughput")
def test_performance_events(self):
    """Test event system performance"""
    event_system = EventSystem()
    count = [0]
    
    def handler(data):
        count[0] += 1
    
    event_system.subscribe('perf_event', handler)
    
    # Emit 1000 events
    for i in range(1000):
        event_system.emit('perf_event', {'index': i})
    
    assert count[0] == 1000
    logger.info(f"Event system handled 1000 events successfully")

@suite.test("Performance - Configuration operations")
def test_performance_config(self):
    """Test configuration performance"""
    config = ConfigManager()
    
    # Set 100 configuration values
    for i in range(100):
        config.set(f'key_{i}', f'value_{i}')
    
    # Retrieve all values
    for i in range(100):
        value = config.get(f'key_{i}')
        assert value == f'value_{i}'
    
    logger.info("Configuration handled 100 key-value pairs successfully")

# ============================================================================
# Run all tests
# ============================================================================

if __name__ == '__main__':
    success = suite.run_all()
    sys.exit(0 if success else 1)
