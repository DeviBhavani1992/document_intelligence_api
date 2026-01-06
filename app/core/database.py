from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("MONGO_DB_NAME", "document_db")

client = MongoClient(MONGO_URI)

# ✅ THIS is what was missing
db = client[DB_NAME]
