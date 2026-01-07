from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import uuid

from app.services.pdf_service import extract_text_from_pdf
from app.services.ai_service import summarize_text
from app.services.document_service import save_document

router = APIRouter()

ALLOWED_TYPES = {
    "application/pdf",
    "image/png",
    "image/jpeg"
}

MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", 10 * 1024 * 1024))
UPLOAD_DIR = os.getenv("UPLOAD_FOLDER", "uploads")

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # 1️⃣ Validate file type
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, PNG, JPG files are allowed"
        )

    # 2️⃣ Read file
    contents = await file.read()

    # 3️⃣ Validate file size
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File size exceeds allowed limit"
        )

    # 4️⃣ Save file
    ext = file.filename.split(".")[-1]
    safe_name = f"{uuid.uuid4()}.{ext}"
    file_path = os.path.join(UPLOAD_DIR, safe_name)

    try:
        with open(file_path, "wb") as f:
            f.write(contents)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"File save failed: {str(e)}"
        )

    # 5️⃣ Extract text (PDF only)
    extracted_text = None
    try:
        if file.content_type == "application/pdf":
            extracted_text = extract_text_from_pdf(file_path)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"PDF extraction failed: {str(e)}"
        )

    # 6️⃣ AI Summarization
    summary = None
    try:
        if extracted_text:
            summary = summarize_text(extracted_text)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"AI summarization failed: {str(e)}"
        )

    # 7️⃣ Prepare MongoDB document
    document_data = {
        "original_filename": file.filename,
        "saved_filename": safe_name,
        "content_type": file.content_type,
        "file_path": file_path,
        "file_size": len(contents),
        "text_length": len(extracted_text) if extracted_text else 0,
        "extracted_text": extracted_text,
        "summary": summary
    }

    # 8️⃣ Save to MongoDB
    try:
        document_id = save_document(document_data)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database save failed: {str(e)}"
        )

    # 9️⃣ Response
    return {
        "status": "success",
        "document_id": document_id,
        "original_filename": file.filename,
        "saved_filename": safe_name,
        "content_type": file.content_type,
        "file_size": len(contents),
        "text_length": len(extracted_text) if extracted_text else 0,
        "extracted_text_preview": extracted_text[:500] if extracted_text else None,
        "summary": summary
    }
