import os

# Model directory
MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")

# API settings
API_TITLE = "Sentence Embedding API"
API_VERSION = "1.0.0"

# Redis settings
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))
REDIS_CACHE_TTL = 3600  # 1 hour cache TTL

# Database settings (using in-memory for now)
class Settings:
    def __init__(self):
        self.models_dir = MODELS_DIR

settings = Settings()