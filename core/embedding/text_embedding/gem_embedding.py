from google import genai
from dotenv import load_dotenv
import os
load_dotenv()

GEMMINI_API_KEY = os.getenv("GEMMINI_API_KEY")

client = genai.Client(api_key=GEMMINI_API_KEY)

result = client.models.embed_content(
        model="gemini-embedding-001",
        contents= [
            "What is the meaning of life?",
            "What is the purpose of existence?",
            "How do I bake a cake?"
        ])

for embedding in result.embeddings:
    print(embedding)