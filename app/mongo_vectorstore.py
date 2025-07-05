# backend/app/mongo_vectorstore.py

import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise ValueError("❌ MONGO_URI not found in .env file")

# Connect to MongoDB Atlas
client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
db = client["rag_db"]  # Use your database name
collection = db["documents"]  # Use your collection name

def store_vectors(chunks: List[str], embeddings: List[List[float]]) -> None:
    """
    Stores chunks and embeddings in MongoDB for vector search.
    """
    if not chunks or not embeddings:
        print("⚠️ Empty chunks or embeddings provided to store_vectors.")
        return

    documents_to_insert = [
        {"text": chunk, "embedding": embedding}
        for chunk, embedding in zip(chunks, embeddings)
    ]

    try:
        result = collection.insert_many(documents_to_insert)
        print(f"✅ Successfully inserted {len(result.inserted_ids)} documents into MongoDB.")
    except Exception as e:
        print(f"❌ Error inserting into MongoDB: {e}")

def get_similar_vectors(query_embedding: List[float], top_k: int = 3) -> List[Dict[str, Any]]:
    """
    Performs vector similarity search using MongoDB Atlas Vector Search.
    Requires an index named 'vector_index' on 'embedding'.
    """
    try:
        pipeline = [
            {
                "$vectorSearch": {
                    "index": "vector_index",  # Must match the index created in Atlas
                    "queryVector": query_embedding,
                    "path": "embedding",
                    "numCandidates": top_k * 10,
                    "limit": top_k
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "text": 1,
                    "score": { "$meta": "vectorSearchScore" }
                }
            }
        ]

        results = list(collection.aggregate(pipeline))
        print(f"🔍 Found {len(results)} similar documents from vector search.")
        return results

    except Exception as e:
        print(f"❌ Error during vector similarity search: {e}")
        return []
