from llama_cloud_services import LlamaParse
from pathlib import Path

from dotenv import load_dotenv
import os
load_dotenv()

Llma_API_KEY = os.getenv("Llama_API_KEY")
output_path = "/home/quang/My_Project/Paraline/paraline/core/document_parsing/Evalution_matrix/test_LlamaPaser"
parser = LlamaParse(
  # See how to get your API key at https://docs.cloud.llamaindex.ai/api_key
  api_key=Llma_API_KEY,
  num_workers=19,       # if multiple files passed, split in `num_workers` API calls
  verbose=True,
  language="en", 
)
result = parser.parse("/home/quang/My_Project/Paraline/paraline/core/document_parsing/Evalution_matrix/document/2506.02153v1-table.pdf")
markdown_documents = result.get_markdown()
output_dir = Path(output_path)
output_dir.mkdir(parents=True, exist_ok=True)
if len(markdown_documents) > 0:
    if isinstance(markdown_documents[0], str):
        all_md = "\n\n".join(markdown_documents)
    else:
        all_md = "\n\n".join([doc.text for doc in markdown_documents])
    md_filename = output_dir / f"test_table_LlamaParse.md"
    with open(md_filename, "w", encoding="utf-8") as f:
        f.write(all_md)

print("Done")