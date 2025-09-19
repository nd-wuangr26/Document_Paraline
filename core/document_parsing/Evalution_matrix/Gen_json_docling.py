from docling.document_converter import DocumentConverter
from pathlib import Path
from docling_core.types.doc.document import ImageRefMode

source = "/home/quang/My_Project/Paraline/paraline/core/document_parsing/Evalution_matrix/document/2506.02153v1-table.pdf"
converter = DocumentConverter()
doc = converter.convert(source).document
doc.save_as_json("/home/quang/My_Project/Paraline/paraline/core/document_parsing/Evalution_matrix/test_table_docling_ht.md", image_mode=ImageRefMode.REFERENCED)

