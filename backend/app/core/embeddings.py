# embeddings.py
import os
from sentence_transformers import SentenceTransformer

# Define a path to store/download the model manually
MODEL_PATH = os.getenv("EMBEDDING_MODEL_PATH", "models/bge-small")
# Load model (will load from local folder if exists)
model = SentenceTransformer(MODEL_PATH)

def get_embedding(texts: list[str]) -> list[list[float]]:
    if isinstance(texts, str):
        texts = [texts]
    return model.encode(texts, normalize_embeddings=True).tolist()
