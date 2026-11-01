from datetime import datetime
from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field, ConfigDict

class ToolCallInfo(BaseModel):
    id: Optional[str] = None
    name: str
    arguments: Dict[str, Any] = Field(default_factory=dict)

class ToolResultInfo(BaseModel):
    call_id: Optional[str] = None
    name: str
    status: str = "success"
    result: Any
    display_title: Optional[str] = None
    execution_time_ms: Optional[float] = None

class MessageBase(BaseModel):
    role: str
    content: str

class MessageCreate(BaseModel):
    content: str
    document_ids: Optional[List[str]] = Field(default_factory=list)

class MessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    conversation_id: str
    role: str
    content: str
    tool_calls: Optional[List[ToolCallInfo]] = None
    tool_results: Optional[List[ToolResultInfo]] = None
    status: str
    created_at: datetime

class ConversationCreate(BaseModel):
    title: Optional[str] = "New Chat"

class ConversationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    created_at: datetime
    updated_at: datetime
    messages: List[MessageResponse] = Field(default_factory=list)

class ConversationListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    created_at: datetime
    updated_at: datetime
    message_count: int = 0
    last_message: Optional[str] = None

class DocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    conversation_id: Optional[str] = None
    filename: str
    original_name: str
    file_size: int
    file_type: str
    summary: Optional[str] = None
    created_at: datetime

class ActionConfirmationRequest(BaseModel):
    action_id: str
    approved: bool

class PendingActionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    conversation_id: str
    action_type: str
    description: str
    payload: Dict[str, Any]
    status: str
    created_at: datetime

class HealthResponse(BaseModel):
    status: str
    gemini_configured: bool
    gemini_model: str
    duckduckgo_search: bool
    calculator: bool
    document_reader: bool
    active_conversations_count: int
    uploaded_documents_count: int
    specialist_agents_active: int = 7
    mongodb_connected: bool = False
    generated_projects_count: int = 0
