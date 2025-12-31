from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).resolve().parents[3]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
    
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
import sys
import os

# Add parent directory to sys.path to allow imports from 'backend' package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.rag import ingest_file, init_collection
from backend.agent import LangGraphAgent
import shutil
import os
import uvicorn

app = FastAPI(title="Agentic RAG Backend API")
agent = LangGraphAgent()

# Initialize connection on startup
@app.on_event("startup")
async def startup_event():
    init_collection()

class ChatRequest(BaseModel):
    query: str
    thread_id: str = "default_user"

@app.post("/ingest")
async def ingest_document(file: UploadFile = File(...)):
    # Save file temporarily
    upload_dir = "uploaded_files"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        # Ingest
        ingest_file(file_path)
        return {"status": "success", "message": f"Successfully ingested {file.filename}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        # Agent run with thread_id
        result = agent.run(request.query, thread_id=request.thread_id)
        return result
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
