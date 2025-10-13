

# GraphRAG Workflow Documentation

## Tổng quan
- GraphRAG là một workflow kết hợp giữa Knowledge Graph (Neo4j) và Large Language Model (LLM) để thực hiện truy vấn ngữ nghĩa, lưu trữ tri thức và hội thoại thông minh trên dữ liệu văn bản. Dưới đây là mô tả chi tiết các bước hoạt động, flow, và các thông tin cần thiết để triển khai GraphRAG.

---
## Giải thích chi tiết các bước truy vấn GraphRAG

🔹 **1. Query → Cypher Query (nếu dùng Neo4j hoặc GraphStore)**

- Khi bạn nhập query (ví dụ: "Who is the security manager of Company X?"), LlamaIndex sẽ dùng LLM để dịch câu hỏi tự nhiên thành một query dạng graph (thường là Cypher).

- Ví dụ:

```cypher
MATCH (c:Company {name: "Company X"})-[:HAS_SECURITY_MANAGER]->(p:Person)
RETURN p.name
```

🔹 **2. Traverse trên Knowledge Graph**

- Knowledge Graph lưu dưới dạng triplets (Entity–Relation–Entity).

- Engine sẽ traverse graph để tìm các node và edge liên quan.

- Bạn có thể config độ sâu (traverse depth), số triplet tối đa (`max_triplets_per_chunk`), hay cách expand node.

🔹 **3. Tích hợp Text Retrieval (nếu include_text=True)**

- Nếu query không chỉ cần quan hệ mà cần thêm context → LlamaIndex sẽ lấy thêm text chunks gốc liên quan đến các node/edge đã tìm.

- Các text này có embedding nên có thể dùng similarity search để bổ sung chi tiết.

---
## 1. Chuẩn bị môi trường
- **Kiểm tra thư mục làm việc:**
  - Sử dụng Python để kiểm tra và in ra thư mục hiện tại.
- **Khởi động các dịch vụ Docker:**
  - Sử dụng `docker compose up -d` để khởi động Neo4j và các dịch vụ cần thiết cho vectorDB.
- **Cài đặt các thư viện:**
  - Cài đặt các package: `llama-index`, `neo4j`, `llama-index-graph-stores-neo4j`.

---

## 2. Chuẩn bị dữ liệu
- **Tải dữ liệu mẫu:**
  - Dùng lệnh `curl` để tải file text mẫu từ Project Gutenberg về thư mục `data_sample`.
- **Đọc dữ liệu:**
  - Sử dụng `SimpleDirectoryReader` để đọc file text và kiểm tra nội dung.

---

## 3. Kết nối Neo4j Knowledge Graph
- **Kết nối tới Neo4j:**
  - Sử dụng `Neo4jGraphStore` với thông tin đăng nhập và địa chỉ Bolt.
  - Tạo `StorageContext` để quản lý lưu trữ cho Knowledge Graph.

---

## 4. Cấu hình LLM và Embedding
- **Cấu hình OpenAI LLM và Embedding:**
  - Sử dụng biến môi trường `OPENAI_API_KEY`.
  - Khởi tạo `OpenAI` cho LLM và `OpenAIEmbedding` cho embedding.

---

## 5. Tạo Knowledge Graph Index
- **Embedding và trích xuất triplets:**
  - Sử dụng `KnowledgeGraphIndex.from_documents` để tạo index từ documents.
  - Tham số `llm` dùng để extract triplets, `embed_model` để tạo embeddings.
  - Có thể điều chỉnh số triplets mỗi chunk và bật hiển thị tiến trình.

---

## 6. Truy vấn Knowledge Graph
- **Tạo query engine:**
  - Sử dụng `as_query_engine` để tạo engine truy vấn kết hợp KG và văn bản.
  - Có thể chọn chế độ trả lời (ví dụ: `tree_summarize`) và số lượng kết quả tương tự.
- **Thực hiện truy vấn:**
  - Gửi câu hỏi (ví dụ: "Who is Fred") và nhận kết quả trả về từ KG.

---

## 7. Giao diện hội thoại (Gradio)
- **Thiết lập bộ nhớ hội thoại:**
  - Sử dụng `ChatMemoryBuffer` để lưu lịch sử hội thoại.
- **Hàm truy vấn hội thoại:**
  - Tạo prompt dựa trên lịch sử hội thoại và truy vấn KG.
  - Lưu lại câu hỏi và câu trả lời vào bộ nhớ.
- **Giao diện Gradio:**
  - Tạo chatbot UI với Gradio, cho phép người dùng nhập câu hỏi và nhận câu trả lời từ KG.
  - Có nút Clear để xóa lịch sử hội thoại.

---

## 8. Các thông tin cần thiết
- **Biến môi trường:**
  - Cần có file `.env` chứa `OPENAI_API_KEY`.
- **Cấu hình Neo4j:**
  - Đảm bảo Neo4j chạy ở địa chỉ với user và password giống như trong docker compose (có thể thay đổi).
- **Dữ liệu:**
  - File text mẫu cần được tải về đúng vị trí.
- **Các package:**
  - Đảm bảo đã cài đặt đầy đủ các package cần thiết.

---

## 9. Flow tổng quát
1. Khởi động môi trường (Docker, cài package)
2. Tải và đọc dữ liệu
3. Kết nối Neo4j
4. Cấu hình LLM và embedding
5. Tạo Knowledge Graph Index từ dữ liệu
6. Tạo query engine và thực hiện truy vấn
7. Tương tác hội thoại qua Gradio

---

## 10. Lưu ý
- Đảm bảo các service (Neo4j, Docker) đã chạy trước khi thực hiện các bước tiếp theo.
- Kiểm tra biến môi trường và quyền truy cập file dữ liệu.
- Có thể mở rộng workflow với các loại dữ liệu khác, LLM khác hoặc các tính năng nâng cao của LlamaIndex và Neo4j.

---
## Liên hệ & đóng góp
- Tác giả: Hoàng
- Repo: https://github.com/viphoangdep/Rag_demo_paraline

---
Bạn có thể mở rộng thêm các tool hoặc tích hợp LLM khác theo nhu cầu.
## Tài liệu tham khảo
- [LlamaIndex Documentation](https://docs.llamaindex.ai/)
- [Neo4j Documentation](https://neo4j.com/docs/)
- [Gradio Documentation](https://gradio.app/docs/)
- [GraphRAG-Microsoft](https://github.com/microsoft/graphrag)

