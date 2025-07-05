# backend/app/embedder.py

from sentence_transformers import SentenceTransformer
from typing import List, Union
import numpy as np

_model = None  # Global cache for model

def get_embedding_model() -> SentenceTransformer:
    """
    Loads and returns the SentenceTransformer model.
    Uses singleton pattern to avoid reloading.
    """
    global _model
    if _model is None:
        try:
            # Lightweight and fast model; change to `all-mpnet-base-v2` for higher quality
            _model = SentenceTransformer("all-MiniLM-L6-v2")
            print("✅ Loaded embedding model: all-MiniLM-L6-v2")
        except Exception as e:
            print(f"❌ Failed to load embedding model: {e}")
            raise
    return _model


def embed_texts(texts: List[str]) -> List[Union[List[float], np.ndarray]]:
    """
    Embeds a list of texts and returns vector embeddings.
    Ensures safe return format for MongoDB (list of floats).
    """
    model = get_embedding_model()
    
    try:
        embeddings = model.encode(texts, convert_to_numpy=True)  # Always as ndarray
    except Exception as e:
        print(f"❌ Error during embedding: {e}")
        raise

    return embeddings.tolist()  # Convert ndarray to List[List[float]] for storage
