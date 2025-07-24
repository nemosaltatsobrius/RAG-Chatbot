import streamlit as st
from genai_services import answer_with_context
from chroma_services import query_documents

st.title("💬 RAG Q&A Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant" and "context" in message:
            with st.expander("📚 Retrieved Context"):
                st.markdown(message["context"])

# Chat input
if prompt := st.chat_input("Ask a question about your documents..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Searching documents and generating answer..."):
            # Query documents
            context_chunks = query_documents(prompt, n_results=3)
            
            if not context_chunks:
                response = "❌ No relevant context found. Please ingest a document first using the Document Ingestion page."
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            else:
                # Generate answer
                answer = answer_with_context(prompt, context_chunks)
                st.markdown(answer)
                
                # Show context
                context_display = "\n\n---\n\n".join(context_chunks)
                with st.expander("📚 Retrieved Context"):
                    st.markdown(context_display)
                
                # Add to chat history
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": answer,
                    "context": context_display
                })

# Sidebar with chat controls
with st.sidebar:
    st.header("💬 Chat Controls")
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
    
    # Display document count
    try:
        from chroma_services import collection
        doc_count = collection.count()
        st.metric("📊 Document Chunks", doc_count)
    except Exception as e:
        st.metric("📊 Document Chunks", "0")
        print(f"Failed to get document count: {e}")