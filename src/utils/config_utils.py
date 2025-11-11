"""
Configuration utilities for PyAI IDE
Handles JSON configuration file operations
"""

import json
from pathlib import Path
from typing import Any, Dict, Optional


def load_json(file_path: Path) -> Dict[str, Any]:
    """
    Load JSON configuration from file.
    
    Args:
        file_path: Path to JSON file
        
    Returns:
        Dictionary containing JSON data, or empty dict if file doesn't exist
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        return {}
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading JSON from {file_path}: {e}")
        return {}


def save_json(file_path: Path, data: Dict[str, Any]) -> bool:
    """
    Save JSON configuration to file.
    
    Args:
        file_path: Path to JSON file
        data: Dictionary to save
        
    Returns:
        True if successful, False otherwise
    """
    file_path = Path(file_path)
    
    try:
        # Ensure parent directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except IOError as e:
        print(f"Error saving JSON to {file_path}: {e}")
        return False


def get_nested(data: Dict, path: str, default: Any = None) -> Any:
    """
    Get nested value from dictionary using dot notation.
    
    Args:
        data: Dictionary to search
        path: Dot-separated path (e.g., 'github.token')
        default: Default value if path not found
        
    Returns:
        Value at path or default
    """
    keys = path.split('.')
    current = data
    
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    
    return current


def set_nested(data: Dict, path: str, value: Any) -> Dict:
    """
    Set nested value in dictionary using dot notation.
    
    Args:
        data: Dictionary to modify
        path: Dot-separated path (e.g., 'github.token')
        value: Value to set
        
    Returns:
        Modified dictionary
    """
    keys = path.split('.')
    current = data
    
    # Navigate to parent of target key
    for key in keys[:-1]:
        if key not in current:
            current[key] = {}
        current = current[key]
    
    # Set the value
    current[keys[-1]] = value
    return data
