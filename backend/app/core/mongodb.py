import os
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from app.core.config import settings, BASE_DIR

logger = logging.getLogger("buildpilot.db")

class MongoDocumentStore:
    """
    Asynchronous document repository supporting both live MongoDB connections
    and resilient local document persistence fallback when MongoDB daemon is offline.
    """
    def __init__(self):
        self.client = None
        self.db = None
        self.is_connected = False
        self.fallback_file = BASE_DIR / "mongodb_fallback.json"
        self._init_connection()

    def _init_connection(self):
        mongodb_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017/buildpilot")
        try:
            from pymongo import MongoClient
            self.client = MongoClient(mongodb_url, serverSelectionTimeoutMS=1500)
            self.client.admin.command('ping')
            self.db = self.client.get_database("buildpilot")
            self.is_connected = True
            logger.info("Connected to live MongoDB instance successfully.")
        except Exception as e:
            logger.info(f"Live MongoDB not available ({e}). Using resilient document repository fallback.")
            self.is_connected = False
            if not self.fallback_file.exists():
                with open(self.fallback_file, "w", encoding="utf-8") as f:
                    json.dump([], f)

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
