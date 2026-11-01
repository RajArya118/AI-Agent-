import os
from pathlib import Path
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

# Resolve paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-3.8-flash"
    PORT: int = 8000
    HOST: str = "0.0.0.0"
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173"
    DATABASE_URL: str = f"sqlite:///{BASE_DIR / 'ai_assistant.db'}"
    MONGODB_URL: str = "mongodb://localhost:27017/buildpilot"
    MONGODB_URI: str = ""
    MAX_UPLOAD_SIZE_MB: int = 10
    UPLOAD_DIRECTORY: str = str(UPLOAD_DIR)

    @property
    def cors_origin_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

    @property
    def is_gemini_configured(self) -> bool:
        key = self.GEMINI_API_KEY.strip()
        return bool(key and key != "your_gemini_api_key_here" and len(key) > 5)

    @property
    def effective_mongodb_uri(self) -> str:
        # Atlas connection strings typically use MONGODB_URI or MONGODB_URL
        uri = os.getenv("MONGODB_URI") or self.MONGODB_URI or os.getenv("MONGODB_URL") or self.MONGODB_URL
        return uri.strip()

    @property
    def effective_port(self) -> int:
        port_env = os.getenv("PORT")
        if port_env:
            try:
                return int(port_env)
            except ValueError:
                pass
        return self.PORT

    @property
    def effective_host(self) -> str:
        return os.getenv("HOST", self.HOST)

settings = Settings()
