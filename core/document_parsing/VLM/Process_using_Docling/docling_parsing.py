import os
from pathlib import Path
from docling.document_converter import DocumentConverter

doc_dir = "/home/quang/My_Project/Paraline/paraline/document/Huong-dan-doc-va-phan-tich-BCTC-NHANH.pdf"

source = Path(doc_dir)
converter = DocumentConverter()
doc = converter.convert(source).document
print(doc.export_to_markdown())

