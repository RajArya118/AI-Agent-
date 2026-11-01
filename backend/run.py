import os
import sys
from pathlib import Path

# Ensure backend root is on sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import uvicorn
from app.core.config import settings

def main():
    print("=" * 60)
    print("🚀 Starting AI Personal Assistant Agent Application")
    print("=" * 60)
    print(f"-> Backend running on: http://localhost:{settings.PORT}")
    print(f"-> Interactive API docs: http://localhost:{settings.PORT}/docs")
    print(f"-> Health diagnostics: http://localhost:{settings.PORT}/api/health")
    if settings.is_gemini_configured:
        print(f"-> Gemini API: Active ({settings.GEMINI_MODEL})")
    else:
        print("-> Gemini API: Not configured in .env (running in autonomous tool fallback mode)")
    print("=" * 60)
    print(f"👉 Open your browser at: http://localhost:{settings.PORT}")
    print("=" * 60)

    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, log_level="info")

if __name__ == "__main__":
    main()
