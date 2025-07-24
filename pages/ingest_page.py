import streamlit as st
from genai_services import summarize_text, chunk_text
from chroma_services import ingest_documents
import tempfile
import os
import uuid

try:
    from markitdown import MarkItDown
except ImportError:
    st.error(
        "❌ `markitdown` not found. Please install via `pip install markitdown[all]`"
    )
    st.stop()

st.title("Document Ingestion & Summarization")

# Initialize session state
if "processed_doc" not in st.session_state:
    st.session_state.processed_doc = None
if "doc_summary" not in st.session_state:
    st.session_state.doc_summary = None

uploaded_file = st.file_uploader(
    "Upload a document",
    type=["txt", "pdf", "md", "html", "docx"],
    help="Supported formats: TXT, PDF, Markdown, HTML, DOCX",
)

if uploaded_file:
    # Create temporary file
    with tempfile.NamedTemporaryFile(
        delete=False, suffix=os.path.splitext(uploaded_file.name)[1]
    ) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    try:
        # Convert document to text
        converter = MarkItDown()
        doc_text = converter.convert(tmp_path).text_content
        st.session_state.processed_doc = doc_text

        # Display document info
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Document Size", f"{len(doc_text)} characters")
        with col2:
            st.metric("Estimated Chunks", f"{len(chunk_text(doc_text))}")

        # Document preview
        st.subheader("Document Preview")
        with st.expander("View extracted text", expanded=False):
            st.text_area("Extracted Text", doc_text, height=300, disabled=True)

        # Processing options
        col1, col2 = st.columns(2)

        with col1:
            if st.button("Generate Summary", type="secondary"):
                with st.spinner("Generating summary..."):
                    summary = summarize_text(doc_text)
                    st.session_state.doc_summary = summary

        with col2:
            if st.button("🔄 Ingest to Database", type="primary"):
                with st.spinner("Processing and ingesting document..."):
                    chunks = chunk_text(doc_text)
                    chunk_ids = [f"{uploaded_file.name}_{uuid.uuid4()}" for _ in chunks]
                    ingested_count = ingest_documents(chunks, chunk_ids)

                    if ingested_count > 0:
                        st.success(f"Successfully ingested {ingested_count} chunks!")
                        st.info("Dataset Updated")
                    else:
                        st.error("❌ Failed to ingest document")

        # Display summary if available
        if st.session_state.doc_summary:
            st.subheader("Document Summary")
            st.markdown(st.session_state.doc_summary)

    except Exception as e:
        st.error(f"❌ Error processing document: {str(e)}")
    finally:
        # Clean up temporary file
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
