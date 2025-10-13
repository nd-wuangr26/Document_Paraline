from llama_cloud_services import LlamaParse
from dotenv import load_dotenv
from pathlib import Path

import os
load_dotenv()

Llma_API_KEY = os.getenv("Llama_API_KEY")
class LlamaParseDocument:
    
    def parse(self, file_path:str):
        parser = LlamaParse(
        # See how to get your API key at https://docs.cloud.llamaindex.ai/api_key
        api_key=Llma_API_KEY,

        # The parsing mode
        parse_mode="parse_page_with_agent",

        # The model to use
        model="openai-gpt-4-1-mini",

        # Whether to use high resolution OCR (Slow)
        high_res_ocr=True,

        # Adaptive long table. LlamaParse will try to detect long table and adapt the output
        adaptive_long_table=True,

        # Whether to try to extract outlined tables
        outlined_table_extraction=True,

        # Whether to output tables as HTML in the markdown output
        output_tables_as_HTML=True,
        
        language="en"
        )
        return parser.parse(file_path)

    def export_function_md_with_image_ref(conv_res, output_path:str, input_file_path:str, replace_blank:str="_"):
        output_dir = Path(output_path)
        output_dir.mkdir(parents=True, exist_ok=True)
        doc_filename = Path(input_file_path).stem.replace(" ", replace_blank)

        # Lấy danh sách markdown documents và nối lại thành 1 chuỗi
        markdown_documents = conv_res.get_markdown_documents(split_by_page=True)
        if len(markdown_documents) > 0:
            if isinstance(markdown_documents[0], str):
                all_md = "\n\n".join(markdown_documents)
            else:
                all_md = "\n\n".join([doc.text for doc in markdown_documents])
            md_filename = output_dir / f"{doc_filename}-with-image-refs.md"
            with open(md_filename, "w", encoding="utf-8") as f:
                f.write(all_md)
            
if __name__ == "__main__":
    parser = LlamaParseDocument.parse()
    result = parser("/home/quang/My_Project/Paraline/paraline/core/document_parsing/Evalution_matrix/document/2506.02153v1-trang.pdf")
    markdown_documents = result.get_markdown_documents(split_by_page=True)
