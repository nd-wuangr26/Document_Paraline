# Simple RAG
## Tổng Quan Hệ Thống

Hệ thống RAG này được thiết kế để xử lý và trả lời câu hỏi từ tài liệu PDF nội bộ. Sử dụng các thuật toán tính độ tương đồng để tìm ra những đoạn văn có trong document và lưu trữ các đoạn văn dưới dạng vector trong vector store. Đưa query của người dùng kết hợp với các chunk để đưa vào LLM để sinh ra câu trả lời.

<img width="327" height="154" alt="image" src="https://github.com/user-attachments/assets/308f6bd8-0813-4746-b9f9-c59ee46b2629" />


## Các Thành Phần Chính

### 1. Xử Lý và Phân Đoạn Văn Bản (Chunking)
- **Phương Pháp**: Semantic Chunking
- **Công cụ**: `SemanticChunker` từ LangChain
- **Đặc điểm**:
  - Phân đoạn văn bản dựa trên ngữ nghĩa
  - Sử dụng ngưỡng phần trăm (percentile) là 80%
  - Tiền xử lý văn bản:
    ```python
    chunk.page_content = chunk.page_content.replace("\n", " ")
    chunk.page_content = " ".join(chunk.page_content.split())
    ```

### 2. Embedding
- **Model**: AITeamVN/Vietnamese_Embedding
- **Framework**: HuggingFace Embeddings
- **Ứng dụng**: Chuyên biệt cho văn bản tiếng Việt

### 3. Vector Database
- **Công nghệ**: FAISS (Facebook AI Similarity Search)
- **Chức năng**:
  - Lưu trữ và tìm kiếm vector embeddings
  - Hỗ trợ tìm kiếm similarity nhanh chóng
- **Tính năng**:
  ```python
  # Tạo vector store
  def create_vector_store(chunks: Document) -> FAISS
  
  # Lưu vector store
  def save_vector_store(path: str) -> None
  
  # Tải vector store
  def load_vector_store(path: str) -> None
  ```

### 4. Re-ranking
- **Model**: BAAI/bge-reranker-v2-m3
- **Framework**: sentence-transformers CrossEncoder
- **Quy trình**:
  1. Ghép cặp query với từng đoạn văn
  2. Tính điểm tương đồng
  3. Sắp xếp kết quả theo điểm số

### 5. Language Model
- **Model**: openai/gpt-oss-20b (Fireworks AI)
- **Cấu hình**:
  - Sử dụng API tùy chỉnh với base_url
  - Xác thực qua API key
- **Chức năng**: Tạo câu trả lời dựa trên context

### 6. Quy Trình Truy Vấn
1. **Embedding Query**:
   ```python
   query_embedding = embeddings.embed_query(query)
   ```

2. **Tìm Kiếm Tương Đồng**:
   ```python
   retrieved = vector_db.similarity_search_by_vector(
       embedding=query_embedding,
       k=5
   )
   ```

3. **Prompt Engineering**:
   ```python
   combined_prompt = (
       f"Hãy trở thành chuyên gia tư vấn tuyển sinh đa ngành nghề của trường Đại học Kỹ thuật Công nghiệp - Đại học Thái Nguyên.\n"
       f"Câu hỏi của khách hàng: {query}\n"
       f"Dựa vào các thông tin sau, hãy trả lời:\n{passages}\n"
   )
   ```

## Yêu Cầu Hệ Thống

### Thư Viện
- langchain-community
- langchain-experimental
- langchain-huggingface
- sentence-transformers
- python-dotenv
- openai
- faiss-cpu

### Biến Môi Trường
```
BASE_URL=your_base_url
API_KEY=your_api_key
```

## Ưu Điểm của Hệ Thống
1. Tối ưu hóa cho tiếng Việt với embedding model chuyên biệt
2. Sử dụng semantic chunking cho phân đoạn thông minh
3. Kết hợp re-ranking để cải thiện độ chính xác
4. Prompt engineering được điều chỉnh cho bối cảnh cụ thể
5. Khả năng lưu trữ và tải lại vector store
