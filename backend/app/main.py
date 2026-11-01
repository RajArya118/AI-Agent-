import os
import logging
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.core.config import settings, BASE_DIR
from app.core.database import init_db
from app.api import (
    conversations_router,
    chat_router,
    documents_router,
    health_router,
    projects_router
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("buildpilot")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: initialize database tables
    logger.info("Initializing database tables...")
    init_db()
    logger.info("BuildPilot database initialized successfully.")
    yield
    # Shutdown
    logger.info("BuildPilot service shutting down.")

app = FastAPI(
    title="BuildPilot AI — Autonomous Multi-Agent Engineering Platform",
    description="Full-stack AI platform with Planner, UI/UX, Frontend, Backend, Database, and QA specialist agents.",
    version="2.0.0",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list + ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers (prefixed with /api)
app.include_router(projects_router)
app.include_router(conversations_router)
app.include_router(chat_router)
app.include_router(documents_router)
app.include_router(health_router)

# Locate frontend dist
frontend_dist = BASE_DIR.parent / "frontend" / "dist"
if not frontend_dist.exists():
    alt_dist = Path("C:/Users/chand/AppData/Local/ai_agent_frontend/dist")
    if alt_dist.exists():
        frontend_dist = alt_dist

if frontend_dist.exists():
    logger.info(f"Mounting frontend static files from {frontend_dist}")
    app.mount("/assets", StaticFiles(directory=str(frontend_dist / "assets")), name="assets")

    @app.get("/{full_path:path}")
    async def serve_react_app(full_path: str):
        if full_path.startswith("api"):
            return None
        file_target = frontend_dist / full_path
        if file_target.exists() and file_target.is_file():
            return FileResponse(file_target)
        return FileResponse(frontend_dist / "index.html")
else:
    @app.get("/")
    def root():
        return {
            "name": "BuildPilot AI API",
            "version": "2.0.0",
            "status": "online",
            "docs_url": "/docs",
            "health_url": "/api/health"
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=False)
