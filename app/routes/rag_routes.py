from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import List
import os
import shutil

from app.rag_pipeline import handle_query, ingest_documents

router = APIRouter()

#UPLOAD_DIR defines the path to a folder (uploaded_docs) one level above this file.
#Creates the folder if it doesn't already exist.
# Directory to temporarily store uploaded files
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "uploaded_docs")
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload-docs")
async def upload_documents(files: List[UploadFile] = File(...)):
    """
        Accepts one or more files (List[UploadFile]) from the client using a multipart/form-data POST request.
        Files are saved temporarily, then processed via ingest_documents.
    Upload one or more documents (PDF/TXT/DOCX) and ingest them into the RAG system.
    """
    file_paths: List[str] = []

    try:
        for file in files:
            file_path = os.path.join(UPLOAD_DIR, file.filename)
            try:
                with open(file_path, "wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)
                file_paths.append(file_path)
                #opening files as file streams and uploading files
            finally:
                # file stream closed
                file.file.close()

        if not file_paths:
            raise HTTPException(status_code=400, detail="No valid files to process.")

        await ingest_documents(file_paths)

        return {"message": f"✅ Successfully ingested {len(file_paths)} documents."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"🚫 Upload/Ingestion failed: {str(e)}")

    finally:
        # Cleanup: remove uploaded temp files
        for path in file_paths:
            try:
                if os.path.exists(path):
                    os.remove(path)
            except Exception as cleanup_err:
                print(f"⚠️ Cleanup failed for {path}: {cleanup_err}")


@router.post("/query")
async def query_documents(user_input: str = Form(...)):
    """
    Accepts a user query and returns an AI-generated answer with context.
    """
    if not user_input.strip():
        raise HTTPException(status_code=400, detail="🚫 Query cannot be empty.")
    
    try:
        response = await handle_query(user_input)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"⚠️ Query handling failed: {str(e)}")

#wb
# w - write mode
# b - binary