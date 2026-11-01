import pytest
import io
import zipfile
from fastapi.testclient import TestClient
from app.main import app
from app.agents.planner_agent import PlannerAgent
from app.agents.uiux_agent import UIUXAgent
from app.agents.database_agent import DatabaseAgent
from app.agents.backend_agent import BackendAgent
from app.agents.frontend_agent import FrontendAgent
from app.agents.qa_agent import QAAgent
from app.agents.orchestrator import orchestrator
from app.generators.workspace_manager import WorkspaceManager
from app.core.mongodb import mongo_store

client = TestClient(app)

# ==========================================
# Phase 4: Specialist Agent Tests
# ==========================================

@pytest.mark.asyncio
async def test_planner_agent():
    planner = PlannerAgent()
    context = {"prompt": "Build a luxury hotel booking website", "title": "Hotel Luxe"}
    res = await planner.execute(context)
    assert res["status"] == "completed"
    assert res["output"]["archetype"] == "hotel_booking"
    assert "RoomCatalog" in res["output"]["frontend_modules"]
    assert len(res["output"]["task_dependency_graph"]) == 6

@pytest.mark.asyncio
async def test_uiux_agent():
    uiux = UIUXAgent()
    context = {"plan": {"archetype": "ecommerce"}}
    res = await uiux.execute(context)
    assert res["status"] == "completed"
    assert "color_system" in res["output"]
    assert "mobile_sm" in res["output"]["viewports"]
    assert res["output"]["viewports"]["desktop"] == "1440px"

@pytest.mark.asyncio
async def test_database_agent():
    db_agent = DatabaseAgent()
    context = {"plan": {"archetype": "portfolio"}}
    res = await db_agent.execute(context)
    assert res["status"] == "completed"
    assert "projects" in res["output"]["collections"]
    assert "messages" in res["output"]["collections"]

@pytest.mark.asyncio
async def test_backend_agent():
    be_agent = BackendAgent()
    context = {"plan": {"archetype": "task_manager"}}
    res = await be_agent.execute(context)
    assert res["status"] == "completed"
    assert res["output"]["framework"] == "FastAPI"
    assert any("/api/tasks" in e["path"] for e in res["output"]["endpoints"])

@pytest.mark.asyncio
async def test_frontend_agent():
    fe_agent = FrontendAgent()
    context = {"plan": {"archetype": "hotel_booking"}}
    res = await fe_agent.execute(context)
    assert res["status"] == "completed"
    assert any("RoomCard" in c["name"] for c in res["output"]["components"])

@pytest.mark.asyncio
async def test_qa_agent():
    qa_agent = QAAgent()
    context = {"plan": {"archetype": "ecommerce"}}
    res = await qa_agent.execute(context)
    assert res["status"] == "completed"
    assert res["output"]["qa_status"] == "PASS"
    assert res["output"]["passed_tests"] > 0

# ==========================================
# Multi-Agent Orchestrator Pipeline Tests
# ==========================================

@pytest.mark.asyncio
async def test_orchestrator_pipeline_hotel():
    record = await orchestrator.execute_generation_pipeline(
        prompt="Build a hotel booking website."
    )
    assert record["status"] == "completed"
    assert record["archetype"] == "hotel_booking"
    assert len(record["agent_timeline"]) == 6
    assert record["qa_status"] == "PASS"
    assert record["files_count"] >= 2

@pytest.mark.asyncio
async def test_orchestrator_pipeline_ecommerce():
    record = await orchestrator.execute_generation_pipeline(
        prompt="Build an e-commerce website with admin dashboard."
    )
    assert record["status"] == "completed"
    assert record["archetype"] == "ecommerce"

@pytest.mark.asyncio
async def test_orchestrator_pipeline_portfolio():
    record = await orchestrator.execute_generation_pipeline(
        prompt="Build a portfolio website with contact form."
    )
    assert record["status"] == "completed"
    assert record["archetype"] == "portfolio"

@pytest.mark.asyncio
async def test_orchestrator_pipeline_task_manager():
    record = await orchestrator.execute_generation_pipeline(
        prompt="Build a task management application."
    )
    assert record["status"] == "completed"
    assert record["archetype"] == "task_manager"

# ==========================================
# REST API Endpoints & Workflows
# ==========================================

def test_api_health():
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert data["specialist_agents_active"] == 7

def test_api_project_lifecycle():
    # 1. Create project
    res = client.post("/api/projects", json={
        "prompt": "Build a luxury hotel booking website.",
        "title": "Grand Horizon Resort"
    })
    assert res.status_code == 201
    proj = res.json()
    p_id = proj["id"]
    assert proj["title"] == "Grand Horizon Resort"
    assert proj["archetype"] == "hotel_booking"

    # 2. Get project details
    res = client.get(f"/api/projects/{p_id}")
    assert res.status_code == 200
    details = res.json()
    assert len(details["file_tree"]) >= 2

    # 3. Live Preview HTML test
    preview_res = client.get(f"/api/projects/{p_id}/preview")
    assert preview_res.status_code == 200
    assert "Grand Horizon" in preview_res.text
    assert "<script>" in preview_res.text
    # Verify no dead fake buttons
    assert "onclick=" in preview_res.text

    # 4. Read specific file
    file_res = client.get(f"/api/projects/{p_id}/files/README.md")
    assert file_res.status_code == 200
    assert "BuildPilot AI" in file_res.json()["content"]

    # 5. Security Path Traversal prevention
    with pytest.raises(ValueError, match="Path traversal attempt blocked"):
        WorkspaceManager.validate_safe_path(p_id, "../../etc/passwd")

    with pytest.raises(ValueError, match="Path traversal attempt blocked"):
        WorkspaceManager.validate_safe_path(p_id, "..\\..\\windows\\system32\\calc.exe")

    # 6. ZIP Export test
    export_res = client.get(f"/api/projects/{p_id}/export")
    assert export_res.status_code == 200
    assert export_res.headers["content-type"] == "application/zip"
    zip_bytes = io.BytesIO(export_res.content)
    with zipfile.ZipFile(zip_bytes, "r") as z:
        names = z.namelist()
        assert "index.html" in names
        assert "README.md" in names

    # 7. List projects
    list_res = client.get("/api/projects")
    assert list_res.status_code == 200
    assert any(p["id"] == p_id for p in list_res.json())

    # 8. Delete project
    del_res = client.delete(f"/api/projects/{p_id}")
    assert del_res.status_code == 204
