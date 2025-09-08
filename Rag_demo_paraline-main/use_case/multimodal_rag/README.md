# Multimodal RAG Implementation

This implementation demonstrates a Multimodal Retrieval Augmented Generation (RAG) system that can process both text and images from PDF documents. The system combines the power of multiple AI models to provide accurate responses to queries about document content.

## Overview

The multimodal RAG system processes PDF documents containing both text and images, creates embeddings for both modalities, and uses them for retrieval and question answering.

## Key Components and Techniques

### 1. Document Processing
- **PDF Processing**: Using `Fitz` for extracting both text and images
- **Image Processing**: Using `PIL` for image handling
- Automatic extraction and storage of images in an `extracted_images` directory

### 2. Image Understanding
- **Model**: Google's Gemini 1.5 Flash model
- **Purpose**: Generates descriptive summaries of images
- **Technique**: Uses a specialized prompt for image captioning:
  ```python
  "You are an assistant tasked with summarizing tables, images and text for retrieval.
   These summaries will be embedded and used to retrieve the raw text or table elements
   Give a concise summary of the table or text that is well optimized for retrieval."
  ```

### 3. Text Processing and Chunking
- **Chunking Method**: RecursiveCharacterTextSplitter with tiktoken encoding
- **Parameters**:
  - Chunk size: 400 characters
  - Overlap: 50 characters
- **Document Structure**: Uses LangChain's Document class with metadata tracking

### 4. Embedding System
- **Model**: Cohere's embed-english-v3.0
- **Implementation**: Using `CohereEmbeddings` from LangChain
- **Features**: 
  - Processes both text chunks and image descriptions
  - Creates unified vector representations

### 5. Vector Storage and Retrieval
- **Vector Database**: ChromaDB
- **Retrieval Method**: Similarity search
- **Parameters**:
  - Top-k: 1 (retrieving the single most relevant document)
- **Implementation**: Combined storage of text and image embeddings in a single collection

### 6. Question Answering System
- **Model**: Cohere's command-r-plus
- **Temperature**: 0 (for maximum consistency)
- **Prompt Template**:
  ```
  System: You are an assistant for question-answering tasks. 
  Answer the question based upon your knowledge.
  Use three-to-five sentences maximum and keep the answer concise.
  ```
- **Chain Components**:
  1. Document Retrieval
  2. Prompt Formation
  3. LLM Processing
  4. Response Parsing

## Usage Example

```python
# Query example
query = "meaning of Figure 1: The Transformer - model architecture."

# Retrieve relevant documents
docs = retriever.invoke(query)

# Generate response using RAG chain
generation = rag_chain.invoke({
    "documents": docs[0].page_content,
    "question": query
})
```

```
Figure 1 illustrates the Transformer model architecture, a neural network used for processing sequential data. It shows the flow of information through the decoder layer, with inputs passing through various processes, including attention mechanisms and feed-forward networks, to produce output probabilities. The diagram provides a visual representation of the model's internal processes and connections.
```

## Required API Keys

The implementation requires two API keys:
1. `GOOGLE_API_KEY` - For Gemini model access
2. `COHERE_API_KEY` - For embeddings and LLM

## Dependencies

- Fitz
- PIL (Python Imaging Library)
- python-dotenv
- google.generativeai
- langchain
- langchain_cohere
- chromadb
- tiktoken

## Implementation Notes

1. The system processes both text and images simultaneously
2. Image descriptions are generated before chunking to ensure context preservation
3. The unified vector store allows for cross-modal retrieval
4. The system uses a consistent chunk size for both text and image descriptions
5. Temperature is set to 0 for the final LLM to ensure consistent responses
