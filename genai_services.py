import os
from typing import List
from openai import OpenAI
from dotenv import load_dotenv
import tiktoken
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv(".env")

# Environment variables
api_key = os.getenv("MODEL_API_KEY")
base_url = os.getenv("MODEL_BASE_URL")
model_name = os.getenv("MODEL_NAME")

assert api_key and base_url and model_name, "❌ Missing API environment variables."

openai_client = OpenAI(api_key=api_key, base_url=base_url)

def call_llm(messages: List[dict], max_tokens: int = 1000) -> str:
    """Call the LLM with error handling and retry logic."""
    try:
        response = openai_client.chat.completions.create(
            model=model_name,
            messages=messages,
            max_tokens=max_tokens,
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"LLM call failed: {e}")
        return f"⚠️ Error calling LLM: {e}"

def summarize_text(text: str) -> str:
    """Generate a concise summary of the given text."""
    messages = [
        {
            "role": "system", 
            "content": "You are a helpful assistant that creates concise, informative summaries. Focus on key points and main themes."
        },
        {
            "role": "user", 
            "content": f"Please provide a comprehensive summary of this text, highlighting the main points and key information:\n\n{text}"
        }
    ]
    return call_llm(messages, max_tokens=500)

def chunk_text(text: str, chunk_size: int = 500, chunk_overlap: int = 50) -> List[str]:
    """Split text into overlapping chunks using tiktoken."""
    if not text:
        return []

    try:
        enc = tiktoken.get_encoding("cl100k_base")
    except Exception:
        # Fallback to character-based chunking
        logger.warning("Tiktoken not available, using character-based chunking")
        chunks = []
        for i in range(0, len(text), chunk_size - chunk_overlap):
            chunks.append(text[i:i + chunk_size])
        return chunks

    tokens = enc.encode(text)
    chunks = []
    
    i = 0
    while i < len(tokens):
        end = min(i + chunk_size, len(tokens))
        chunk_tokens = tokens[i:end]
        chunk_text = enc.decode(chunk_tokens)
        chunks.append(chunk_text)
        
        # Move to next chunk with overlap
        i = end - chunk_overlap if end < len(tokens) else end
    
    return chunks

def answer_with_context(question: str, contexts: List[str]) -> str:
    """Generate an answer based on the provided context."""
    context_str = "\n\n---\n\n".join(contexts)
    
    messages = [
        {
            "role": "system", 
            "content": """You are a helpful assistant that answers questions based on provided context. 
            Follow these guidelines:
            - Answer directly and concisely
            - Use information from the context when available
            - If the context doesn't contain enough information, say so clearly
            - Don't make up information not in the context
            - Cite specific parts of the context when relevant
            -Present the information in a clear and concise manner.
            -Use lists and bullet points when appropriate."""
        },
        {
            "role": "user", 
            "content": f"Context:\n{context_str}\n\nQuestion: {question}\n\nAnswer:"
        }
    ]
    
    return call_llm(messages)