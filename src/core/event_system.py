"""
Event system for PyAI IDE
Provides pub/sub event handling for application-wide communication
"""

from typing import Any, Callable, Dict, List, Optional


class EventListener:
    """Represents an event listener"""
    
    def __init__(self, event_type: str, callback: Callable, priority: int = 0):
        """
        Initialize event listener.
        
        Args:
            event_type: Type of event to listen for
            callback: Callback function
            priority: Priority level (higher = called first)
        """
        self.event_type = event_type
        self.callback = callback
        self.priority = priority
    
    def __lt__(self, other):
        """Compare listeners by priority (for sorting)"""
        return self.priority > other.priority  # Higher priority first


class EventSystem:
    """
    Central event system for application-wide event handling
    """
    
    def __init__(self):
        """Initialize event system"""
        self.listeners: Dict[str, List[EventListener]] = {}
        self.event_history: List[Dict[str, Any]] = []
        self.max_history = 1000
    
    def subscribe(self, event_type: str, callback: Callable, priority: int = 0) -> EventListener:
        """
        Subscribe to an event.
        
        Args:
            event_type: Type of event to subscribe to
            callback: Callback function to call when event is emitted
            priority: Priority level (higher = called first)
            
        Returns:
            EventListener instance
        """
        listener = EventListener(event_type, callback, priority)
        
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        
        self.listeners[event_type].append(listener)
        self.listeners[event_type].sort()
        
        return listener
    
    def unsubscribe(self, listener: EventListener) -> bool:
        """
        Unsubscribe from an event.
        
        Args:
            listener: EventListener instance to remove
            
        Returns:
            True if successful, False if listener not found
        """
        event_type = listener.event_type
        
        if event_type not in self.listeners:
            return False
        
        try:
            self.listeners[event_type].remove(listener)
            return True
        except ValueError:
            return False
    
    def emit(self, event_type: str, *args, **kwargs) -> List[Any]:
        """
        Emit an event and call all registered listeners.
        
        Args:
            event_type: Type of event to emit
            *args: Positional arguments to pass to listeners
            **kwargs: Keyword arguments to pass to listeners
            
        Returns:
            List of return values from listeners
        """
        results = []
        
        # Record event in history
        self._record_event(event_type, args, kwargs)
        
        # Call all listeners for this event type
        if event_type in self.listeners:
            for listener in self.listeners[event_type]:
                try:
                    result = listener.callback(*args, **kwargs)
                    results.append(result)
                except Exception as e:
                    print(f"Error in event listener for {event_type}: {e}")
        
        return results
    
    def _record_event(self, event_type: str, args: tuple, kwargs: dict) -> None:
        """
        Record event in history for debugging.
        
        Args:
            event_type: Type of event
            args: Event arguments
            kwargs: Event keyword arguments
        """
        event_record = {
            'type': event_type,
            'args': args,
            'kwargs': kwargs,
        }
        
        self.event_history.append(event_record)
        
        # Trim history if it gets too large
        if len(self.event_history) > self.max_history:
            self.event_history = self.event_history[-self.max_history:]
    
    def get_event_history(self, event_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get event history.
        
        Args:
            event_type: Optional filter by event type
            
        Returns:
            List of event records
        """
        if event_type is None:
            return self.event_history.copy()
        
        return [e for e in self.event_history if e['type'] == event_type]
    
    def clear_history(self) -> None:
        """Clear event history"""
        self.event_history.clear()
    
    def get_listener_count(self, event_type: Optional[str] = None) -> int:
        """
        Get number of listeners.
        
        Args:
            event_type: Optional filter by event type
            
        Returns:
            Number of listeners
        """
        if event_type is None:
            return sum(len(listeners) for listeners in self.listeners.values())
        
        return len(self.listeners.get(event_type, []))
    
    def clear_listeners(self, event_type: Optional[str] = None) -> None:
        """
        Clear listeners.
        
        Args:
            event_type: Optional filter by event type
        """
        if event_type is None:
            self.listeners.clear()
        else:
            self.listeners.pop(event_type, None)
