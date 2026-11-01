import json
from typing import Dict, Any
from sqlalchemy.orm import Session
from app.models.db_models import PendingAction

def request_consequential_action(
    action_type: str,
    description: str,
    payload: Dict[str, Any],
    conversation_id: str,
    db_session: Session
) -> Dict[str, Any]:
    """
    Register a consequential action that pauses agent execution and waits for explicit user confirmation.
    """
    action = PendingAction(
        conversation_id=conversation_id,
        action_type=action_type,
        description=description,
        payload=json.dumps(payload),
        status="pending"
    )
    db_session.add(action)
    db_session.commit()
    db_session.refresh(action)

    return {
        "status": "requires_confirmation",
        "action_id": action.id,
        "action_type": action_type,
        "description": description,
        "message": f"Security Confirmation Required: {description}. Please confirm or reject this action to proceed."
    }

def execute_confirmed_action(action: PendingAction, approved: bool, db_session: Session) -> Dict[str, Any]:
    """
    Execute or discard the confirmed action once approved by the user.
    """
    if not approved:
        action.status = "rejected"
        db_session.commit()
        return {
            "status": "rejected",
            "message": f"Action '{action.action_type}' was declined by the user."
        }

    action.status = "approved"
    db_session.commit()
    
    payload = json.loads(action.payload)
    
    # Handle action implementations
    if action.action_type == "delete_all_messages":
        from app.models.db_models import Message
        db_session.query(Message).filter(Message.conversation_id == action.conversation_id).delete()
        db_session.commit()
        return {"status": "executed", "message": "All messages in this conversation have been cleared."}
    
    elif action.action_type == "delete_document":
        from app.models.db_models import Document
        doc_id = payload.get("document_id")
        doc = db_session.query(Document).filter(Document.id == doc_id).first()
        if doc:
            db_session.delete(doc)
            db_session.commit()
            return {"status": "executed", "message": f"Document '{doc.original_name}' has been deleted."}
        return {"status": "error", "message": "Document not found."}

    return {"status": "executed", "message": f"Action '{action.action_type}' was approved and executed successfully."}
