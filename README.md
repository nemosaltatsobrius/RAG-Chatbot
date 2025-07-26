# RAG QnA & Summarization Chatbot

This project is a Streamlit web application that demonstrates the power of Retrieval-Augmented Generation (RAG) for question-answering and text summarization. It allows users to upload documents, which are then processed and stored in a vector database (ChromaDB). Users can then ask questions about the documents or request summaries, and the application will use a Large Language Model (LLM) to generate responses based on the retrieved context.

## Features

- **Document Upload:** Supports various file formats, including PDF, DOCX, TXT, MD, and HTML.
- **Text Processing:** Automatically extracts text from uploaded documents and splits it into manageable chunks.
- **Vector Storage:** Uses ChromaDB to store document chunks as vector embeddings for efficient similarity search.
- **Intelligent Q&A:** Ask questions and receive contextual answers based on the content of your uploaded documents.
- **Document Summarization:** Generate concise summaries of your documents using an AI-powered model.
- **Contextual Transparency:** View the specific document chunks that were retrieved to generate an answer.

## How it Works

The application follows a standard RAG pipeline:

1.  **Ingestion:** When a document is uploaded, it's converted to plain text and then split into smaller chunks. Each chunk is then converted into a numerical vector (embedding) and stored in the ChromaDB vector database.
2.  **Retrieval:** When a user asks a question, the question is also converted into a vector embedding. This embedding is then used to query the ChromaDB database and find the most relevant document chunks (i.e., those with the most similar embeddings).
3.  **Generation:** The retrieved document chunks are then passed to a Large Language Model (LLM) along with the original question. The LLM uses this context to generate a comprehensive and accurate answer.

## Getting Started

### Prerequisites

- Python 3.7+
- An API key for a Large Language Model (e.g., OpenAI)

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/RAG-Chatbot.git
    cd RAG-Chatbot
    ```

2.  **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up your environment variables:**

    Create a `.env` file in the root directory of the project and add the following variables:

    ```env
    MODEL_API_KEY="your-api-key"
    MODEL_BASE_URL="your-model-base-url"
    MODEL_NAME="your-model-name"
    CHROMA_COLLECTION_NAME="your-chroma-collection-name"
    ```

### Running the Application

To start the Streamlit application, run the following command in your terminal:

```bash
streamlit run main.py
```

## Project Structure

```
RAG-Chatbot/
├── .gitignore
├── chroma_services.py      # Handles interactions with the ChromaDB vector database
├── genai_services.py       # Manages interactions with the Large Language Model
├── main.py                 # The main Streamlit application file
├── requirements.txt        # A list of all the project's dependencies
├── template.env            # A template for the .env file
├── test_grok.py
├── pages/
│   ├── chatbot_page.py     # The chatbot interface
│   └── ingest_page.py      # The document ingestion and summarization page
├── chroma_db/              # The directory where the ChromaDB database is stored
└── ...
```

## Contributing

Contributions are welcome! If you have any ideas, suggestions, or bug reports, please open an issue or submit a pull request.
