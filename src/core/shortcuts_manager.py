"""
Keyboard Shortcuts Manager for PyAI IDE
Manages keyboard shortcuts and their customization
"""

from typing import Callable, Dict, Optional, List
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt
from utils.logger import logger


class ShortcutsManager:
    """Manages keyboard shortcuts for the IDE"""
    
    def __init__(self, app_data_manager):
        """Initialize shortcuts manager
        
        Args:
            app_data_manager: AppDataManager instance for persistence
        """
        self.app_data_manager = app_data_manager
        self.shortcuts = app_data_manager.shortcuts.copy()
        self.actions: Dict[str, List[Callable]] = {}
        self._conflict_cache = {}
    
    def register_action(self, action_id: str, callback: Callable):
        """Register action for shortcut
        
        Args:
            action_id: Unique action identifier
            callback: Function to call when shortcut is triggered
        """
        if action_id not in self.actions:
            self.actions[action_id] = []
        self.actions[action_id].append(callback)
        logger.info(f"Registered action: {action_id}")
    
    def trigger_action(self, action_id: str):
        """Trigger action by ID
        
        Args:
            action_id: Action identifier
        """
        if action_id in self.actions:
            for callback in self.actions[action_id]:
                try:
                    callback()
                except Exception as e:
                    logger.error(f"Error triggering action {action_id}: {e}")
        else:
            logger.warning(f"Action not found: {action_id}")
    
    def get_shortcut(self, action_id: str) -> Optional[str]:
        """Get shortcut for action
        
        Args:
            action_id: Action identifier
            
        Returns:
            Shortcut string or None
        """
        return self.shortcuts.get(action_id)
    
    def set_shortcut(self, action_id: str, shortcut: str) -> bool:
        """Set shortcut for action
        
        Args:
            action_id: Action identifier
            shortcut: Shortcut string (e.g., "Ctrl+S")
            
        Returns:
            True if successful, False if conflict
        """
        # Check for conflicts
        if self._has_conflict(shortcut, action_id):
            logger.warning(f"Shortcut conflict: {shortcut}")
            return False
        
        # Validate shortcut
        if not self._is_valid_shortcut(shortcut):
            logger.warning(f"Invalid shortcut: {shortcut}")
            return False
        
        self.shortcuts[action_id] = shortcut
        self.app_data_manager.set_shortcut(action_id, shortcut)
        self._conflict_cache.clear()
        logger.info(f"Shortcut set: {action_id} -> {shortcut}")
        return True
    
    def get_all_shortcuts(self) -> Dict[str, str]:
        """Get all shortcuts
        
        Returns:
            Dictionary of action_id -> shortcut
        """
        return self.shortcuts.copy()
    
    def reset_shortcuts(self):
        """Reset shortcuts to defaults"""
        self.shortcuts = self.app_data_manager._get_default_shortcuts()
        for action_id, shortcut in self.shortcuts.items():
            self.app_data_manager.set_shortcut(action_id, shortcut)
        self._conflict_cache.clear()
        logger.info("Shortcuts reset to defaults")
    
    def _has_conflict(self, shortcut: str, exclude_action: str = None) -> bool:
        """Check if shortcut conflicts with existing shortcuts
        
        Args:
            shortcut: Shortcut to check
            exclude_action: Action ID to exclude from check
            
        Returns:
            True if conflict exists
        """
        cache_key = f"{shortcut}:{exclude_action}"
        if cache_key in self._conflict_cache:
            return self._conflict_cache[cache_key]
        
        for action_id, existing_shortcut in self.shortcuts.items():
            if exclude_action and action_id == exclude_action:
                continue
            if existing_shortcut == shortcut:
                self._conflict_cache[cache_key] = True
                return True
        
        self._conflict_cache[cache_key] = False
        return False
    
    def _is_valid_shortcut(self, shortcut: str) -> bool:
        """Validate shortcut format
        
        Args:
            shortcut: Shortcut string to validate
            
        Returns:
            True if valid
        """
        try:
            # Try to parse with Qt
            seq = QKeySequence(shortcut)
            return not seq.isEmpty()
        except:
            return False
    
    def get_conflicting_actions(self, shortcut: str) -> List[str]:
        """Get actions that use the same shortcut
        
        Args:
            shortcut: Shortcut to check
            
        Returns:
            List of action IDs
        """
        conflicts = []
        for action_id, existing_shortcut in self.shortcuts.items():
            if existing_shortcut == shortcut:
                conflicts.append(action_id)
        return conflicts
    
    def export_shortcuts(self) -> Dict[str, str]:
        """Export shortcuts for backup
        
        Returns:
            Dictionary of shortcuts
        """
        return self.shortcuts.copy()
    
    def import_shortcuts(self, shortcuts: Dict[str, str]) -> bool:
        """Import shortcuts from backup
        
        Args:
            shortcuts: Dictionary of shortcuts
            
        Returns:
            True if successful
        """
        try:
            # Validate all shortcuts
            for action_id, shortcut in shortcuts.items():
                if not self._is_valid_shortcut(shortcut):
                    logger.warning(f"Invalid shortcut in import: {action_id} -> {shortcut}")
                    return False
            
            # Import
            self.shortcuts = shortcuts.copy()
            for action_id, shortcut in shortcuts.items():
                self.app_data_manager.set_shortcut(action_id, shortcut)
            
            self._conflict_cache.clear()
            logger.info("Shortcuts imported successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to import shortcuts: {e}")
            return False


class ShortcutHandler:
    """Handles keyboard events and triggers shortcuts"""
    
    def __init__(self, shortcuts_manager: ShortcutsManager):
        """Initialize shortcut handler
        
        Args:
            shortcuts_manager: ShortcutsManager instance
        """
        self.shortcuts_manager = shortcuts_manager
        self.shortcut_map: Dict[str, str] = {}
        self._build_shortcut_map()
    
    def _build_shortcut_map(self):
        """Build map of shortcut strings to action IDs"""
        self.shortcut_map = {}
        for action_id, shortcut in self.shortcuts_manager.get_all_shortcuts().items():
            self.shortcut_map[shortcut] = action_id
    
    def handle_key_event(self, event) -> bool:
        """Handle keyboard event
        
        Args:
            event: QKeyEvent
            
        Returns:
            True if event was handled
        """
        # Build shortcut string from event
        modifiers = event.modifiers()
        key = event.key()
        
        shortcut_str = self._build_shortcut_string(modifiers, key)
        
        if shortcut_str in self.shortcut_map:
            action_id = self.shortcut_map[shortcut_str]
            self.shortcuts_manager.trigger_action(action_id)
            return True
        
        return False
    
    def _build_shortcut_string(self, modifiers, key) -> str:
        """Build shortcut string from modifiers and key
        
        Args:
            modifiers: Qt modifiers
            key: Qt key code
            
        Returns:
            Shortcut string
        """
        parts = []
        
        if modifiers & Qt.ControlModifier:
            parts.append("Ctrl")
        if modifiers & Qt.ShiftModifier:
            parts.append("Shift")
        if modifiers & Qt.AltModifier:
            parts.append("Alt")
        if modifiers & Qt.MetaModifier:
            parts.append("Meta")
        
        # Get key name
        key_seq = QKeySequence(key)
        if not key_seq.isEmpty():
            key_name = key_seq.toString().split('+')[-1]
            parts.append(key_name)
        
        return '+'.join(parts)
