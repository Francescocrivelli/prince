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

#query best match for 1 student profile
def query_best_match(student_profile: str, n_results=1):
    return students_collection.query(
        query_texts=[student_profile],
        n_results=n_results
    )



#create a that updates the user profile in chroma without deleting the existing profile
def update_user_profile_by_id(user_id: str, user_profile: schemas.UserProfile):
    students_collection.update(
        ids=[user_id],
        documents=[user_profile.model_dump_json()],
        metadatas=[user_profile.model_dump()]
    )


#get student profile from chroma
def get_student_profile(user_id: str):
    #returns looks like this:
    # {
    #     "ids": ["1234567890"],
    #     "documents": ["user profile"],
    #     "metadatas": [{"user_id": "1234567890"}]
    # }
    return students_collection.get(
        ids=[user_id]
    )

#get stundet profile from chroma based on one metadata field
def get_student_profile_by_metadata(metadata_field: str, metadata_value: str):
    #returns looks like this:
    # {
    #     "ids": ["1234567890"],
    #     "documents": ["user profile"],
    #     "metadatas": [{"user_id": "1234567890"}]
    # }
    return students_collection.get(
        where={metadata_field: metadata_value}
    )

#get student profile by phone number
def get_student_by_phone(phone_number: str):
    return students_collection.get(
        where={"user_id": phone_number}
    )

#create new student entry with phone number
def create_student_with_phone(phone_number: str, full_name: str = None):
    metadata = {
        "user_id": phone_number,
        "full_name": full_name
    }
    students_collection.upsert(
        ids=[phone_number],
        documents=[str(metadata)],  # Initial empty document
        metadatas=[metadata]
    )
    return metadata

#find closest matching student by name query
def find_student_by_name_query(name_query: str, n_results: int = 1):
    results = students_collection.query(
        query_texts=[name_query],
        n_results=n_results,
        where={"full_name": {"$ne": None}}  # Only search where full_name exists
    )
    return results

#update conversation history in document
def update_conversation_history(phone_number: str, conversation_text: str):
    existing = get_student_by_phone(phone_number)
    if existing and existing['documents']:
        # Append new conversation to existing document
        current_doc = existing['documents'][0]
        updated_doc = current_doc + "\n--- New Conversation ---\n" + conversation_text
    else:
        updated_doc = conversation_text
    
    students_collection.upsert(
        ids=[phone_number],
        documents=[updated_doc],
        metadatas=[existing['metadatas'][0]] if existing and existing['metadatas'] else [{"user_id": phone_number}]
    )




