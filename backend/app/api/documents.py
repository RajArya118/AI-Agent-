import os
import uuid
import shutil
from pathlib import Path
from typing import List, Optional
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from sqlalchemy.orm import Session
from app.core.config import settings, UPLOAD_DIR
from app.core.database import get_db
from app.models.db_models import Document
from app.schemas.api_schemas import DocumentResponse
from app.tools.doc_reader import extract_text_from_file

router = APIRouter(prefix="/api/documents", tags=["Documents"])

ALLOWED_EXTENSIONS = {".pdf", ".txt", ".md", ".csv"}

@router.post("/upload", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    conversation_id: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file selected")

    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format '{file_ext}'. Allowed formats: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    # Secure unique filename
    unique_prefix = uuid.uuid4().hex[:10]
    safe_name = f"{unique_prefix}_{Path(file.filename).name}"
    save_path = UPLOAD_DIR / safe_name

    # Check file size while reading
    max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    total_size = 0

    try:
        with open(save_path, "wb") as buffer:
            while chunk := await file.read(1024 * 64):  # 64 KB chunks
                total_size += len(chunk)
                if total_size > max_bytes:
                    save_path.unlink(missing_ok=True)
                    raise HTTPException(
                        status_code=413,
                        detail=f"File exceeds maximum allowed size of {settings.MAX_UPLOAD_SIZE_MB}MB."
                    )
                buffer.write(chunk)
    except HTTPException:
        raise
    except Exception as e:
        save_path.unlink(missing_ok=True)
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

    # Extract text content
    extracted_text = ""
    try:
        extracted_text = extract_text_from_file(str(save_path), file_ext)
    except Exception as e:
        extracted_text = f"[Text extraction warning: {str(e)}]"

    # Generate quick summary / preview
    summary = None
    if extracted_text:
        first_lines = extracted_text.strip().split("\n")[:6]
        summary = " ".join(first_lines)[:300] + ("..." if len(extracted_text) > 300 else "")

    # Save to database
    doc = Document(
        conversation_id=conversation_id,
        filename=safe_name,
        original_name=file.filename,
        file_path=str(save_path),
        file_size=total_size,
        file_type=file_ext.replace(".", ""),
        content_text=extracted_text,
        summary=summary
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    return DocumentResponse(
        id=doc.id,
        conversation_id=doc.conversation_id,
        filename=doc.filename,
        original_name=doc.original_name,
        file_size=doc.file_size,
        file_type=doc.file_type,
        summary=doc.summary,
        created_at=doc.created_at
    )

@router.get("", response_model=List[DocumentResponse])
def list_documents(conversation_id: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Document)
    if conversation_id:
        query = query.filter(Document.conversation_id == conversation_id)
    docs = query.order_by(Document.created_at.desc()).all()
    return [
        DocumentResponse(
            id=d.id,
            conversation_id=d.conversation_id,
            filename=d.filename,
            original_name=d.original_name,
            file_size=d.file_size,
            file_type=d.file_type,
            summary=d.summary,
            created_at=d.created_at
        )
        for d in docs
    ]

@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(document_id: str, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    try:
        Path(doc.file_path).unlink(missing_ok=True)
    except Exception:
        pass
    db.delete(doc)
    db.commit()
    return None
