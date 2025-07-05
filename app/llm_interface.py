# backend/app/llm_interface.py

import os
import ollama
from dotenv import load_dotenv
from typing import Dict, Any

load_dotenv()

# Defaults from .env or fallback values
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL_NAME = os.getenv("OLLAMA_MODEL_NAME", "tinyllama")

# You can also explicitly set the host via env var
os.environ["OLLAMA_HOST"] = OLLAMA_HOST

# --- Ollama LLM Interface ---
async def call_ollama_llm(prompt: str, context: str) -> Dict[str, Any]:
    """
    Calls the Ollama LLM with the given prompt and context.
    """
    try:
        system_prompt = (
            "You are a precise and concise assistant. Only answer questions using the provided context.\n"
            "If the answer is not clearly available in the context, respond with: 'I don't know based on the given information.'\n"
            "Always return the answer in **exactly one clear and informative sentence** — no extra details or bullet points."
        )


        final_prompt = (
            f"Context:\n{context}\n\n"
            f"Question:\n{prompt}\n\n"
            f"Answer:"
        )

        response = ollama.chat(
            model=OLLAMA_MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": final_prompt}
            ],
            options={
                "temperature": 0.3,
                "num_ctx": 4096,
            }
        )

        return {
            "answer": response.get("message", {}).get("content", "⚠️ No response from LLM."),
            "source_documents": []
        }

    except Exception as e:
        print(f"❌ Ollama error: {e}")
        return {
            "answer": f"❌ Error: {str(e)}",
            "source_documents": []
        }

# --- Public Function Used in RAG ---
async def call_llm(prompt: str, context: str) -> Dict[str, Any]:
    return await call_ollama_llm(prompt, context)
