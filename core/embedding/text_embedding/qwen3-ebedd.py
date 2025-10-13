from sentence_transformers import SentenceTransformer

# Load the model
model = SentenceTransformer("Qwen/Qwen3-Embedding-0.6B")

queries = [
    "What is the capital of China?",
]
documents = [
    "The capital of China is Beijing.",
    "Gravity is a force that attracts two bodies towards each other. It gives weight to physical objects and is responsible for the movement of planets around the sun.",
]


query_embeddings = model.encode(queries, prompt_name="query")
document_embeddings = model.encode(documents)
print("Query Embeddings:", query_embeddings)
print("Document Embeddings:", document_embeddings)
# Compute the (cosine) similarity between the query and document embeddings
similarity = model.similarity(query_embeddings, document_embeddings)
print(similarity)
