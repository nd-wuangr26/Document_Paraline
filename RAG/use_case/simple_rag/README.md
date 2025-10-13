# Simple Retrieval-Augmented Generation (RAG)
## Tổng Quan về Simple Retrieval-Augmented Generation (RAG)

Retrieval-Augmented Generation (RAG) là một phương pháp tiên tiến trong lĩnh vực trí tuệ nhân tạo, đặc biệt trong xử lý ngôn ngữ tự nhiên (NLP). RAG kết hợp giữa hai kỹ thuật chính: truy xuất thông tin (retrieval) và sinh văn bản (generation), nhằm tạo ra các hệ thống có khả năng cung cấp câu trả lời chi tiết và chính xác dựa trên thông tin từ nhiều nguồn.

<img width="825" height="669" alt="image" src="https://github.com/user-attachments/assets/e38037be-71c8-4808-aded-476127392805" />

## Các bước thực hiện RAG 
1. Create Vector database: Đầu tiên, convert toàn bộ dữ liệu tri thức thành các vector và lưu trữ chúng vào một vector database.
2. User input: User cung cấp 1 câu truy vấn (query) bằng ngôn ngữ tự nhiên nhằm tìm kiếm câu trả lời hoặc để hoàn thành câu truy vấn đó.
3. Information retrieval: Cơ chế retrieval quét toàn vộ vector trong database để xác định các phân đoạn tri thức (chính là paragraphs) nào có ngữ nghĩa tương đồng với câu truy vấn của người dùng. Các paragraphs này sau đó được vào LLM để làm tăng context cho quá trình sinh ra câu trả lời.
4. Combining data: Các paragraphs được lấy sau quá trình retrieval từ database được kết hợp với câu query ban đầu của user tạo thành 1 câu prompt.
5. Generate text: Câu prompt được bổ sung thêm context sau đó được đưa qua LLM để sinh ra câu phản hồi cuối cùng theo context bổ sung.

## Ưu điểm
- Khả năng sử dụng hiệu quả các nguồn kiến ​​thức bên ngoài khi tạo văn bản. Bằng cách truy xuất thông tin từ nhiều nguồn khác nhau, các mô hình RAG có thể tạo ra phản hồi chính xác hơn, phù hợp ngữ cảnh và mang tính thông tin cao hơn so với các mô hình truyền thống chỉ dựa vào các mẫu được học nội bộ.
- Các mô hình RAG đã được áp dụng cho nhiều nhiệm vụ NLP khác nhau, bao gồm trả lời câu hỏi, tóm tắt, tạo đối thoại và tạo nội dung. Chúng đã cho thấy kết quả đầy hứa hẹn trong việc cải thiện chất lượng và mức độ phù hợp của văn bản được tạo ra bằng cách kết hợp kiến ​​thức bên ngoài trong quá trình tạo văn bản.
- RAG không yêu cầu training lại mô hình, tiết kiệm thời gian và tài nguyên tính toán.

## Nhược điểm 
- Chỉ có thể sử dụng trên dữ liệu text
- Hiệu suất của RAG phụ thuộc vào chất lượng độ chính xác của model retrieval, tính toàn diện và chính xác của kho tri thức có sẵn.

## Các Thành Phần của project 

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
