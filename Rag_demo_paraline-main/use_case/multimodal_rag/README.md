# Multimodal RAG

Triển khai này trình bày một hệ thống Multimodal Retrieval Augmented Generation (RAG) có khả năng xử lý cả văn bản và hình ảnh từ tài liệu PDF. Hệ thống kết hợp sức mạnh của nhiều mô hình AI để cung cấp câu trả lời chính xác cho các truy vấn về nội dung tài liệu.

<img width="1999" height="734" alt="image" src="https://github.com/user-attachments/assets/bd5da1fe-b04e-4b8e-b01f-8f3f65dea5cb" />


## Overview

Hệ thống RAG đa phương thức xử lý tài liệu PDF chứa cả văn bản và hình ảnh, tạo embeddings cho cả hai phương thức, và sử dụng chúng cho việc truy xuất và trả lời câu hỏi.


## Key Components and Techniques

### 1. Document Processing
- **PDF Processing**: `Fitz` để trích xuất cả văn bản và hình ảnh
- **Image Processing**: Sử dụng `PIL` để xử lý hình ảnh
- Tự động trích xuất và lưu trữ hình ảnh trong thư mục `extracted_images`

### 2. Image Understanding
- **Model**: Salesforce/blip-image-captioning-base
- **Purpose**: Tạo ra các mô tả tóm tắt của hình ảnh

### 3. Text Processing and Chunking
- **Chunking Method**: Sử dụng class RecursiveCharacterTextSplitter
- **Parameters**:
  - Chunk size: 400 ký tự
  - Overlap: 50 ký tự
- **Document Structure**: Sử dụng class Document của LangChain

### 4. Embedding System
- **Model**: Cohere's embed-english-v3.0
- **Triển khai**: Sử dụng `CohereEmbeddings` từ LangChain
- **Features**: 
  - Xử lý cả đoạn văn bản và mô tả hình ảnh
  - Tạo biểu diễn vector thống nhất

### 5. Vector Storage and Retrieval
- **Vector Database**: ChromaDB
- **Retrieval Method**: Similarity search
- **Parameters**:
  - Top-k: 1 (truy xuất tài liệu có liên quan nhất)
- **Implementation**: Lưu trữ kết hợp embeddings văn bản và hình ảnh trong một bộ sưu tập

### 6. Question Answering System
- **Model**: Cohere's command-r-plus
- **Temperature**: 0 (để đảm bảo tính nhất quán tối đa)
- **Prompt Template**:
  ```
  System: You are an assistant for question-answering tasks. 
  Answer the question based upon your knowledge.
  Use three-to-five sentences maximum and keep the answer concise.
  ```
- **Chain Components**:
  1. Truy xuất tài liệu
  2. Tạo Prompt
  3. Xử lý LLM
  4. Phân tích cú pháp phản hồi

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

Triển khai yêu cầu hai API keys:
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

1. Hệ thống xử lý đồng thời cả văn bản và hình ảnh
2. Mô tả hình ảnh được tạo trước khi phân đoạn để đảm bảo bảo toàn ngữ cảnh
3. Vector store thống nhất cho phép truy xuất đa phương thức
4. Hệ thống sử dụng kích thước đoạn nhất quán cho cả văn bản và mô tả hình ảnh
5. Temperature được đặt thành 0 cho LLM cuối cùng để đảm bảo phản hồi nhất quán
