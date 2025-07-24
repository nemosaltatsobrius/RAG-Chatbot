import chromadb
import os
from dotenv import load_dotenv
from typing import List
import logging

logger = logging.getLogger(__name__)

load_dotenv(".env")

collection_name = os.getenv("CHROMA_COLLECTION_NAME")
assert collection_name, "❌ Missing CHROMA_COLLECTION_NAME in .env"

# Initialize ChromaDB
try:
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    collection = chroma_client.get_or_create_collection(name=collection_name)
    logger.info(f"Connected to ChromaDB collection: {collection_name}")
except Exception as e:
    logger.error(f"Failed to initialize ChromaDB: {e}")
    raise

def ingest_documents(docs: List[str], ids: List[str]) -> int:
    """Ingest documents into ChromaDB."""
    if not docs or not ids:
        return 0
    
    assert len(docs) == len(ids), "IDs and documents must match in length"
    
    try:
        collection.add(documents=docs, ids=ids)
        logger.info(f"Successfully ingested {len(docs)} documents")
        return len(docs)
    except Exception as e:
        logger.error(f"Ingestion failed: {e}")
        return 0

def query_documents(query_text: str, n_results: int = 3) -> List[str]:
    """Query documents from ChromaDB."""
    try:
        results = collection.query(
            query_texts=[query_text], 
            n_results=n_results
        )
        
        documents = results.get('documents', [[]])[0]
        logger.info(f"Retrieved {len(documents)} documents for query: {query_text[:50]}...")
        
        return documents
    except Exception as e:
        logger.error(f"Query failed: {e}")
        return []

def get_collection_stats() -> dict:
    """Get statistics about the collection."""
    try:
        return {
            "count": collection.count(),
            "name": collection_name
        }
    except Exception as e:
        logger.error(f"Failed to get collection stats: {e}")
        return {"count": 0, "name": collection_name}

def clear_collection() -> bool:
    """Clear all documents from the collection."""
    try:
        # Get all IDs and delete them
        all_docs = collection.get()
        if all_docs['ids']:
            collection.delete(ids=all_docs['ids'])
            logger.info("Collection cleared successfully")
            return True
        return True
    except Exception as e:
        logger.error(f"Failed to clear collection: {e}")
        return False