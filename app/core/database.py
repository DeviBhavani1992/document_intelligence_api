from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("MONGO_DB_NAME", "document_db")

client = MongoClient(MONGO_URI)

# ✅ THIS is what was missing
db = client[DB_NAME]
test_collection = db.test_collection

result = test_collection.insert_one({
    "name": "Test User",
    "status": "MongoDB connected"
})

print("Inserted ID:", result.inserted_id)
