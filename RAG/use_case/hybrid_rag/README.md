# HybridRAG Workflow Documentation

## Tổng quan
HybridRAG là workflow kết hợp giữa các phương pháp truy vấn truyền thống (BM25), truy vấn vector (embedding), truy vấn graph (graph traversal), nhằm tạo ra kết quả truy vấn tốt nhất. 

Trong demo này chúng ta sẽ sử dụng phương pháp truy vấn BM25 + vector search, kết hợp với Weaviate làm vectorDB và HuggingFace cho embedding. Dưới đây là mô tả chi tiết các bước hoạt động, flow, và các thông tin cần thiết để triển khai HybridRAG.

---

## 1. Chuẩn bị môi trường
- **Kiểm tra thư mục làm việc:**
  - Sử dụng Python để kiểm tra và in ra thư mục hiện tại.
- **Cài đặt các thư viện:**
  - Cài đặt các package: `fitz` (PyMuPDF), `llama-index`, `weaviate-client`, `huggingface`, `gradio`, `python-dotenv`, `llama-index-embeddings-huggingface`.
  - Chạy lệnh sau ở cell đầu tiên của notebook:
    ```python
    !pip install llama-index weaviate-client huggingface-hub pymupdf gradio python-dotenv llama-index-embeddings-huggingface
    ```
  - Nếu dùng embedding HuggingFace, cần cài thêm:
    ```python
    !pip install llama-index-embeddings-huggingface
    ```

---

## 2. Đọc và xử lý dữ liệu PDF
- **Đọc file PDF:**
  - Sử dụng PyMuPDF để mở file PDF và lấy Table of Contents (TOC).
  - In ra các mục lục, tiêu đề, và số trang bắt đầu.
- **Tách và làm sạch dữ liệu:**
  - Hàm `chunk_pdf_hierarchical` sẽ tách PDF thành các đoạn (chunk) theo TOC, làm sạch text và sinh metadata cho từng đoạn.
  - Nếu không có TOC, toàn bộ file sẽ thành một chunk.

---

## 3. Tách chunk theo hierarchy
- **Tách chunk nhỏ hơn:**
  - Sử dụng `HierarchicalNodeParser` của LlamaIndex để tách các chunk lớn thành các sub-chunk nhỏ hơn với các kích thước khác nhau.
  - Kết hợp metadata gốc và metadata sinh ra từ node parser.

---

## 4. Lưu trữ embedding vào VectorDB (Weaviate)
- **Kết nối Weaviate:**
  - Kết nối tới Weaviate server, xóa collection cũ nếu có, tạo collection mới tên 'Security'.
- **Sinh embedding:**
  - Sử dụng HuggingFaceEmbedding (ví dụ model Qwen/Qwen3-Embedding-0.6B) để sinh embedding cho từng chunk.
- **Batch insert:**
  - Thêm từng chunk vào collection 'Security' với embedding và metadata, sử dụng batch động để tối ưu hiệu năng.

---

## 5. Truy vấn dữ liệu

- **BM25 Search:**
  - Truy vấn dựa trên từ khóa truyền thống, phù hợp với câu hỏi ngắn, rõ ràng về keyword.
- **Vector Search:**
  - Truy vấn dựa trên embedding vector, phù hợp với câu hỏi dài, nhiều ngữ cảnh hoặc ý nghĩa sâu.
- **Hybrid Search:**
  - Kết hợp cả BM25 và Vector Search, có thể điều chỉnh trọng số `alpha` để cân bằng giữa hai phương pháp.
  - **Ý nghĩa alpha:**
    - `alpha` gần 1: ưu tiên kết quả BM25 (tìm kiếm keyword mạnh).
    - `alpha` gần 0: ưu tiên kết quả embedding (tìm kiếm ngữ nghĩa sâu).
    - `alpha` khoảng 0.3 – 0.7: cân bằng giữa keyword và ngữ nghĩa.
  - **Ví dụ:**
    - Nếu câu hỏi ngắn, ví dụ: "ISO 27001 là gì?" → nên tăng alpha (0.8 – 1).
    - Nếu câu hỏi dài, ví dụ: "Các quy trình kiểm soát bảo mật trong doanh nghiệp cần lưu ý gì?" → giảm alpha (0 – 0.3).
    - Nếu câu hỏi vừa có keyword vừa có ngữ cảnh, ví dụ: "Chính sách bảo mật và quy trình kiểm soát" → alpha khoảng 0.5.
---

## 6. Các thông tin cần thiết
- **Biến môi trường:**
  - Đảm bảo đã cài đặt và cấu hình các package cần thiết.
- **Cấu hình Weaviate:**
  - Đảm bảo Weaviate server đang chạy và có thể truy cập.
- **Dữ liệu:**
  - File PDF cần được đặt đúng vị trí và có TOC để tách chunk hiệu quả.

---

## 7. Flow tổng quát
1. Chuẩn bị môi trường và cài package
2. Đọc và tách dữ liệu PDF thành các chunk
3. Sinh embedding và lưu vào Weaviate
4. Thực hiện các loại truy vấn: BM25, vector, hybrid

---

## 8. Lưu ý
- Nên kiểm tra lại metadata của từng chunk để đảm bảo thông tin phân cấp chính xác.
- Có thể mở rộng workflow với các loại embedding khác hoặc các phương pháp truy vấn nâng cao.
- Batch insert giúp tối ưu hiệu năng khi lưu trữ nhiều chunk.

---
## Giới thiệu về BM25
BM25 là một thuật toán xếp hạng dựa trên xác suất, thường dùng trong các hệ thống tìm kiếm văn bản. Trong HybridRAG, BM25 được dùng để truy vấn các đoạn văn bản liên quan nhất đến câu hỏi của người dùng.

**Công thức BM25:**

Tham khảo chi tiết: [BM25 Wikipedia](https://en.wikipedia.org/wiki/Okapi_BM25)

---
## Liên hệ & đóng góp
- Tác giả: Hoàng
- Repo: https://github.com/viphoangdep/Rag_demo_paraline

---
Bạn có thể mở rộng thêm các tool hoặc tích hợp LLM khác theo nhu cầu.
## Tài liệu tham khảo
- [LlamaIndex Documentation](https://docs.llamaindex.ai/)
- [Weaviate Documentation](https://weaviate.io/developers/weaviate)
- [HuggingFace Embedding](https://huggingface.co/docs)
- [PyMuPDF Documentation](https://pymupdf.readthedocs.io/en/latest/)
