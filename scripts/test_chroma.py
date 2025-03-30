# scripts/test_chroma_student.py

from app.core import database

# Use a fixed fake student ID
STUDENT_ID = "test-student-001"

# Fake profile data
document = "I'm a computer science student at Stanford focused on LLMs and robotics."
metadata = {
    "name": "Test User",
    "school": "Stanford",
    "grad_year": 2025,
    "skills": ["LLMs", "robotics"],
    "interested_in": "early-stage AI startups"
}

print("👉 Upserting test student into Chroma...")
database.upsert_student(STUDENT_ID, document, metadata)

print("✅ Upsert complete.")

print("\n🔍 Fetching student back by ID...")
result = database.students_collection.get(ids=[STUDENT_ID])

print("\n✅ Found student:")
print("ID:", result["ids"][0])
print("Document:", result["documents"][0])
print("Metadata:", result["metadatas"][0])