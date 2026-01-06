from datetime import datetime
from app.core.database import db

collection = db.documents


def save_document(data: dict) -> str:
    data["created_at"] = datetime.utcnow()
    result = collection.insert_one(data)
    return str(result.inserted_id)
