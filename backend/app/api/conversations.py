import json
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.db_models import Conversation, Message
from app.schemas.api_schemas import (
    ConversationResponse,
    ConversationListItem,
    ConversationCreate,
    MessageResponse,
    ToolCallInfo,
    ToolResultInfo
)

router = APIRouter(prefix="/api/conversations", tags=["Conversations"])

def _format_message(msg: Message) -> MessageResponse:
    tool_calls = json.loads(msg.tool_calls) if msg.tool_calls else None
    tool_results = json.loads(msg.tool_results) if msg.tool_results else None
    return MessageResponse(
        id=msg.id,
        conversation_id=msg.conversation_id,
        role=msg.role,
        content=msg.content,
        tool_calls=[ToolCallInfo(**tc) for tc in tool_calls] if tool_calls else None,
        tool_results=[ToolResultInfo(**tr) for tr in tool_results] if tool_results else None,
        status=msg.status,
        created_at=msg.created_at
    )

@router.get("", response_model=List[ConversationListItem])
def list_conversations(db: Session = Depends(get_db)):
    conversations = db.query(Conversation).order_by(Conversation.updated_at.desc()).all()
    result = []
    for conv in conversations:
        count = len(conv.messages)
        last_msg = conv.messages[-1].content if count > 0 else None
        if last_msg and len(last_msg) > 60:
            last_msg = last_msg[:60] + "..."
        result.append(
            ConversationListItem(
                id=conv.id,
                title=conv.title,
                created_at=conv.created_at,
                updated_at=conv.updated_at,
                message_count=count,
                last_message=last_msg
            )
        )
    return result

@router.post("", response_model=ConversationResponse, status_code=status.HTTP_201_CREATED)
def create_conversation(payload: ConversationCreate, db: Session = Depends(get_db)):
    conv = Conversation(title=payload.title or "New Chat")
    db.add(conv)
    db.commit()
    db.refresh(conv)
    return ConversationResponse(
        id=conv.id,
        title=conv.title,
        created_at=conv.created_at,
        updated_at=conv.updated_at,
        messages=[]
    )

@router.get("/{conversation_id}", response_model=ConversationResponse)
def get_conversation(conversation_id: str, db: Session = Depends(get_db)):
    conv = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")

    formatted_messages = [_format_message(m) for m in conv.messages]
    return ConversationResponse(
        id=conv.id,
        title=conv.title,
        created_at=conv.created_at,
        updated_at=conv.updated_at,
        messages=formatted_messages
    )

@router.delete("/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_conversation(conversation_id: str, db: Session = Depends(get_db)):
    conv = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    db.delete(conv)
    db.commit()
    return None
