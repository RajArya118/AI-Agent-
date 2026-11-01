import asyncio
import os
import json
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal, init_db
from app.models.db_models import Conversation, Message, Document

client = TestClient(app)

def run_tests():
    print("=" * 60)
    print("RUNNING AI PERSONAL ASSISTANT COMPREHENSIVE TEST SUITE")
    print("=" * 60)

    # 1. Test Health Endpoint
    print("\n[1] Testing Health Endpoint (/api/health)...")
    res = client.get("/api/health")
    assert res.status_code == 200, f"Health check failed: {res.text}"
    health_data = res.json()
    print("-> Status:", health_data["status"])
    print("-> Gemini Configured:", health_data["gemini_configured"])
    print("-> Model:", health_data["gemini_model"])
    print("-> Calculator Tool Active:", health_data["calculator"])
    print("-> Web Search Tool Active:", health_data["duckduckgo_search"])
    print("-> Document Reader Active:", health_data["document_reader"])

    # 2. Test Create Conversation
    print("\n[2] Testing Create Conversation (/api/conversations)...")
    res = client.post("/api/conversations", json={"title": "Test AI Suite Session"})
    assert res.status_code == 201, f"Create conversation failed: {res.text}"
    conv = res.json()
    conv_id = conv["id"]
    print(f"-> Created conversation ID: {conv_id} with title: '{conv['title']}'")

    # 3. Test Calculator Tool
    print("\n[3] Testing Calculator Tool execution...")
    math_prompt = "Calculate 125 * 45 + sqrt(1024) - 2^4"
    res = client.post(f"/api/conversations/{conv_id}/messages", json={"content": math_prompt})
    assert res.status_code == 200, f"Message failed: {res.text}"
    msg = res.json()
    print("-> Assistant Response Status:", msg["status"])
    print("-> Tool Calls Executed:", [tc["name"] for tc in (msg.get("tool_calls") or [])])
    assert msg.get("tool_calls") and msg["tool_calls"][0]["name"] == "calculator"
    print("-> Calculator Output Details:", msg.get("tool_results"))
    print("-> Assistant Message Content:\n", msg["content"])

    # 4. Test Web Search Tool
    print("\n[4] Testing Web Search Tool execution...")
    search_prompt = "Search for latest Python 3 features and release notes"
    res = client.post(f"/api/conversations/{conv_id}/messages", json={"content": search_prompt})
    assert res.status_code == 200, f"Search message failed: {res.text}"
    search_msg = res.json()
    print("-> Assistant Response Status:", search_msg["status"])
    print("-> Tool Calls Executed:", [tc["name"] for tc in (search_msg.get("tool_calls") or [])])
    assert search_msg.get("tool_calls") and search_msg["tool_calls"][0]["name"] == "web_search"
    print("-> Assistant Search Findings Summary Snippet:\n", search_msg["content"][:300] + "...")

    # 5. Test File Upload (TXT and validation)
    print("\n[5] Testing Document Upload and Text Extraction (/api/documents/upload)...")
    sample_txt_content = """# Autonomous AI Assistant System Architecture
The AI Assistant system utilizes an execution loop combining reasoning with modular tools.
Key components include:
1. AST-based Calculator: Eliminates code injection while providing comprehensive mathematical capabilities.
2. DuckDuckGo Search Integration: Delivers live web search without requiring external credit card API keys.
3. Multi-format Document Processing: Supports PDF and TXT text extraction and query-based retrieval.
4. Security Confirmation Gates: Enforces explicit user confirmation before any consequential action is taken."""
    
    files = {"file": ("architecture_doc.txt", sample_txt_content.encode("utf-8"), "text/plain")}
    data = {"conversation_id": conv_id}
    res = client.post("/api/documents/upload", files=files, data=data)
    assert res.status_code == 201, f"Upload failed: {res.text}"
    doc = res.json()
    doc_id = doc["id"]
    print(f"-> Uploaded Doc ID: {doc_id}, Original Name: '{doc['original_name']}', Size: {doc['file_size']} bytes")
    print("-> Document Summary Preview:", doc.get("summary"))

    # 6. Test Document Reader Tool
    print("\n[6] Testing Document Reader Tool execution...")
    doc_prompt = "Summarize the uploaded document and list its key components"
    res = client.post(
        f"/api/conversations/{conv_id}/messages",
        json={"content": doc_prompt, "document_ids": [doc_id]}
    )
    assert res.status_code == 200, f"Doc reader message failed: {res.text}"
    doc_msg = res.json()
    print("-> Tool Calls Executed:", [tc["name"] for tc in (doc_msg.get("tool_calls") or [])])
    assert doc_msg.get("tool_calls") and doc_msg["tool_calls"][0]["name"] == "read_document"
    print("-> Document Reading Output:\n", doc_msg["content"][:350] + "...")

    # 7. Test Consequential Action Confirmation Flow
    print("\n[7] Testing Consequential Action Security Flow...")
    action_prompt = "Please delete all messages in this conversation history"
    res = client.post(f"/api/conversations/{conv_id}/messages", json={"content": action_prompt})
    assert res.status_code == 200
    action_msg = res.json()
    print("-> Status:", action_msg["status"])
    assert action_msg["status"] == "pending_confirmation"
    action_res = next(r for r in action_msg["tool_results"] if r["status"] == "requires_confirmation")
    pending_action_id = action_res["result"]["action_id"]
    print(f"-> Security Gate Active: Action ID '{pending_action_id}' requires user approval")

    # Confirm action rejection first
    print("-> Testing Rejection of action...")
    reject_res = client.post(
        f"/api/conversations/{conv_id}/action-confirmation",
        json={"action_id": pending_action_id, "approved": False}
    )
    assert reject_res.status_code == 200
    print("-> Rejection response:", reject_res.json()["message"])

    # 8. Test Conversation History retrieval
    print("\n[8] Testing Conversation Full History retrieval (/api/conversations/{id})...")
    res = client.get(f"/api/conversations/{conv_id}")
    assert res.status_code == 200
    conv_data = res.json()
    print(f"-> Conversation '{conv_data['title']}' has {len(conv_data['messages'])} persisted messages.")

    # 9. Test Frontend Static Asset Serving from FastAPI
    print("\n[9] Testing Production Frontend Serving from FastAPI (GET /)...")
    res = client.get("/")
    assert res.status_code == 200
    assert "<!doctype html>" in res.text.lower() or "html" in res.text.lower()
    print("-> React HTML App successfully served at root '/'!")

    print("\n" + "=" * 60)
    print("ALL TESTS PASSED SUCCESSFULLY! (100% PASS RATE)")
    print("=" * 60)

if __name__ == "__main__":
    init_db()
    run_tests()
