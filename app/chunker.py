# backend/app/chunker.py

import os
from typing import List
from PyPDF2 import PdfReader

# Optional: Uncomment below to use LangChain-style chunking for better results
# from langchain.text_splitter import RecursiveCharacterTextSplitter

def chunk_text(text: str, chunk_size: int = 1000, chunk_overlap: int = 100) -> List[str]:
    """
    Splits a string into overlapping chunks of specified size.
    """
    chunks = []
    current_position = 0

    while current_position < len(text):
        end_position = min(current_position + chunk_size, len(text))
        chunk = text[current_position:end_position]
        chunks.append(chunk.strip())
        current_position += (chunk_size - chunk_overlap)

        # Edge safety
        if chunk_size <= chunk_overlap:
            print("⚠️ chunk_size must be greater than chunk_overlap to avoid infinite loop.")
            break

    return chunks

def extract_text_from_pdf(file_path: str) -> str:
    """
    Extracts all text from a PDF file using PyPDF2.
    """
    try:
        with open(file_path, 'rb') as file:
            reader = PdfReader(file)
            return "\n".join([page.extract_text() or "" for page in reader.pages])
    except Exception as e:
        print(f"❌ Error extracting text from PDF '{file_path}': {e}")
        return ""

def process_document(file_path: str) -> List[str]:
    """
    Handles file type detection, text extraction, and chunking.
    Supports PDF, TXT, and optionally DOCX.
    """
    ext = os.path.splitext(file_path)[1].lower()
    text = ""

    if ext == ".pdf":
        text = extract_text_from_pdf(file_path)

    elif ext in [".txt", ".md"]:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
        except Exception as e:
            print(f"❌ Error reading {file_path}: {e}")
            return []

    elif ext == ".docx":
        print(f"⚠️ DOCX support not implemented. Skipping: {file_path}")
        # To support: pip install python-docx
        # from docx import Document
        # doc = Document(file_path)
        # text = "\n".join([para.text for para in doc.paragraphs])
        return []

    else:
        print(f"❌ Unsupported file type: {ext} for {file_path}")
        return []

    return chunk_text(text) if text else []
