import voyageai
import PIL 
from dotenv import load_dotenv
import os
load_dotenv()
import numpy as np

VOYAGE_API_KEY = os.getenv("VOYAGE_API_KEY")

vo = voyageai.Client(api_key=VOYAGE_API_KEY)

inputs = [
    ["This is a banana.", PIL.Image.open('/home/quang/My_Project/Paraline/paraline/core/embedding/multimodal_embedding/img/banana.jpeg')]
]

# Vectorize inputs
result = vo.multimodal_embed(inputs, model="voyage-multimodal-3")
# search
query = list()
query.append(["This is a apple."])
query_result = vo.multimodal_embed(query, model="voyage-multimodal-3")

result_cosin = np.dot(result.embeddings, query_result.embeddings)
print(result_cosin)