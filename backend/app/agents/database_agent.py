from typing import Dict, Any
from app.agents.base_agent import BaseSpecialistAgent

class DatabaseAgent(BaseSpecialistAgent):
    def __init__(self):
        super().__init__(
            name="Database Agent",
            role="Data Architect & Database Engineer",
            description="Designs document schemas, index strategies, relationship mappings, and high-fidelity seed datasets for MongoDB."
        )

    async def _run(self, context: Dict[str, Any], gemini_client=None) -> Dict[str, Any]:
        plan = context.get("plan", {})
        archetype = plan.get("archetype", "custom_webapp")

        if archetype == "hotel_booking":
            collections = {
                "rooms": {
                    "indexes": [("room_type", 1), ("price_per_night", 1), ("rating", -1)],
                    "schema": {
                        "id": "string",
                        "title": "string",
                        "room_type": "string (Deluxe | Suite | Ocean View | Standard)",
                        "price_per_night": "number",
                        "rating": "number",
                        "amenities": "array of strings",
                        "available": "boolean",
                        "image_url": "string"
                    }
                },
                "bookings": {
                    "indexes": [("room_id", 1), ("check_in", 1), ("guest_email", 1)],
                    "schema": {
                        "id": "string",
                        "room_id": "string",
                        "guest_name": "string",
                        "guest_email": "string",
                        "check_in": "ISO Date",
                        "check_out": "ISO Date",
                        "total_price": "number",
                        "status": "string (confirmed | pending | cancelled)"
                    }
                }
            }
        elif archetype == "ecommerce":
            collections = {
                "products": {
                    "indexes": [("category", 1), ("price", 1), ("stock", 1)],
                    "schema": {
                        "id": "string",
                        "title": "string",
                        "category": "string",
                        "price": "number",
                        "rating": "number",
                        "stock": "number",
                        "image_url": "string"
                    }
                },
                "orders": {
                    "indexes": [("customer_email", 1), ("status", 1), ("created_at", -1)],
                    "schema": {
                        "id": "string",
                        "items": "array of objects (product_id, qty, price)",
                        "total_amount": "number",
                        "status": "string (paid | processing | shipped)",
                        "created_at": "ISO Date"
                    }
                }
            }
        elif archetype == "portfolio":
            collections = {
                "projects": {
                    "indexes": [("category", 1), ("featured", -1)],
                    "schema": {
                        "id": "string",
                        "title": "string",
                        "description": "string",
                        "category": "string",
                        "tags": "array of strings",
                        "demo_url": "string",
                        "github_url": "string"
                    }
                },
                "messages": {
                    "indexes": [("created_at", -1)],
                    "schema": {
                        "id": "string",
                        "sender_name": "string",
                        "sender_email": "string",
                        "message": "string",
                        "created_at": "ISO Date"
                    }
                }
            }
        else: # task_manager
            collections = {
                "tasks": {
                    "indexes": [("status", 1), ("priority", 1), ("due_date", 1)],
                    "schema": {
                        "id": "string",
                        "title": "string",
                        "description": "string",
                        "status": "string (todo | in_progress | completed)",
                        "priority": "string (low | medium | high)",
                        "assigned_to": "string",
                        "created_at": "ISO Date"
                    }
                }
            }

        return {
            "archetype": archetype,
            "database_type": "MongoDB",
            "collections": collections,
            "validation_rules": "BSON Schema validation enforced on write",
            "seed_data_ready": True
        }
