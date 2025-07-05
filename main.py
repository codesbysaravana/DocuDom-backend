# backend/main.py

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.routes import rag_routes

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="DocuSage AI",
    description="RAG-powered document Q&A backend using MongoDB Vector Search and LLMs.",
    version="1.0.0"
)

# Configure CORS (allow frontend access from Streamlit or other domains)
origins = [
    "http://localhost:8501",  # Local Streamlit
    "http://127.0.0.1:8501",
    "http://localhost:3000",
    "http://docusage-frontend-bucket.s3-website.ap-south-1.amazonaws.com/"
    # Add more origins like your deployed frontend URL here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include RAG routes under a versioned API prefix
app.include_router(rag_routes.router, prefix="/api/rag")

# Health check route
@app.get("/")
async def root():
    return {"message": "✅ Welcome to DocuSage AI Backend!"}

# Run the app only if called directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
