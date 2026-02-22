from typing import List, Dict, Any
import json
import redis.asyncio as redis
from .config import REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_CACHE_TTL

# Redis client
redis_client = None

async def get_redis():
    """Get Redis client instance"""
    global redis_client
    if redis_client is None:
        redis_client = await redis.from_url(
            f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}",
            decode_responses=True
        )
    return redis_client

# In-memory database (fallback)
phrases_db: List[Dict[str, Any]] = []

async def add_phrase(phrase_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Add a phrase to the database and cache"""
    # Add to memory
    phrase_dict["id"] = len(phrases_db) + 1
    phrases_db.append(phrase_dict)
    
    # Cache in Redis
    try:
        redis = await get_redis()
        # Cache individual phrase
        await redis.setex(
            f"phrase:{phrase_dict['id']}",
            REDIS_CACHE_TTL,
            json.dumps(phrase_dict, default=str)
        )
        # Invalidate phrases list cache
        await redis.delete("phrases:all")
    except Exception as e:
        print(f"Redis caching error: {e}")
    
    return phrase_dict

async def get_all_phrases() -> List[Dict[str, Any]]:
    """Get all phrases from cache or database"""
    try:
        redis = await get_redis()
        # Try to get from cache
        cached = await redis.get("phrases:all")
        if cached:
            return json.loads(cached)
    except Exception as e:
        print(f"Redis read error: {e}")
    
    # Fallback to memory
    return phrases_db

async def get_phrase_count() -> int:
    """Get the total number of phrases"""
    return len(phrases_db)

def clear_database():
    """Clear all phrases (for testing)"""
    global phrases_db
    phrases_db = []