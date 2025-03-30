# database.py
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv
import os
from app.core import embeddings

load_dotenv()
# openai_embed = embedding_functions.OpenAIEmbeddingFunction(
#     api_key=os.getenv("OPENAI_API_KEY"),
#     model_name="text-embedding-3-small"
# )

# Use BGE-small model for embeddings
embedding_function = embeddings.get_embedding

chroma_client = chromadb.HttpClient(host="chroma", port=8001)

students_collection = chroma_client.get_or_create_collection(
    name="students",
    embedding_function=embedding_function
)

jobs_collection = chroma_client.get_or_create_collection(
    name="jobs",
    embedding_function=embedding_function
)

#upsert = add or update
def upsert_student(student_id: str, document: str, metadata: dict):
    students_collection.upsert(
        ids=[student_id],
        documents=[document],
        metadatas=[metadata]
    )

#query = search
def query_jobs(student_profile: str, n_results=5):
    return jobs_collection.query(
        query_texts=[student_profile],
        n_results=n_results
    )