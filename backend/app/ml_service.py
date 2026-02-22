import os
import json
import hashlib
from sentence_transformers import SentenceTransformer
from typing import List, Union
from .config import settings
from .database import get_redis

class ModelService:
    def __init__(self):
        self.model_folders = []
        self.models_list = []
        self.load_models()
    
    def load_models(self):
        """Load all available models from the models directory"""
        if os.path.exists(settings.models_dir):
            self.model_folders = [f for f in os.listdir(settings.models_dir) 
                                 if os.path.isdir(os.path.join(settings.models_dir, f))]
            self.models_list = [SentenceTransformer(os.path.join(settings.models_dir, f)) 
                              for f in self.model_folders]
            
            print("Models available:")
            for i, f in enumerate(self.model_folders, start=1):
                print(f"{i}: {f}")
        else:
            print(f"Models directory not found: {settings.models_dir}")
    
    def get_available_models(self) -> dict:
        """Return dictionary of available models"""
        return {i + 1: name for i, name in enumerate(self.model_folders)}
    
    def _generate_cache_key(self, text: Union[str, List[str]], model_number: int) -> str:
        """Generate cache key for text and model"""
        text_str = text if isinstance(text, str) else json.dumps(text, sort_keys=True)
        hash_input = f"{text_str}:{model_number}".encode('utf-8')
        return f"embedding:{hashlib.md5(hash_input).hexdigest()}"
    
    async def encode_text(self, text: Union[str, List[str]], model_number: int) -> List[float]:
        """
        Encode text using specified model with Redis cache
        """
        if model_number < 1 or model_number > len(self.models_list):
            raise ValueError(f"Choose model between 1 and {len(self.models_list)}")
        
        # Try to get from cache
        cache_key = self._generate_cache_key(text, model_number)
        try:
            redis = await get_redis()
            cached = await redis.get(cache_key)
            if cached:
                print(f"✅ Cache hit for key: {cache_key}")
                return json.loads(cached)
        except Exception as e:
            print(f"⚠️ Redis cache read error: {e}")
        
        # Generate embedding
        print(f"🔄 Cache miss, generating embedding for key: {cache_key}")
        model = self.models_list[model_number - 1]
        vector = model.encode(text).tolist()
        
        # Store in cache
        try:
            redis = await get_redis()
            await redis.setex(
                cache_key,
                3600,  # 1 hour TTL
                json.dumps(vector)
            )
            print(f"✅ Cached embedding for key: {cache_key}")
        except Exception as e:
            print(f"⚠️ Redis cache write error: {e}")
        
        return vector
    
    def get_model_name(self, model_number: int) -> str:
        """Get model name by number"""
        if model_number < 1 or model_number > len(self.model_folders):
            raise ValueError(f"Choose model between 1 and {len(self.model_folders)}")
        return self.model_folders[model_number - 1]

# Create global instance
model_service = ModelService()