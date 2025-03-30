# database.py
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv
import os
from backend_app.core import embeddings
from backend_app.models import schemas
from backend_app.main import app

load_dotenv()
# openai_embed = embedding_functions.OpenAIEmbeddingFunction(
#     api_key=os.getenv("OPENAI_API_KEY"),
#     model_name="text-embedding-3-small"
# )

# Use BGE-small model for embeddings
embedding_function = embeddings.BGEEmbeddingFunction()

chroma_client = chromadb.HttpClient(host="chroma", port=8000)

students_collection = chroma_client.get_or_create_collection(
    name="students",
    embedding_function=embedding_function
)

jobs_collection = chroma_client.get_or_create_collection(
    name="jobs",
    embedding_function=embedding_function
)

#upsert = add or update (update  ake replace if uuid already exists)
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