"""
HuggingFace integration service for PyAI IDE
Handles model loading, inference, and API interactions
"""

from typing import Any, Dict, List, Optional, Tuple
from pathlib import Path

from utils.validators import validate_token, validate_model_id
from utils.path_utils import get_models_dir


class HuggingFaceService:
    """
    Service for HuggingFace integration
    Manages model loading, caching, and inference
    """
    
    def __init__(self, token: Optional[str] = None):
        """
        Initialize HuggingFace service.
        
        Args:
            token: HuggingFace API token
        """
        self.token = token
        self.models_dir = get_models_dir()
        self.loaded_models: Dict[str, Any] = {}
        self.model_info_cache: Dict[str, Dict[str, Any]] = {}
    
    def set_token(self, token: str) -> Tuple[bool, str]:
        """
        Set HuggingFace API token.
        
        Args:
            token: API token
            
        Returns:
            Tuple of (success, message)
        """
        is_valid, error = validate_token(token, 'huggingface')
        
        if not is_valid:
            return False, error
        
        self.token = token
        return True, "Token set successfully"
    
    def get_token(self) -> Optional[str]:
        """Get current HuggingFace token"""
        return self.token
    
    def validate_model_id(self, model_id: str) -> Tuple[bool, str]:
        """
        Validate a model ID.
        
        Args:
            model_id: Model ID to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        return validate_model_id(model_id)
    
    def load_model(self, model_id: str, local: bool = True) -> Tuple[bool, str]:
        """
        Load a model.
        
        Args:
            model_id: Model ID (e.g., 'gpt2')
            local: Whether to load locally or use API
            
        Returns:
            Tuple of (success, message)
        """
        # Validate model ID
        is_valid, error = validate_model_id(model_id)
        if not is_valid:
            return False, error
        
        # Check if already loaded
        if model_id in self.loaded_models:
            return True, f"Model {model_id} already loaded"
        
        try:
            if local:
                # Try to load locally using transformers
                try:
                    from transformers import AutoModel, AutoTokenizer
                    
                    tokenizer = AutoTokenizer.from_pretrained(model_id)
                    model = AutoModel.from_pretrained(model_id)
                    
                    self.loaded_models[model_id] = {
                        'model': model,
                        'tokenizer': tokenizer,
                        'type': 'local',
                    }
                    
                    return True, f"Model {model_id} loaded successfully"
                except ImportError:
                    return False, "transformers library not installed"
                except Exception as e:
                    return False, f"Failed to load model: {str(e)}"
            else:
                # Use HuggingFace Inference API
                if not self.token:
                    return False, "HuggingFace token not set"
                
                self.loaded_models[model_id] = {
                    'model_id': model_id,
                    'type': 'api',
                }
                
                return True, f"Model {model_id} configured for API inference"
        
        except Exception as e:
            return False, f"Error loading model: {str(e)}"
    
    def unload_model(self, model_id: str) -> Tuple[bool, str]:
        """
        Unload a model.
        
        Args:
            model_id: Model ID to unload
            
        Returns:
            Tuple of (success, message)
        """
        if model_id not in self.loaded_models:
            return False, f"Model {model_id} not loaded"
        
        try:
            del self.loaded_models[model_id]
            return True, f"Model {model_id} unloaded"
        except Exception as e:
            return False, f"Error unloading model: {str(e)}"
    
    def list_loaded_models(self) -> List[str]:
        """Get list of loaded models"""
        return list(self.loaded_models.keys())
    
    def infer(self, model_id: str, input_text: str, **kwargs) -> Tuple[bool, Any]:
        """
        Run inference on a model.
        
        Args:
            model_id: Model ID
            input_text: Input text
            **kwargs: Additional arguments
            
        Returns:
            Tuple of (success, result)
        """
        if model_id not in self.loaded_models:
            return False, f"Model {model_id} not loaded"
        
        try:
            model_info = self.loaded_models[model_id]
            
            if model_info['type'] == 'local':
                # Local inference
                tokenizer = model_info['tokenizer']
                model = model_info['model']
                
                inputs = tokenizer(input_text, return_tensors='pt')
                outputs = model(**inputs)
                
                return True, outputs
            
            elif model_info['type'] == 'api':
                # API inference
                if not self.token:
                    return False, "HuggingFace token not set"
                
                try:
                    from huggingface_hub import InferenceClient
                    
                    client = InferenceClient(api_key=self.token)
                    result = client.text_generation(input_text, model=model_id)
                    
                    return True, result
                except ImportError:
                    return False, "huggingface_hub library not installed"
                except Exception as e:
                    return False, f"API inference failed: {str(e)}"
        
        except Exception as e:
            return False, f"Inference error: {str(e)}"
    
    def get_model_info(self, model_id: str) -> Dict[str, Any]:
        """
        Get information about a model.
        
        Args:
            model_id: Model ID
            
        Returns:
            Dictionary with model information
        """
        if model_id in self.model_info_cache:
            return self.model_info_cache[model_id]
        
        try:
            from huggingface_hub import model_info
            
            info = model_info(model_id)
            
            model_data = {
                'id': model_id,
                'downloads': getattr(info, 'downloads', 0),
                'likes': getattr(info, 'likes', 0),
                'tags': getattr(info, 'tags', []),
                'pipeline_tag': getattr(info, 'pipeline_tag', None),
            }
            
            self.model_info_cache[model_id] = model_data
            return model_data
        
        except Exception as e:
            return {'error': str(e)}
    
    def search_models(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search for models on HuggingFace Hub.
        
        Args:
            query: Search query
            limit: Maximum number of results
            
        Returns:
            List of model information dictionaries
        """
        try:
            from huggingface_hub import list_models
            
            models = list_models(search=query, limit=limit)
            
            results = []
            for model in models:
                results.append({
                    'id': model.id,
                    'downloads': model.downloads,
                    'likes': model.likes,
                    'tags': model.tags,
                })
            
            return results
        
        except Exception as e:
            print(f"Error searching models: {e}")
            return []
