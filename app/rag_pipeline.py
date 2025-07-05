# backend/app/rag_pipeline.py

from app.embedder import embed_texts
from app.chunker import process_document
from app.mongo_vectorstore import get_similar_vectors, store_vectors
from app.llm_interface import call_llm
from typing import List, Dict, Any


async def ingest_documents(file_paths: List[str]):
    """
    Ingests documents into the vector store:
    - Chunks each document
    - Embeds chunks
    - Stores in MongoDB
    """
    all_chunks = []

    for file_path in file_paths:
        chunks = process_document(file_path)
        if chunks:
            all_chunks.extend(chunks)
        else:
            print(f"⚠️ No chunks generated from: {file_path}")

    if not all_chunks:
        print("❌ No chunks to ingest. Aborting.")
        return

    # Embed chunks
    try:
        embeddings = embed_texts(all_chunks)
    except Exception as e:
        print(f"❌ Error generating embeddings: {e}")
        return

    # Convert to plain list (for MongoDB compatibility)
    cleaned_embeddings = []
    for emb in embeddings:
        if hasattr(emb, "tolist"):
            cleaned_embeddings.append(emb.tolist())
        else:
            cleaned_embeddings.append(emb)

    if len(all_chunks) != len(cleaned_embeddings):
        print("❌ Chunk-embedding count mismatch. Aborting ingestion.")
        return

    store_vectors(all_chunks, cleaned_embeddings)
    print("✅ Document ingestion complete.")


async def handle_query(user_input: str) -> Dict[str, Any]:
    if not user_input.strip():
        return {"answer": "❌ Please provide a valid question.", "source_documents": []}

    try:
        # Embed query
        query_embedding = embed_texts([user_input])[0]
        if hasattr(query_embedding, "tolist"):
            query_embedding = query_embedding.tolist()

        # ✅ FIXED: Removed 'await'
        similar_docs = get_similar_vectors(query_embedding, top_k=3)

        if similar_docs:
            context = " ".join([doc["text"] for doc in similar_docs])
            source_documents = [
                {
                    "content": doc["text"],
                    "score": round(doc.get("score", 0), 4)
                } for doc in similar_docs
            ]
        else:
            context = "No relevant context found in documents."
            source_documents = []
            print("⚠️ No similar documents retrieved.")

        # Generate answer
        llm_response = await call_llm(user_input, context)

        return {
            "answer": llm_response.get("answer", "⚠️ Could not generate a response."),
            "source_documents": source_documents
        }

    except Exception as e:
        print(f"❌ Error handling query: {e}")
        return {
            "answer": "❌ Internal server error while processing the query.",
            "source_documents": []
        }
