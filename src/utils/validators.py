"""
Input validators for PyAI IDE
Validates tokens, model IDs, and other user inputs
"""

import re
from typing import Tuple


def validate_token(token: str, token_type: str = 'github') -> Tuple[bool, str]:
    """
    Validate API token format.
    
    Args:
        token: Token string to validate
        token_type: Type of token ('github', 'huggingface')
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not token or not isinstance(token, str):
        return False, "Token cannot be empty"
    
    token = token.strip()
    
    if len(token) < 10:
        return False, "Token is too short"
    
    if token_type == 'github':
        # GitHub tokens typically start with 'ghp_' or 'ghu_'
        if not (token.startswith('ghp_') or token.startswith('ghu_') or 
                token.startswith('ghs_') or token.startswith('ghr_')):
            return False, "Invalid GitHub token format"
    
    elif token_type == 'huggingface':
        # HuggingFace tokens typically start with 'hf_'
        if not token.startswith('hf_'):
            return False, "Invalid HuggingFace token format"
    
    return True, ""


def validate_model_id(model_id: str) -> Tuple[bool, str]:
    """
    Validate HuggingFace model ID format.
    
    Args:
        model_id: Model ID to validate (e.g., 'username/model-name')
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not model_id or not isinstance(model_id, str):
        return False, "Model ID cannot be empty"
    
    model_id = model_id.strip()
    
    # Model ID should be in format: username/model-name
    if '/' not in model_id:
        return False, "Model ID should be in format: username/model-name"
    
    parts = model_id.split('/')
    if len(parts) != 2:
        return False, "Model ID should contain exactly one '/'"
    
    username, model_name = parts
    
    if not username or not model_name:
        return False, "Username and model name cannot be empty"
    
    # Validate characters
    if not re.match(r'^[a-zA-Z0-9_-]+$', username):
        return False, "Invalid characters in username"
    
    if not re.match(r'^[a-zA-Z0-9_.-]+$', model_name):
        return False, "Invalid characters in model name"
    
    return True, ""


def validate_project_name(name: str) -> Tuple[bool, str]:
    """
    Validate project name.
    
    Args:
        name: Project name to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not name or not isinstance(name, str):
        return False, "Project name cannot be empty"
    
    name = name.strip()
    
    if len(name) < 1:
        return False, "Project name is too short"
    
    if len(name) > 255:
        return False, "Project name is too long"
    
    # Allow alphanumeric, spaces, hyphens, underscores
    if not re.match(r'^[a-zA-Z0-9\s_-]+$', name):
        return False, "Project name contains invalid characters"
    
    return True, ""


def validate_github_url(url: str) -> Tuple[bool, str]:
    """
    Validate GitHub repository URL.
    
    Args:
        url: GitHub URL to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not url or not isinstance(url, str):
        return False, "URL cannot be empty"
    
    url = url.strip()
    
    # Check if it's a valid GitHub URL
    github_pattern = r'^https://github\.com/[a-zA-Z0-9_-]+/[a-zA-Z0-9_.-]+(?:\.git)?$'
    
    if not re.match(github_pattern, url):
        return False, "Invalid GitHub repository URL"
    
    return True, ""
