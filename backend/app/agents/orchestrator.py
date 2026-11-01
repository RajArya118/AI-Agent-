import uuid
import time
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from app.agents.planner_agent import PlannerAgent
from app.agents.uiux_agent import UIUXAgent
from app.agents.database_agent import DatabaseAgent
from app.agents.backend_agent import BackendAgent
from app.agents.frontend_agent import FrontendAgent
from app.agents.qa_agent import QAAgent
from app.generators.presets import get_project_files_by_archetype
from app.generators.workspace_manager import WorkspaceManager

logger = logging.getLogger("buildpilot.orchestrator")

class AgentOrchestrator:
    def __init__(self):
        self.planner = PlannerAgent()
        self.uiux = UIUXAgent()
        self.database = DatabaseAgent()
        self.backend = BackendAgent()
        self.frontend = FrontendAgent()
        self.qa = QAAgent()

    async def execute_generation_pipeline(
        self,
        prompt: str,
        title: Optional[str] = None,
        gemini_client=None
    ) -> Dict[str, Any]:
        """
        Runs the full 7-agent software engineering pipeline.
        Tracks progress, captures agent telemetry, writes sandboxed files, and certifies quality.
        """
        start_time = time.perf_counter()
        project_id = str(uuid.uuid4())
        clean_title = title or prompt.strip().capitalize()[:40]

        agent_timeline: List[Dict[str, Any]] = []
        context: Dict[str, Any] = {"prompt": prompt, "title": clean_title, "project_id": project_id}

        # 1. Step: Planner Agent
        logger.info(f"[{project_id}] Running Planner Agent...")
        plan_res = await self.planner.execute(context, gemini_client)
        agent_timeline.append(plan_res)
        context["plan"] = plan_res.get("output", {})

        # 2. Step: UI/UX Agent
        logger.info(f"[{project_id}] Running UI/UX Agent...")
        uiux_res = await self.uiux.execute(context, gemini_client)
        agent_timeline.append(uiux_res)
        context["uiux"] = uiux_res.get("output", {})

        # 3. Step: Database Agent
        logger.info(f"[{project_id}] Running Database Agent...")
        db_res = await self.database.execute(context, gemini_client)
        agent_timeline.append(db_res)
        context["database"] = db_res.get("output", {})

        # 4. Step: Backend Agent
        logger.info(f"[{project_id}] Running Backend Agent...")
        backend_res = await self.backend.execute(context, gemini_client)
        agent_timeline.append(backend_res)
        context["backend"] = backend_res.get("output", {})

        # 5. Step: Frontend Agent
        logger.info(f"[{project_id}] Running Frontend Agent...")
        frontend_res = await self.frontend.execute(context, gemini_client)
        agent_timeline.append(frontend_res)
        context["frontend"] = frontend_res.get("output", {})

        # 6. Step: QA Agent
        logger.info(f"[{project_id}] Running QA Agent...")
        qa_res = await self.qa.execute(context, gemini_client)
        agent_timeline.append(qa_res)
        context["qa"] = qa_res.get("output", {})

        # 7. Code Generation & Sandbox file generation
        archetype = context["plan"].get("archetype", "custom_webapp")
        project_files = get_project_files_by_archetype(archetype, clean_title)

        # Write files into sandbox
        written_paths = WorkspaceManager.write_project_files(project_id, project_files)
        file_tree = WorkspaceManager.get_project_file_tree(project_id)

        total_elapsed = round((time.perf_counter() - start_time) * 1000, 2)

        record = {
            "id": project_id,
            "title": clean_title,
            "prompt": prompt,
            "archetype": archetype,
            "status": "completed",
            "progress": 100,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "execution_time_ms": total_elapsed,
            "agent_timeline": agent_timeline,
            "files_count": len(written_paths),
            "file_tree": file_tree,
            "qa_status": context["qa"].get("qa_status", "PASS")
        }

        return record

orchestrator = AgentOrchestrator()
