"""
Services for PyAI IDE
Provides integration with external services like GitHub and HuggingFace
"""

from .github_service import GitHubService
from .huggingface_service import HuggingFaceService

__all__ = [
    'GitHubService',
    'HuggingFaceService',
]
