# Multimodal RAG
## Tổng quan

Cũng giống như Retrieval Augmented Generation (RAG) tuy nhiên khi đối mặt với vấn đề trong tài liệu còn nhiều kiểu dữ liệu không chỉ riêng text có thể là ảnh, bảng, biểu đồ,... thì lại không thể triển khai được bằng Simple RAG từ đó kỹ thuật Multimodal Retrieval Augmented Generation (RAG) ra đời. Một hệ thống Multimodal Retrieval Augmented Generation (RAG) có khả năng xử lý cả văn bản và hình ảnh từ tài liệu PDF. Hệ thống kết hợp sức mạnh của nhiều mô hình AI để cung cấp câu trả lời chính xác cho các truy vấn về nội dung tài liệu.

<img width="1999" height="734" alt="image" src="https://github.com/user-attachments/assets/bd5da1fe-b04e-4b8e-b01f-8f3f65dea5cb" />

## Các bước thực hiện

1. **Create Vector Database:** Đầu tiên, toàn bộ dữ liệu tri thức được xử lý để tạo vector database. Với tài liệu chứa text và hình ảnh, text được chia thành các chunk nhỏ theo phương pháp Context-Aware Chunking nhằm giữ ngữ cảnh, còn hình ảnh được trích xuất và sinh caption bằng mô hình VLM (Visual Language Model). Sau đó, caption được gắn vào chunk text phù hợp dựa trên vị trí, trang hoặc semantic similarity. Mỗi chunk text + caption sau đó được chuyển đổi thành vector embeddings bằng mô hình embedding và lưu trữ vào vector database như FAISS, Chroma hoặc Pinecone.
2. **User Input:** Người dùng cung cấp một câu truy vấn (query) bằng ngôn ngữ tự nhiên. Query này có thể chỉ là text, hoặc có thể bao gồm hình ảnh nếu muốn tìm kiếm dựa trên dữ liệu đa phương tiện.
3. **Information Retrieval:** Cơ chế retrieval quét toàn bộ vector trong database để xác định các chunk (paragraphs) có ngữ nghĩa tương đồng với câu truy vấn. Với Multimodal RAG, retrieval có thể dựa trên text embedding, image embedding hoặc kết hợp cả hai. Những chunk này sau đó được lấy để bổ sung context cho quá trình sinh câu trả lời bởi LLM.
4. **Combining Data:** Các chunk text + caption được lấy từ database được kết hợp với câu truy vấn của user để tạo thành một prompt duy nhất. Prompt này giữ nguyên ngữ cảnh đầy đủ giữa text và hình ảnh, đảm bảo LLM có thể hiểu mối liên hệ giữa các phần dữ liệu đa phương tiện.
5. **Generate Text:** Prompt đã được bổ sung context được đưa qua LLM để sinh câu trả lời cuối cùng. LLM sử dụng thông tin text và hình ảnh trong các chunk để tạo ra phản hồi chính xác, có ngữ cảnh, đáp ứng đầy đủ yêu cầu của người dùng.

## Ưu điểm 

- Hiểu ngữ cảnh đa phương tiện: Multimodal RAG không chỉ dựa vào text mà còn khai thác thông tin từ hình ảnh thông qua caption hoặc embedding, giúp LLM hiểu mối quan hệ giữa text và hình ảnh.
- Cải thiện độ chính xác của retrieval: Việc kết hợp text và caption làm vector embeddings giàu thông tin hơn, giúp tìm kiếm các chunk phù hợp với query chính xác hơn.
- Giữ ngữ cảnh trong document dài: Sử dụng Context-Aware Chunking giúp giữ mạch logic khi chia nhỏ text, tránh mất thông tin quan trọng khi query.
- Mở rộng dễ dàng: Có thể thêm nhiều loại dữ liệu khác (video, audio, bảng biểu) bằng cách sinh embedding phù hợp và gắn vào chunk text, mà không thay đổi toàn bộ pipeline.

## Nhược điểm:

- Chi phí tính toán cao: Việc trích xuất ảnh, sinh caption bằng VLM, tạo embedding và lưu vào vector database tốn nhiều tài nguyên, đặc biệt với document lớn.
- Xử lý ngữ cảnh hình ảnh phức tạp: Nếu ảnh không có caption tốt hoặc vị trí ảnh khó xác định, việc gắn caption vào text có thể sai ngữ cảnh, làm giảm chất lượng retrieval.
- Phụ thuộc vào chất lượng mô hình: Hiệu quả phụ thuộc vào độ chính xác của VLM để sinh caption và mô hình embedding để đo semantic similarity.
- Quản lý dữ liệu phức tạp: Multimodal RAG yêu cầu quản lý nhiều loại dữ liệu (text, image, embedding, caption), cần thiết kế pipeline cẩn thận để tránh lỗi hoặc mất thông tin.

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
