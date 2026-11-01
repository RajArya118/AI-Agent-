import json
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.models.db_models import Message, Document

class MemoryService:
    @staticmethod
    def get_conversation_history(conversation_id: str, db: Session, limit: int = 15) -> List[Dict[str, Any]]:
        """
        Retrieve recent conversation history formatted for context injection.
        """
        messages = (
            db.query(Message)
            .filter(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.desc())
            .limit(limit)
            .all()
        )
        # Reverse to chronological order
        messages.reverse()

        history = []
        for msg in messages:
            tool_calls = json.loads(msg.tool_calls) if msg.tool_calls else None
            tool_results = json.loads(msg.tool_results) if msg.tool_results else None
            history.append({
                "role": msg.role,
                "content": msg.content,
                "tool_calls": tool_calls,
                "tool_results": tool_results
            })
        return history

    @staticmethod
    def get_conversation_documents(conversation_id: str, db: Session) -> List[Dict[str, Any]]:
        """
        Retrieve document metadata attached to this conversation.
        """
        docs = db.query(Document).filter(Document.conversation_id == conversation_id).all()
        return [
            {
                "id": doc.id,
                "filename": doc.original_name,
                "file_type": doc.file_type,
                "summary": doc.summary or (doc.content_text[:300] + "..." if doc.content_text else "No content preview")
            }
            for doc in docs
        ]

    @staticmethod
    def build_system_instruction(conversation_id: str, db: Session) -> str:
        """
        Construct dynamic system instructions including role, guidelines, and document memory.
        """
        docs = MemoryService.get_conversation_documents(conversation_id, db)
        
        doc_context = ""
        if docs:
            doc_context = "\n\n### Attached Documents in this Conversation:\n"
            for d in docs:
                doc_context += f"- ID: `{d['id']}` | Name: `{d['filename']}` ({d['file_type']})\n  Preview: {d['summary']}\n"
            doc_context += "\nYou can use the `read_document` tool with the Document ID to inspect its full contents or search specific sections.\n"

        system_prompt = f"""You are a helpful, accurate, and intelligent AI Personal Assistant.
You have access to specialized tools:
1. `calculator`: For all math, arithmetic, scientific formulas, or numerical calculations. Always invoke the calculator tool to ensure precision rather than guessing arithmetic.
2. `web_search`: For real-time facts, current news, market information, technical documentation, or information you are uncertain of.
3. `read_document`: For accessing, searching, and summarizing uploaded PDF and TXT files.
4. `request_consequential_action`: Before performing irreversible, destructive, or consequential external actions (such as deleting data), use this tool to request explicit user confirmation.

Guidelines:
- Provide clear, well-structured answers using Markdown (headings, bullet points, code blocks).
- Be concise yet thorough.
- When you use a tool, explain your findings clearly to the user.{doc_context}
"""
        return system_prompt
