from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os
load_dotenv()

class OpenAIEmbedding:
    def __init__(self, model: str = "text-embedding-3-small", chunk_size: int = 1):
        self.API_KEY = os.getenv("OPENAI_API_KEY")
        self.model = model
        self.chunk_size = chunk_size
        self.embeddings = OpenAIEmbeddings(model=self.model, chunk_size=self.chunk_size,api_key=self.API_KEY)

    def embed_documents(self, texts):
        return self.embeddings.embed_documents(texts)

    def embed_query(self, text):
        return self.embeddings.embed_query(text)
    
if __name__ == "__main__":
    embedding = OpenAIEmbedding()
    texts = ["Hello, world!", "OpenAI is great."]
    print(embedding.embed_documents(texts))
    print(embedding.embed_query("Hello!"))