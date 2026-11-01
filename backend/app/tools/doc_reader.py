import os
from pathlib import Path
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
import pypdf

def extract_text_from_file(file_path: str, file_type: str) -> str:
    """Extract plain text from PDF or TXT files."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    ext = file_type.lower().replace(".", "")
    if ext == "pdf":
        text_parts = []
        reader = pypdf.PdfReader(str(path))
        for page_num, page in enumerate(reader.pages):
            page_text = page.extract_text() or ""
            if page_text.strip():
                text_parts.append(f"--- Page {page_num + 1} ---\n{page_text}")
        return "\n\n".join(text_parts)
    elif ext in ("txt", "md", "csv", "json"):
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    else:
        raise ValueError(f"Unsupported file type: {ext}")

def read_document_content(
    document_id: str,
    db_session: Session,
    query: Optional[str] = None,
    max_length: int = 4000
) -> Dict[str, Any]:
    """
    Retrieve document text from SQLite. If query is provided, returns relevant excerpts.
    """
    from app.models.db_models import Document
    doc = db_session.query(Document).filter(Document.id == document_id).first()
    if not doc:
        return {"status": "error", "error": f"Document ID '{document_id}' not found."}

    content = doc.content_text or ""
    if not content:
        try:
            content = extract_text_from_file(doc.file_path, doc.file_type)
            doc.content_text = content
            db_session.commit()
        except Exception as e:
            return {"status": "error", "error": f"Failed reading file content: {str(e)}"}

    if query:
        # Search for query keywords in document content
        keywords = query.lower().split()
        paragraphs = content.split("\n\n")
        matching = []
        for p in paragraphs:
            p_lower = p.lower()
            if any(k in p_lower for k in keywords):
                matching.append(p.strip())

        if matching:
            excerpt = "\n\n...\n\n".join(matching[:5])
            if len(excerpt) > max_length:
                excerpt = excerpt[:max_length] + " ...[truncated]"
            return {
                "status": "success",
                "document_id": doc.id,
                "document_name": doc.original_name,
                "match_type": "query_excerpts",
                "content": excerpt
            }

    # Return full or truncated content
    truncated = False
    if len(content) > max_length:
        content = content[:max_length] + " ...[truncated]"
        truncated = True

    return {
        "status": "success",
        "document_id": doc.id,
        "document_name": doc.original_name,
        "match_type": "full_content",
        "truncated": truncated,
        "content": content
    }
