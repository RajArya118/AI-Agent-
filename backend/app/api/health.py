from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db
from app.core.mongodb import mongo_store
from app.models.db_models import Conversation, Document
from app.schemas.api_schemas import HealthResponse

router = APIRouter(prefix="/api/health", tags=["Health"])

@router.get("", response_model=HealthResponse)
def get_health(db: Session = Depends(get_db)):
    conv_count = db.query(Conversation).count()
    doc_count = db.query(Document).count()
    projects = mongo_store.list_projects()
    
    return HealthResponse(
        status="healthy",
        gemini_configured=settings.is_gemini_configured,
        gemini_model=settings.GEMINI_MODEL,
        duckduckgo_search=True,
        calculator=True,
        document_reader=True,
        active_conversations_count=conv_count,
        uploaded_documents_count=doc_count,
        specialist_agents_active=7,
        mongodb_connected=mongo_store.is_connected,
        generated_projects_count=len(projects)
    )
