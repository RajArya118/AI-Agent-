import os
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from app.core.config import settings, BASE_DIR

logger = logging.getLogger("buildpilot.db")

class MongoDocumentStore:
    """
    MongoDB Document Repository supporting:
    1. Production MongoDB Atlas clusters (via mongodb+srv:// or mongodb:// connection string).
    2. Automatic indexing for high-performance sorting and query retrieval.
    3. Resilient local document persistence fallback when running offline or without credentials.
    """
    def __init__(self):
        self.client = None
        self.db = None
        self.is_connected = False
        self.connection_target = "Fallback (Local)"
        self.fallback_file = BASE_DIR / "mongodb_fallback.json"
        self._init_connection()

    def _init_connection(self):
        mongodb_url = settings.effective_mongodb_uri
        if not mongodb_url:
            mongodb_url = "mongodb://localhost:27017/buildpilot"

        try:
            from pymongo import MongoClient
            # Set timeout to prevent hanging on cold starts
            self.client = MongoClient(mongodb_url, serverSelectionTimeoutMS=2500)
            self.client.admin.command('ping')
            
            # Extract database name if specified in URI, otherwise default to 'buildpilot'
            default_db_name = "buildpilot"
            try:
                # get_default_database() uses db from the connection string if present
                self.db = self.client.get_default_database()
            except Exception:
                self.db = self.client.get_database(default_db_name)

            if self.db is None:
                self.db = self.client.get_database(default_db_name)

            # Ensure production indexes
            self._init_indexes()

            self.is_connected = True
            masked_url = self._mask_credentials(mongodb_url)
            self.connection_target = f"MongoDB ({masked_url})"
            logger.info(f"Connected to MongoDB successfully: {self.connection_target}")
        except Exception as e:
            logger.info(f"MongoDB not connected ({e}). Using resilient document repository fallback.")
            self.is_connected = False
            self.connection_target = "Local Resilient Fallback (mongodb_fallback.json)"
            if not self.fallback_file.exists():
                with open(self.fallback_file, "w", encoding="utf-8") as f:
                    json.dump([], f)

    def _init_indexes(self):
        """Creates required MongoDB collection indexes for production performance."""
        try:
            if self.db is not None:
                self.db.projects.create_index([("created_at", -1)], background=True)
                self.db.projects.create_index([("status", 1)], background=True)
                self.db.projects.create_index([("archetype", 1)], background=True)
                logger.info("MongoDB production indexes verified for 'projects' collection.")
        except Exception as e:
            logger.warning(f"Could not initialize MongoDB indexes: {e}")

    def _mask_credentials(self, uri: str) -> str:
        """Safely mask password in logs/diagnostics."""
        try:
            if "@" in uri and "://" in uri:
                scheme_part, rest = uri.split("://", 1)
                auth_part, host_part = rest.split("@", 1)
                user = auth_part.split(":")[0] if ":" in auth_part else auth_part
                return f"{scheme_part}://{user}:****@{host_part}"
        except Exception:
            pass
        return "mongodb://[configured]"

    def _read_fallback(self) -> List[Dict[str, Any]]:
        try:
            with open(self.fallback_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def _write_fallback(self, docs: List[Dict[str, Any]]):
        with open(self.fallback_file, "w", encoding="utf-8") as f:
            json.dump(docs, f, indent=2)

    def insert_project(self, project_data: Dict[str, Any]) -> str:
        if self.is_connected and self.db is not None:
            doc = dict(project_data)
            doc["_id"] = doc["id"]
            self.db.projects.replace_one({"_id": doc["_id"]}, doc, upsert=True)
            return doc["_id"]
        else:
            docs = self._read_fallback()
            # replace or insert
            docs = [d for d in docs if d.get("id") != project_data.get("id")]
            docs.insert(0, project_data)
            self._write_fallback(docs)
            return project_data["id"]

    def get_project(self, project_id: str) -> Optional[Dict[str, Any]]:
        if self.is_connected and self.db is not None:
            doc = self.db.projects.find_one({"_id": project_id})
            if doc:
                doc.pop("_id", None)
            return doc
        else:
            docs = self._read_fallback()
            return next((d for d in docs if d.get("id") == project_id), None)

    def list_projects(self) -> List[Dict[str, Any]]:
        if self.is_connected and self.db is not None:
            cursor = self.db.projects.find().sort("created_at", -1)
            results = []
            for doc in cursor:
                doc.pop("_id", None)
                results.append(doc)
            return results
        else:
            return self._read_fallback()

    def delete_project(self, project_id: str) -> bool:
        if self.is_connected and self.db is not None:
            res = self.db.projects.delete_one({"_id": project_id})
            return res.deleted_count > 0
        else:
            docs = self._read_fallback()
            new_docs = [d for d in docs if d.get("id") != project_id]
            self._write_fallback(new_docs)
            return len(new_docs) < len(docs)

mongo_store = MongoDocumentStore()
