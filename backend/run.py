import os
import sys
from pathlib import Path

# Ensure backend root is on sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import uvicorn
from app.core.config import settings

def main():
    host = settings.effective_host
    port = settings.effective_port

    print("=" * 60)
    print("🚀 Starting BuildPilot AI Backend Service")
    print("=" * 60)
    print(f"-> Host: {host} | Port: {port}")
    print(f"-> Interactive API docs: http://{host}:{port}/docs")
    print(f"-> Health diagnostics: http://{host}:{port}/api/health")
    if settings.is_gemini_configured:
        print(f"-> Gemini API: Active ({settings.GEMINI_MODEL})")
    else:
        print("-> Gemini API: Not configured in .env (running in autonomous tool fallback mode)")
    print("=" * 60)

    uvicorn.run("app.main:app", host=host, port=port, log_level="info")

if __name__ == "__main__":
    main()
