import os
import sys
import subprocess

def fix_numpy_issue():
    """Fix NumPy version issue"""
    try:
        import numpy
        print(f"✅ NumPy version: {numpy.__version__}")
    except Exception as e:
        print(f"⚠️ NumPy issue: {e}")
        print("Installing compatible NumPy version...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy==1.24.3"])

def download_model():
    """Download the sentence transformer model"""
    model_name = "all-MiniLM-L6-v2"
    model_path = os.path.join("models", model_name)
    
    # Check if model already exists
    if os.path.exists(model_path) and os.path.exists(os.path.join(model_path, "model.safetensors")):
        print(f"✅ Model already exists at {model_path}")
        return True
    
    print(f"📥 Downloading model {model_name}...")
    try:
        from sentence_transformers import SentenceTransformer
        
        # Download and save model
        model = SentenceTransformer(model_name)
        model.save(model_path)
        print(f"✅ Model downloaded and saved to {model_path}")
        return True
    except Exception as e:
        print(f"❌ Error downloading model: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Fixing NumPy issue...")
    fix_numpy_issue()
    
    print("\n📦 Downloading model...")
    success = download_model()
    
    if success:
        print("\n✅ Setup complete!")
        sys.exit(0)
    else:
        print("\n❌ Setup failed!")
        sys.exit(1)