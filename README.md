📚 DocuDom Backend
DocuDom is a lightweight, production-ready backend service for secure, fast, and intelligent document-based Q&A using RAG (Retrieval-Augmented Generation). It powers document ingestion, chunking, embedding, vector search, and response generation via LLMs.

🚀 Features
⚡ Built with FastAPI for blazing fast performance

📄 Document ingestion, parsing, and chunking (PDF, TXT, etc.)

🤖 Embedding using text-embedding models (e.g. OpenAI, Titan, etc.)

🔍 MongoDB-based vector search and metadata storage

📦 Clean API for upload, indexing, and querying

🔐 .env-configurable secrets and token usage

🧠 Easily pluggable with LangChain & Bedrock/Vertex/Gemini

🌐 Deployable on Vercel, Render, or AWS Lambda (Zappa)

📁 Folder Structure
bash
Copy
Edit
backend/
│
├── app/
│   ├── main.py          # FastAPI entrypoint
│   ├── routes/          # API endpoints (query, upload, health)
│   ├── services/        # Core logic (embed, search, chunk)
│   ├── models/          # Pydantic models for request/response
│   └── config.py        # Env + MongoDB setup
│
├── .env                 # Secrets (ignored in .gitignore)
├── requirements.txt     # All Python dependencies
├── README.md            # You're here
└── zappa_settings.json  # (optional) AWS Lambda config
⚙️ Setup Instructions
1. Clone and Setup Environment
bash
Copy
Edit
git clone https://github.com/your-username/docudom-backend.git
cd docudom-backend/backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
2. Set Up Environment Variables
Create a .env file in the backend/ directory:

env
Copy
Edit
MONGO_URI=mongodb+srv://<your-mongodb-url>
MONGO_DB=docudom
MONGO_COLLECTION=documents

EMBEDDING_PROVIDER=openai         # or titan, vertexai, ollama
EMBEDDING_API_KEY=your_key_here
3. Run Locally
bash
Copy
Edit
uvicorn app.main:app --reload
Visit http://localhost:8000/docs for interactive API docs.

🧪 API Endpoints
Method	Endpoint	Description
POST	/api/upload	Upload and index documents
POST	/api/query	Ask a question from the docs
GET	/api/health	Health check

🚀 Deployment Options
✅ Vercel / Render
Set environment variables in your dashboard.

Connect this repo.

Point start command to: uvicorn app.main:app --host=0.0.0.0 --port=8000

✅ AWS Lambda (Zappa)
bash
Copy
Edit
zappa deploy dev
Make sure zappa_settings.json is properly configured.

📦 Requirements (Partial)
txt
Copy
Edit
fastapi
pymongo
langchain
tiktoken
uvicorn
python-dotenv
zstandard
🧠 Powered By
🧬 LangChain

🧠 LLMs: OpenAI, Titan, Gemini, Claude (plug & play)

📊 MongoDB Atlas Vector Search