from llama_cloud_services import LlamaParse
from dotenv import load_dotenv
import os
load_dotenv()

Llma_API_KEY = os.getenv("Llama_API_KEY")

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
)



# Example usage:

# sync
result = parser.parse("/home/quang/My_Project/Paraline/paraline/document/Huong-dan-doc-va-phan-tich-BCTC-NHANH.pdf")


# get the llama-index markdown documents
markdown_documents = result.get_markdown_documents(split_by_page=True)

# get the llama-index text documents
text_documents = result.get_text_documents(split_by_page=False)

# get the image documents
image_documents = result.get_image_documents(
    include_screenshot_images=True,
    include_object_images=False,
    # Optional: download the images to a directory
    # (default is to return the image bytes in ImageDocument objects)
    image_download_dir="./images",
)

# access the raw job result
# Items will vary based on the parser configuration
for page in result.pages:
    print(page.text)
    print(page.md)
    print(page.images)
    print(page.layout)
    print(page.structuredData)