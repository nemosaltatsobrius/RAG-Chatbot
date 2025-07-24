# main.py (Homepage)
import streamlit as st

st.set_page_config(
    page_title="RAG QnA & Summarization Chatbot", 
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🤖 RAG Chatbot")
st.markdown("""
Welcome to the RAG (Retrieval-Augmented Generation) Chatbot! This application allows you to:

### **Document Processing**
- Upload documents in various formats (PDF, DOCX, TXT, MD, HTML)
- Automatic text extraction and chunking
- Document summarization using AI

###  **Intelligent Q&A**
- Ask questions about your uploaded documents
- Get contextual answers based on document content
- View retrieved context for transparency

###  **Getting Started**
1. **Upload Documents**: Use the sidebar to navigate to the "Document Ingestion" page
2. **Ask Questions**: Go to the "Chatbot" page to interact with your documents

---
*Choose a page from the sidebar to begin!*
""")

# Add some stats if ChromaDB has data
try:
    from chroma_services import collection
    doc_count = collection.count()
    if doc_count > 0:
        st.info(f"📊 Currently storing {doc_count} document chunks in the database")
except Exception:
    st.info("📊 No documents ingested yet")