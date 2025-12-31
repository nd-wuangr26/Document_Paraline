import os
import uuid
from typing import List, Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from openai import OpenAI
from docling.document_converter import DocumentConverter
from docling_core.types.doc.document import ImageRefMode
from docling.chunking import HybridChunker
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchText
from dotenv import load_dotenv

load_dotenv()

# Configuration
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
COLLECTION_NAME = os.getenv("QDRANT_COLLECTION", "agentic_rag")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize Clients
if QDRANT_URL == ":memory:":
    qdrant = QdrantClient(location=":memory:")
else:
    qdrant = QdrantClient(url=QDRANT_URL)

openai_client = OpenAI(api_key=OPENAI_API_KEY)

def init_collection():
    """Initialize Qdrant collection if it doesn't exist."""
    if not qdrant.collection_exists(COLLECTION_NAME):
        qdrant.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
        )
        print(f"Collection '{COLLECTION_NAME}' created.")
    else:
        print(f"Collection '{COLLECTION_NAME}' already exists.")

def get_embedding(text: str) -> List[float]:
    """Get embedding using OpenAI text-embedding-3-small."""
    if not text:
        return [0.0] * 1536
    text = text.replace("\n", " ")
    response = openai_client.embeddings.create(input=[text], model="text-embedding-3-small")
    return response.data[0].embedding

def ingest_file(file_path: str):
    """Process a file using Docling, chunk it, and store in Qdrant."""
    print(f"Ingesting file: {file_path}")
    
    # Ensure collection exists before doing anything
    init_collection()
    
    # 1. Processing with Docling
    converter = DocumentConverter()
    result = converter.convert(file_path)
    doc = result.document
    
    # from pathlib import Path   
    # output_dir = Path("/home/quang/My_Project/Document_Paraline/Agentic_RAG/backend/uploaded_files/converted")
    # output_dir.mkdir(parents=True, exist_ok=True)
    # doc_filename = Path(file_path).stem

    # # Save markdown with externally referenced pictures
    # md_filename = output_dir / f"{doc_filename}-with-image-refs.md"
    # doc.save_as_markdown(md_filename, image_mode=ImageRefMode.REFERENCED, include_annotations=True)
    # print(f"Saved converted markdown to: {md_filename}")
    
    # 2. Hybrid Chunking
    chunker = HybridChunker()
    chunk_iter = chunker.chunk(doc)
    
    points = []
    for chunk in chunk_iter:
        text = chunk.text
        if not text.strip():
            continue
            
        embedding = get_embedding(text)
        
        # Create a payload
        payload = {
            "text": text,
            "source": file_path,
            "page": chunk.meta.page_no if hasattr(chunk.meta, 'page_no') else None
        }
        
        points.append(PointStruct(
            id=str(uuid.uuid4()), 
            vector=embedding,
            payload=payload
        ))
        
    # 3. Upsert to Qdrant
    if points:
        qdrant.upsert(collection_name=COLLECTION_NAME, points=points)
        print(f"Upserted {len(points)} chunks to Qdrant.")
    else:
        print("No chunks generated.")


def init_collection():
    """Initialize Qdrant collection if it doesn't exist."""
    if not qdrant.collection_exists(COLLECTION_NAME):
        qdrant.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
        )
        print(f"Collection '{COLLECTION_NAME}' created.")
    else:
        print(f"Collection '{COLLECTION_NAME}' already exists.")
        
    # Create Full-Text Index for Keyword Search
    try:
        qdrant.create_payload_index(
            collection_name=COLLECTION_NAME,
            field_name="text",
            field_schema="text"
        )
        print("Payload index for 'text' ensured.")
    except Exception as e:
        print(f"Index creation note: {e}")

# ... existing code ...

def search_rag(query: str, limit: int = 3) -> List[Dict[str, Any]]:
    """Search for relevant context using Hybrid Search (Vector + Keyword)."""
    
    # Split limit for Hybrid Strategy
    # If limit is 10, we do 5 Vector + 5 Keyword
    vector_limit = (limit + 1) // 2 
    keyword_limit = limit // 2
    
    results = []
    
    # 1. Semantic Search (Vector)
    try:
        query_vector = get_embedding(query)
        vector_hits = qdrant.query_points(
            collection_name=COLLECTION_NAME,
            query=query_vector,
            limit=vector_limit
        ).points
        results.extend([hit.payload for hit in vector_hits])
    except Exception as e:
        print(f"Vector search failed: {e}")

    # 2. Keyword Search (Lexical)
    try:
        if keyword_limit > 0:
            keyword_hits, _ = qdrant.scroll(
                collection_name=COLLECTION_NAME,
                scroll_filter=Filter(
                    must=[FieldCondition(key="text", match=MatchText(text=query))]
                ),
                limit=keyword_limit,
                with_payload=True,
                with_vectors=False
            )
            results.extend([hit.payload for hit in keyword_hits])
    except Exception as e:
        print(f"Keyword search failed: {e}")
        
    return results

if __name__ == "__main__":
    # Test initialization
    init_collection()
