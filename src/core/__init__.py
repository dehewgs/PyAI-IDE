"""
Core modules for PyAI IDE
"""

from .plugin_system import BasePlugin, PluginManager, PluginHook
from .config_manager import ConfigManager
from .event_system import EventSystem, EventListener

__all__ = [
    'BasePlugin',
    'PluginManager',
    'PluginHook',
    'ConfigManager',
    'EventSystem',
    'EventListener',
]
