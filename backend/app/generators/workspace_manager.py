import os
import io
import zipfile
from pathlib import Path
from typing import Dict, Any, List, Optional
from app.core.config import BASE_DIR

PROJECTS_DIR = BASE_DIR / "generated_projects"
PROJECTS_DIR.mkdir(parents=True, exist_ok=True)

class WorkspaceManager:
    @staticmethod
    def get_project_dir(project_id: str) -> Path:
        """Returns the canonical root path for a generated project."""
        p_dir = PROJECTS_DIR / project_id
        p_dir.mkdir(parents=True, exist_ok=True)
        return p_dir

    @staticmethod
    def validate_safe_path(project_id: str, relative_path: str) -> Path:
        """
        Security verification preventing path traversal outside the project directory.
        Raises ValueError if path attempts to escape the project sandbox.
        """
        base = WorkspaceManager.get_project_dir(project_id).resolve()
        target = (base / relative_path).resolve()

        if not str(target).startswith(str(base)):
            raise ValueError(f"Security Alert: Path traversal attempt blocked: '{relative_path}'")
        return target

    @staticmethod
    def write_project_files(project_id: str, files: Dict[str, str]) -> List[str]:
        """Writes all generated project files into the sandbox."""
        written = []
        base = WorkspaceManager.get_project_dir(project_id)

        for rel_path, content in files.items():
            file_path = WorkspaceManager.validate_safe_path(project_id, rel_path)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            written.append(rel_path)

        return written

    @staticmethod
    def read_project_file(project_id: str, relative_path: str) -> str:
        """Safely reads a project file from disk."""
        target = WorkspaceManager.validate_safe_path(project_id, relative_path)
        if not target.exists() or not target.is_file():
            raise FileNotFoundError(f"File '{relative_path}' not found in project {project_id}.")
        with open(target, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

    @staticmethod
    def get_project_file_tree(project_id: str) -> List[Dict[str, Any]]:
        """Returns a flat list of files with metadata in the project sandbox."""
        base = WorkspaceManager.get_project_dir(project_id)
        file_tree = []

        for p in base.rglob("*"):
            if p.is_file():
                rel = p.relative_to(base).as_posix()
                file_tree.append({
                    "path": rel,
                    "name": p.name,
                    "size": p.stat().st_size,
                    "type": p.suffix.replace(".", "") or "file"
                })

        return sorted(file_tree, key=lambda x: x["path"])

    @staticmethod
    def create_project_zip(project_id: str) -> io.BytesIO:
        """Packages all project files into an in-memory ZIP archive."""
        base = WorkspaceManager.get_project_dir(project_id)
        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for p in base.rglob("*"):
                if p.is_file():
                    arcname = p.relative_to(base).as_posix()
                    zip_file.write(p, arcname=arcname)

        zip_buffer.seek(0)
        return zip_buffer
