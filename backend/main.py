from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models import PhraseCreate
from app.database import add_phrase, get_all_phrases, get_phrase_count
from app.ml_service import model_service
import uvicorn
import warnings

# Suppress the specific warning
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")

app = FastAPI(title="Sentence Embedding API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "Welcome to Sentence Embedding API",
        "endpoints": {
            "POST /postageee/": "Create a new sentence and generate embedding",
            "GET /gettage/": "Get all phrases",
            "GET /models/": "List available models"
        }
    }

@app.post("/postageee/")
async def create_sentence(phrase: PhraseCreate):
    """
    Create a new sentence and generate embedding
    """
    try:
        # Get model name
        model_name = model_service.get_model_name(phrase.modelnumber)
        
        # Generate embedding (async method)
        vector = await model_service.encode_text(phrase.phrase, phrase.modelnumber)
        
        # Prepare phrase dictionary
        phrase_dict = {
            "phrase": phrase.phrase,
            "modelnumber": phrase.modelnumber,
            "embedding": vector,
            "embedding_dim": len(vector) if isinstance(vector, list) else len(vector[0]),
            "model_used": model_name
        }
        
        # Add to database (async method)
        saved_phrase = await add_phrase(phrase_dict)
        
        # Get phrase count (async method)
        count = await get_phrase_count()
        
        return {
            "message": "Phrase created successfully",
            "phrase": {
                "id": saved_phrase["id"],
                "text": saved_phrase["phrase"],
                "model_used": model_name,
                "embedding_dim": saved_phrase["embedding_dim"]
            },
            "phrase_count": count
        }
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@app.get("/gettage/")
async def get_phrases():
    """Get all phrases"""
    phrases = await get_all_phrases()
    return {"phrases": phrases, "count": len(phrases)}

@app.get("/models/")
async def get_models():
    """List available models"""
    return model_service.get_available_models()

@app.get("/redis-test")
async def test_redis():
    """Test Redis connection"""
    try:
        from app.database import get_redis
        redis = await get_redis()
        await redis.set("test_key", "Hello from Redis!")
        value = await redis.get("test_key")
        return {
            "status": "connected",
            "message": f"Redis says: {value}",
            "config": {
                "host": "host.docker.internal" if "HOST" in str(redis) else "localhost",
                "port": 6379,
                "db": 0
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

if __name__ == "__main__":
    print("=" * 50)
    print("Starting Sentence Embedding API Server")
    print("=" * 50)
    print(f"Models available: {len(model_service.models_list)}")
    for i, model_name in enumerate(model_service.model_folders, 1):
        print(f"  {i}: {model_name}")
    print("=" * 50)
    print("Redis caching enabled")
    print("=" * 50)
    print("Server will be available at:")
    print("  → Local: http://localhost:8000")
    print("  → Docs:  http://localhost:8000/docs")
    print("  → Redoc: http://localhost:8000/redoc")
    print("=" * 50)
    print("Press Ctrl+C to stop the server")
    print("=" * 50)
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )