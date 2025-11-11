"""
Plugin system for PyAI IDE
Provides extensible plugin architecture with hooks and lifecycle management
"""

import importlib.util
import inspect
import sys
from abc import ABC, abstractmethod
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional


class PluginHook(Enum):
    """Available plugin hooks"""
    ON_STARTUP = "on_startup"
    ON_SHUTDOWN = "on_shutdown"
    ON_PROJECT_OPEN = "on_project_open"
    ON_PROJECT_CLOSE = "on_project_close"
    ON_FILE_SAVE = "on_file_save"
    ON_FILE_OPEN = "on_file_open"
    ON_MODEL_LOADED = "on_model_loaded"
    ON_MODEL_UNLOADED = "on_model_unloaded"
    ON_GITHUB_CONNECTED = "on_github_connected"
    ON_GITHUB_DISCONNECTED = "on_github_disconnected"
    BEFORE_CODE_EXECUTION = "before_code_execution"
    AFTER_CODE_EXECUTION = "after_code_execution"


class BasePlugin(ABC):
    """
    Base class for all plugins.
    Plugins should inherit from this class and implement required methods.
    """
    
    def __init__(self, name: str, version: str = "1.0.0"):
        """
        Initialize plugin.
        
        Args:
            name: Plugin name
            version: Plugin version
        """
        self.name = name
        self.version = version
        self.enabled = True
        self.hooks: Dict[PluginHook, List[Callable]] = {}
    
    @abstractmethod
    def initialize(self) -> bool:
        """
        Initialize the plugin.
        Called when plugin is loaded.
        
        Returns:
            True if initialization successful, False otherwise
        """
        pass
    
    @abstractmethod
    def shutdown(self) -> bool:
        """
        Shutdown the plugin.
        Called when plugin is unloaded.
        
        Returns:
            True if shutdown successful, False otherwise
        """
        pass
    
    def register_hook(self, hook: PluginHook, callback: Callable) -> None:
        """
        Register a hook callback.
        
        Args:
            hook: Hook to register
            callback: Callback function
        """
        if hook not in self.hooks:
            self.hooks[hook] = []
        self.hooks[hook].append(callback)
    
    def get_hook_callbacks(self, hook: PluginHook) -> List[Callable]:
        """
        Get all callbacks for a hook.
        
        Args:
            hook: Hook to get callbacks for
            
        Returns:
            List of callback functions
        """
        return self.hooks.get(hook, [])
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.name} v{self.version}>"


class PluginManager:
    """
    Manages plugin loading, lifecycle, and hook execution
    """
    
    def __init__(self):
        """Initialize plugin manager"""
        self.plugins: Dict[str, BasePlugin] = {}
        self.hooks: Dict[PluginHook, List[Callable]] = {}
    
    def load_plugin(self, plugin_path: Path) -> Optional[BasePlugin]:
        """
        Load a plugin from a Python file.
        
        Args:
            plugin_path: Path to plugin file
            
        Returns:
            Loaded plugin instance or None if failed
        """
        plugin_path = Path(plugin_path)
        
        if not plugin_path.exists():
            print(f"Plugin file not found: {plugin_path}")
            return None
        
        try:
            # Load module from file
            spec = importlib.util.spec_from_file_location(
                plugin_path.stem,
                plugin_path
            )
            if spec is None or spec.loader is None:
                print(f"Failed to load plugin spec: {plugin_path}")
                return None
            
            module = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = module
            spec.loader.exec_module(module)
            
            # Find BasePlugin subclass
            plugin_class = None
            for name, obj in inspect.getmembers(module):
                if (inspect.isclass(obj) and 
                    issubclass(obj, BasePlugin) and 
                    obj is not BasePlugin):
                    plugin_class = obj
                    break
            
            if plugin_class is None:
                print(f"No BasePlugin subclass found in {plugin_path}")
                return None
            
            # Instantiate plugin
            plugin = plugin_class()
            
            # Initialize plugin
            if not plugin.initialize():
                print(f"Failed to initialize plugin: {plugin.name}")
                return None
            
            # Register plugin
            self.plugins[plugin.name] = plugin
            print(f"Loaded plugin: {plugin}")
            
            return plugin
            
        except Exception as e:
            print(f"Error loading plugin {plugin_path}: {e}")
            return None
    
    def unload_plugin(self, plugin_name: str) -> bool:
        """
        Unload a plugin.
        
        Args:
            plugin_name: Name of plugin to unload
            
        Returns:
            True if successful, False otherwise
        """
        if plugin_name not in self.plugins:
            print(f"Plugin not found: {plugin_name}")
            return False
        
        plugin = self.plugins[plugin_name]
        
        try:
            if not plugin.shutdown():
                print(f"Plugin shutdown failed: {plugin_name}")
                return False
            
            del self.plugins[plugin_name]
            print(f"Unloaded plugin: {plugin_name}")
            return True
            
        except Exception as e:
            print(f"Error unloading plugin {plugin_name}: {e}")
            return False
    
    def register_hook(self, hook: PluginHook, callback: Callable) -> None:
        """
        Register a global hook callback.
        
        Args:
            hook: Hook to register
            callback: Callback function
        """
        if hook not in self.hooks:
            self.hooks[hook] = []
        self.hooks[hook].append(callback)
    
    def trigger_hook(self, hook: PluginHook, *args, **kwargs) -> List[Any]:
        """
        Trigger a hook and execute all registered callbacks.
        
        Args:
            hook: Hook to trigger
            *args: Positional arguments to pass to callbacks
            **kwargs: Keyword arguments to pass to callbacks
            
        Returns:
            List of return values from callbacks
        """
        results = []
        
        # Execute global hooks
        for callback in self.hooks.get(hook, []):
            try:
                result = callback(*args, **kwargs)
                results.append(result)
            except Exception as e:
                print(f"Error executing hook callback: {e}")
        
        # Execute plugin hooks
        for plugin in self.plugins.values():
            if not plugin.enabled:
                continue
            
            for callback in plugin.get_hook_callbacks(hook):
                try:
                    result = callback(*args, **kwargs)
                    results.append(result)
                except Exception as e:
                    print(f"Error executing plugin hook {plugin.name}: {e}")
        
        return results
    
    def get_plugin(self, plugin_name: str) -> Optional[BasePlugin]:
        """
        Get a plugin by name.
        
        Args:
            plugin_name: Name of plugin
            
        Returns:
            Plugin instance or None if not found
        """
        return self.plugins.get(plugin_name)
    
    def list_plugins(self) -> List[BasePlugin]:
        """
        Get list of all loaded plugins.
        
        Returns:
            List of plugin instances
        """
        return list(self.plugins.values())
    
    def enable_plugin(self, plugin_name: str) -> bool:
        """Enable a plugin"""
        plugin = self.get_plugin(plugin_name)
        if plugin:
            plugin.enabled = True
            return True
        return False
    
    def disable_plugin(self, plugin_name: str) -> bool:
        """Disable a plugin"""
        plugin = self.get_plugin(plugin_name)
        if plugin:
            plugin.enabled = False
            return True
        return False
