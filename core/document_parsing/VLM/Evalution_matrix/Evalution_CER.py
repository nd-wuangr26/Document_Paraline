import Levenshtein

def cer(ref: str, hyp: str) -> float:
    """
    Tính CER (Character Error Rate)
    ref: ground truth
    hyp: kết quả extract từ Docling hoặc LlamaParse
    """
    # Tính khoảng cách Levenshtein (edit distance)
    distance = Levenshtein.distance(ref, hyp)
    return distance / len(ref) if len(ref) > 0 else 0.0

def read_markdown(path: str) -> str:
    """Đọc toàn bộ nội dung từ file markdown và trả về chuỗi"""
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()

ground_truth = read_markdown("/home/quang/My_Project/Paraline/paraline/core/document_parsing/Evalution_matrix/ground_truth/Ground_truth.md")
docling_text = read_markdown("/home/quang/My_Project/Paraline/paraline/core/document_parsing/Evalution_matrix/test_Docling/test_text_docling.md")
llamaparse_text = read_markdown("/home/quang/My_Project/Paraline/paraline/core/document_parsing/Evalution_matrix/test_LlamaPaser/test_text_LlamaParser.md")

cer_docling = cer(ground_truth, docling_text)
cer_llamaparse = cer(ground_truth, llamaparse_text)

print(f"CER Docling    : {cer_docling:.4f}")
print(f"CER LlamaParse : {cer_llamaparse:.4f}")

