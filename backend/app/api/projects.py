from typing import List, Optional
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import HTMLResponse, StreamingResponse
from pydantic import BaseModel, Field
from app.agents.orchestrator import orchestrator
from app.generators.workspace_manager import WorkspaceManager
from app.core.mongodb import mongo_store

router = APIRouter(prefix="/api/projects", tags=["BuildPilot Projects"])

class ProjectCreateRequest(BaseModel):
    prompt: str = Field(..., min_length=3, description="Description of the web application to generate")
    title: Optional[str] = Field(None, description="Optional custom project title")

@router.post("", status_code=status.HTTP_201_CREATED)
async def generate_project(payload: ProjectCreateRequest):
    if not payload.prompt.strip():
        raise HTTPException(status_code=400, detail="Generation prompt cannot be empty.")

    try:
        project_record = await orchestrator.execute_generation_pipeline(
            prompt=payload.prompt,
            title=payload.title
        )
        mongo_store.insert_project(project_record)
        return project_record
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Agent Orchestrator encountered an error: {str(e)}"
        )

@router.get("")
def list_projects():
    return mongo_store.list_projects()

@router.get("/{project_id}")
def get_project(project_id: str):
    proj = mongo_store.get_project(project_id)
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found.")
    # Refresh file tree from disk
    proj["file_tree"] = WorkspaceManager.get_project_file_tree(project_id)
    return proj

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: str):
    deleted = mongo_store.delete_project(project_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Project not found.")
    return None

@router.get("/{project_id}/preview", response_class=HTMLResponse)
def get_project_live_preview(project_id: str):
    try:
        content = WorkspaceManager.read_project_file(project_id, "index.html")
        return HTMLResponse(content=content)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Preview index.html not found for this project.")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{project_id}/files/{file_path:path}")
def get_project_file_content(project_id: str, file_path: str):
    try:
        content = WorkspaceManager.read_project_file(project_id, file_path)
        return {"project_id": project_id, "file_path": file_path, "content": content}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"File '{file_path}' not found.")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{project_id}/export")
def export_project_zip(project_id: str):
    proj = mongo_store.get_project(project_id)
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found.")

    zip_io = WorkspaceManager.create_project_zip(project_id)
    safe_filename = f"{proj.get('title', 'buildpilot_project').lower().replace(' ', '_')}_{project_id[:8]}.zip"

    return StreamingResponse(
        zip_io,
        media_type="application/zip",
        headers={"Content-Disposition": f"attachment; filename={safe_filename}"}
    )
