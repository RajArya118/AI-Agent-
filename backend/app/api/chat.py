from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.api_schemas import (
    MessageCreate,
    MessageResponse,
    ActionConfirmationRequest,
    ToolCallInfo,
    ToolResultInfo
)
from app.services.agent_service import AgentService
import json

router = APIRouter(prefix="/api/conversations", tags=["Chat"])

@router.post("/{conversation_id}/messages", response_model=MessageResponse)
async def send_message(
    conversation_id: str,
    payload: MessageCreate,
    db: Session = Depends(get_db)
):
    if not payload.content.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message content cannot be empty."
        )

    try:
        assistant_msg = await AgentService.process_user_turn(
            conversation_id=conversation_id,
            user_text=payload.content,
            document_ids=payload.document_ids,
            db=db
        )

        tool_calls = json.loads(assistant_msg.tool_calls) if assistant_msg.tool_calls else None
        tool_results = json.loads(assistant_msg.tool_results) if assistant_msg.tool_results else None

        return MessageResponse(
            id=assistant_msg.id,
            conversation_id=assistant_msg.conversation_id,
            role=assistant_msg.role,
            content=assistant_msg.content,
            tool_calls=[ToolCallInfo(**tc) for tc in tool_calls] if tool_calls else None,
            tool_results=[ToolResultInfo(**tr) for tr in tool_results] if tool_results else None,
            status=assistant_msg.status,
            created_at=assistant_msg.created_at
        )

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error executing agent turn: {str(e)}"
        )

@router.post("/{conversation_id}/action-confirmation")
def confirm_action(
    conversation_id: str,
    payload: ActionConfirmationRequest,
    db: Session = Depends(get_db)
):
    res = AgentService.handle_action_confirmation(
        action_id=payload.action_id,
        approved=payload.approved,
        db=db
    )
    if res.get("status") == "error":
        raise HTTPException(status_code=404, detail=res.get("message"))
    return res
