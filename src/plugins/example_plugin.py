"""
Example Plugin for PyAI IDE
This is a sample plugin demonstrating the plugin system
"""

from core.plugin_system import BasePlugin, PluginHook


class ExamplePlugin(BasePlugin):
    """
    Example plugin that demonstrates basic plugin functionality
    """
    
    def __init__(self):
        """Initialize the example plugin"""
        super().__init__("Example Plugin", "1.0.0")
        self.startup_count = 0
    
    def initialize(self) -> bool:
        """
        Initialize the plugin.
        Called when the plugin is loaded.
        
        Returns:
            True if initialization successful
        """
        print(f"[{self.name}] Initializing...")
        
        # Register hooks
        self.register_hook(PluginHook.ON_STARTUP, self.on_startup)
        self.register_hook(PluginHook.ON_SHUTDOWN, self.on_shutdown)
        self.register_hook(PluginHook.ON_FILE_SAVE, self.on_file_save)
        
        print(f"[{self.name}] Initialized successfully")
        return True
    
    def shutdown(self) -> bool:
        """
        Shutdown the plugin.
        Called when the plugin is unloaded.
        
        Returns:
            True if shutdown successful
        """
        print(f"[{self.name}] Shutting down...")
        print(f"[{self.name}] Application was started {self.startup_count} times")
        return True
    
    def on_startup(self):
        """Called when the application starts"""
        self.startup_count += 1
        print(f"[{self.name}] Application started (count: {self.startup_count})")
    
    def on_shutdown(self):
        """Called when the application shuts down"""
        print(f"[{self.name}] Application shutting down")
    
    def on_file_save(self, filename: str):
        """
        Called when a file is saved
        
        Args:
            filename: Name of the file being saved
        """
        print(f"[{self.name}] File saved: {filename}")
    
    def get_info(self) -> dict:
        """
        Get plugin information
        
        Returns:
            Dictionary with plugin metadata
        """
        return {
            'name': self.name,
            'version': self.version,
            'description': 'Example plugin demonstrating plugin system',
            'author': 'PyAI IDE Team',
            'enabled': self.enabled,
        }


# This is required for the plugin system to find the plugin class
__plugin_class__ = ExamplePlugin
