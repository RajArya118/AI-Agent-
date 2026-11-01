import time
import json
import re
import logging
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from app.models.db_models import Conversation, Message, Document, PendingAction
from app.schemas.api_schemas import ToolCallInfo, ToolResultInfo
from app.services.memory_service import MemoryService
from app.services.gemini_service import gemini_service
from app.tools import registry
from app.tools.calculator import safe_calculate
from app.tools.web_search import search_web
from app.tools.doc_reader import read_document_content
from app.tools.action_tool import request_consequential_action, execute_confirmed_action

logger = logging.getLogger(__name__)

class AgentService:
    @staticmethod
    async def process_user_turn(
        conversation_id: str,
        user_text: str,
        document_ids: Optional[List[str]],
        db: Session
    ) -> Message:
        """
        Orchestrate the full multi-step agent execution turn.
        """
        # 1. Fetch conversation
        conv = db.query(Conversation).filter(Conversation.id == conversation_id).first()
        if not conv:
            raise ValueError(f"Conversation {conversation_id} not found.")

        # Associate any newly attached documents with this conversation
        if document_ids:
            for doc_id in document_ids:
                doc = db.query(Document).filter(Document.id == doc_id).first()
                if doc and not doc.conversation_id:
                    doc.conversation_id = conversation_id
            db.commit()

        # Update conversation title if default
        if conv.title == "New Chat":
            title_text = user_text.strip().replace("\n", " ")
            if len(title_text) > 35:
                title_text = title_text[:35] + "..."
            conv.title = title_text or "New Chat"
            db.commit()

        # 2. Persist user message
        user_message = Message(
            conversation_id=conversation_id,
            role="user",
            content=user_text,
            status="completed"
        )
        db.add(user_message)
        db.commit()

        # 3. Retrieve context & memory
        history = MemoryService.get_conversation_history(conversation_id, db, limit=12)
        # Exclude the user message just added so we pass history cleanly
        if history and history[-1]["role"] == "user":
            history = history[:-1]

        system_instruction = MemoryService.build_system_instruction(conversation_id, db)
        tools = registry.list_tools()

        tool_calls_data: List[Dict[str, Any]] = []
        tool_results_data: List[Dict[str, Any]] = []
        assistant_content = ""
        final_status = "completed"

        # 4. Check if Gemini API is available
        if gemini_service.is_available():
            try:
                gemini_turn = await gemini_service.call_gemini(
                    prompt=user_text,
                    system_instruction=system_instruction,
                    history=history,
                    tools=tools
                )

                if gemini_turn.get("tool_calls"):
                    for tc in gemini_turn["tool_calls"]:
                        tool_name = tc["name"]
                        tool_args = tc.get("arguments", {})
                        call_id = tc.get("id", tool_name)
                        tool_calls_data.append({
                            "id": call_id,
                            "name": tool_name,
                            "arguments": tool_args
                        })

                        # Execute tool
                        start_time = time.perf_counter()
                        tool_res = None
                        status = "success"

                        if tool_name == "calculator":
                            expr = tool_args.get("expression", "")
                            tool_res = safe_calculate(expr)
                        elif tool_name == "web_search":
                            q = tool_args.get("query", "")
                            max_res = int(tool_args.get("max_results", 5))
                            tool_res = search_web(q, max_results=max_res)
                        elif tool_name == "read_document":
                            doc_id = tool_args.get("document_id")
                            q = tool_args.get("query")
                            tool_res = read_document_content(doc_id, db, query=q)
                        elif tool_name == "request_consequential_action":
                            act_type = tool_args.get("action_type", "unspecified")
                            desc = tool_args.get("description", "Requires confirmation")
                            payload = tool_args.get("payload", {})
                            tool_res = request_consequential_action(act_type, desc, payload, conversation_id, db)
                            status = "requires_confirmation"
                            final_status = "pending_confirmation"
                        else:
                            tool_res = {"status": "error", "error": f"Unknown tool: {tool_name}"}
                            status = "error"

                        elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)
                        tool_results_data.append({
                            "call_id": call_id,
                            "name": tool_name,
                            "status": status,
                            "result": tool_res,
                            "execution_time_ms": elapsed_ms
                        })

                        if status == "requires_confirmation":
                            assistant_content = f"⚠️ **Security Approval Required**\n\nThe assistant proposed an action: **{tool_args.get('description', 'Consequential action')}**.\n\nPlease review and approve or reject this action to continue."
                            break
                        else:
                            # Synthesize final answer with Gemini
                            assistant_content = await gemini_service.synthesize_tool_results(
                                prompt=user_text,
                                system_instruction=system_instruction,
                                history=history,
                                tools=tools,
                                tool_name=tool_name,
                                tool_result=tool_res
                            )

                else:
                    assistant_content = gemini_turn.get("content", "I processed your request.")

            except Exception as e:
                logger.warning(f"Gemini API call failed, falling back to autonomous tool agent: {e}")
                assistant_content, tool_calls_data, tool_results_data, final_status = await AgentService._fallback_autonomous_agent(
                    conversation_id, user_text, db
                )

        else:
            # Mode B: Autonomous local tool execution agent
            assistant_content, tool_calls_data, tool_results_data, final_status = await AgentService._fallback_autonomous_agent(
                conversation_id, user_text, db
            )

        # 5. Persist assistant message in DB
        assistant_message = Message(
            conversation_id=conversation_id,
            role="assistant",
            content=assistant_content,
            tool_calls=json.dumps(tool_calls_data) if tool_calls_data else None,
            tool_results=json.dumps(tool_results_data) if tool_results_data else None,
            status=final_status
        )
        db.add(assistant_message)
        conv.updated_at = db.query(Conversation).filter(Conversation.id == conversation_id).first().updated_at
        db.commit()
        db.refresh(assistant_message)

        return assistant_message

    @staticmethod
    async def _fallback_autonomous_agent(
        conversation_id: str,
        user_text: str,
        db: Session
    ) -> tuple[str, List[Dict[str, Any]], List[Dict[str, Any]], str]:
        """
        Intelligent local agent logic that recognizes math, search, document reading,
        and sensitive action intents, and executes real tools seamlessly.
        """
        tool_calls: List[Dict[str, Any]] = []
        tool_results: List[Dict[str, Any]] = []
        status = "completed"
        text_lower = user_text.lower().strip()

        # Check for sensitive action requests (consequential actions)
        if any(w in text_lower for w in ["clear history", "delete all messages", "wipe chat", "delete conversation"]):
            call_id = "call_action_delete"
            tool_calls.append({
                "id": call_id,
                "name": "request_consequential_action",
                "arguments": {
                    "action_type": "delete_all_messages",
                    "description": "Clear and delete all message history in this conversation"
                }
            })
            start = time.perf_counter()
            res = request_consequential_action(
                "delete_all_messages",
                "Clear and delete all message history in this conversation",
                {},
                conversation_id,
                db
            )
            tool_results.append({
                "call_id": call_id,
                "name": "request_consequential_action",
                "status": "requires_confirmation",
                "result": res,
                "execution_time_ms": round((time.perf_counter() - start) * 1000, 2)
            })
            content = "⚠️ **Action Confirmation Required**\n\nYou requested to clear all messages in this conversation. Please confirm or cancel below to proceed."
            return content, tool_calls, tool_results, "pending_confirmation"

        # Check for Math / Calculation intent
        math_match = re.search(r"(\bcalculate\b|\bmath\b|\bcompute\b|\bwhat is\b\s+)?([0-9\.\s\+\-\*\/\^\(\)\%sqrt|sin|cos|tan|pi|e|log|factorial]+[\+\-\*\/\^\%][0-9\.\s\+\-\*\/\^\(\)\%a-z]+)", text_lower)
        is_explicit_calc = any(text_lower.startswith(prefix) for prefix in ["calculate ", "compute ", "solve ", "eval "])
        
        if math_match or is_explicit_calc:
            raw_expr = user_text
            for prefix in ["calculate", "compute", "solve", "eval", "what is", "can you calculate"]:
                if text_lower.startswith(prefix):
                    raw_expr = user_text[len(prefix):].strip(" ?:=")
                    break

            # Clean expression
            expr = raw_expr.strip()
            call_id = "call_calc_01"
            tool_calls.append({
                "id": call_id,
                "name": "calculator",
                "arguments": {"expression": expr}
            })
            start = time.perf_counter()
            calc_res = safe_calculate(expr)
            elapsed = round((time.perf_counter() - start) * 1000, 2)

            tool_results.append({
                "call_id": call_id,
                "name": "calculator",
                "status": calc_res.get("status", "success"),
                "result": calc_res,
                "execution_time_ms": elapsed
            })

            if calc_res.get("status") == "success":
                content = f"### Calculation Result\n\n$$\n{expr} = {calc_res['result']}\n$$\n\nThe computed result for **`{expr}`** is **{calc_res['result']}**."
            else:
                content = f"I attempted to evaluate `{expr}` with the calculator tool, but encountered: {calc_res.get('error', 'Error in expression')}."
            return content, tool_calls, tool_results, "completed"

        # Check for Document Reading intent
        docs = MemoryService.get_conversation_documents(conversation_id, db)
        if docs and any(w in text_lower for w in ["document", "pdf", "file", "summarize", "read", "content", "attached"]):
            target_doc = docs[0]
            call_id = "call_doc_01"
            tool_calls.append({
                "id": call_id,
                "name": "read_document",
                "arguments": {"document_id": target_doc["id"], "query": user_text}
            })
            start = time.perf_counter()
            doc_res = read_document_content(target_doc["id"], db, query=user_text)
            elapsed = round((time.perf_counter() - start) * 1000, 2)
            tool_results.append({
                "call_id": call_id,
                "name": "read_document",
                "status": doc_res.get("status", "success"),
                "result": doc_res,
                "execution_time_ms": elapsed
            })

            excerpt = doc_res.get("content", "")
            if len(excerpt) > 1200:
                excerpt = excerpt[:1200] + " ...[truncated]"

            content = f"### Document Summary: {target_doc['filename']}\n\nI reviewed **`{target_doc['filename']}`** using the Document Reader tool. Here is the relevant text content:\n\n> {excerpt}\n\nFeel free to ask specific questions about this document!"
            return content, tool_calls, tool_results, "completed"

        # Check for Web Search intent
        search_triggers = ["search", "who is", "what is", "where is", "when did", "latest", "news", "price of", "weather", "look up"]
        if any(trigger in text_lower for trigger in search_triggers) or len(text_lower.split()) > 3:
            query = user_text
            for prefix in ["search for", "search", "look up", "find information on"]:
                if text_lower.startswith(prefix):
                    query = user_text[len(prefix):].strip(" :?")
                    break

            call_id = "call_web_01"
            tool_calls.append({
                "id": call_id,
                "name": "web_search",
                "arguments": {"query": query, "max_results": 4}
            })
            start = time.perf_counter()
            search_res = search_web(query, max_results=4)
            elapsed = round((time.perf_counter() - start) * 1000, 2)
            tool_results.append({
                "call_id": call_id,
                "name": "web_search",
                "status": search_res.get("status", "success"),
                "result": search_res,
                "execution_time_ms": elapsed
            })

            results_list = search_res.get("results", [])
            if results_list:
                items_md = []
                for idx, item in enumerate(results_list, 1):
                    items_md.append(f"{idx}. **[{item['title']}]({item['url']})**\n   {item['snippet']}")
                formatted_results = "\n\n".join(items_md)
                content = f"### Web Search Results for *\"{query}\"*\n\nHere are the top findings from live web search:\n\n{formatted_results}"
            else:
                content = f"I conducted a web search for *\"{query}\"*, but found no direct matches. Please try adjusting your keywords."
            return content, tool_calls, tool_results, "completed"

        # General response
        content = f"""Hello! I am your **AI Personal Assistant**.

I am connected and ready with the following tools:
- 🧮 **Calculator**: Ask me any calculation (e.g., `calculate 25 * 380 + sqrt(144)`).
- 🌐 **Web Search**: Ask me to search the web for any current information or news.
- 📄 **Document Reader**: Upload PDF or TXT documents to read and summarize them.
- 🛡️ **Safety Guard**: Asks for user confirmation before executing any consequential actions.

*(Tip: To enable full Gemini 3.8 Flash multimodal reasoning, ensure your `GEMINI_API_KEY` is added to `backend/.env`)*"""
        return content, tool_calls, tool_results, "completed"

    @staticmethod
    def handle_action_confirmation(
        action_id: str,
        approved: bool,
        db: Session
    ) -> Dict[str, Any]:
        """Process user approval or rejection for a pending consequential action."""
        action = db.query(PendingAction).filter(PendingAction.id == action_id).first()
        if not action:
            return {"status": "error", "message": f"Action {action_id} not found."}

        res = execute_confirmed_action(action, approved, db)
        return res
