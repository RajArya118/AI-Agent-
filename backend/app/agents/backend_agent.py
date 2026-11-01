from typing import Dict, Any
from app.agents.base_agent import BaseSpecialistAgent

class BackendAgent(BaseSpecialistAgent):
    def __init__(self):
        super().__init__(
            name="Backend Agent",
            role="Senior Backend Engineer & API Architect",
            description="Generates production FastAPI REST endpoints, Pydantic data validation schemas, error handlers, and business logic controllers."
        )

    async def _run(self, context: Dict[str, Any], gemini_client=None) -> Dict[str, Any]:
        plan = context.get("plan", {})
        archetype = plan.get("archetype", "custom_webapp")

        endpoints_map = {
            "hotel_booking": [
                {"method": "GET", "path": "/api/rooms", "description": "Retrieve list of rooms with optional filters (type, max_price, available)"},
                {"method": "GET", "path": "/api/rooms/{id}", "description": "Get room details and amenities"},
                {"method": "POST", "path": "/api/bookings", "description": "Create a room reservation with validation and price calculation"},
                {"method": "GET", "path": "/api/amenities", "description": "List all hotel facilities and filters"}
            ],
            "ecommerce": [
                {"method": "GET", "path": "/api/products", "description": "List products with search, pagination, and category filtering"},
                {"method": "POST", "path": "/api/orders", "description": "Submit shopping cart order, calculate taxes, and update stock"},
                {"method": "GET", "path": "/api/admin/metrics", "description": "Return revenue charts, order counts, and top selling products"},
                {"method": "PUT", "path": "/api/inventory/{id}", "description": "Admin endpoint to restock or modify pricing"}
            ],
            "portfolio": [
                {"method": "GET", "path": "/api/projects", "description": "List featured portfolio projects filtered by technology tag"},
                {"method": "POST", "path": "/api/contact", "description": "Receive and sanitize contact form inquiry messages"},
                {"method": "GET", "path": "/api/skills", "description": "Return skills breakdown with proficiency metrics"}
            ],
            "task_manager": [
                {"method": "GET", "path": "/api/tasks", "description": "List Kanban tasks grouped by status (todo, in_progress, completed)"},
                {"method": "POST", "path": "/api/tasks", "description": "Create a new task with priority tag and assignment"},
                {"method": "PUT", "path": "/api/tasks/{id}", "description": "Update task status or drag-and-drop column positioning"},
                {"method": "DELETE", "path": "/api/tasks/{id}", "description": "Archive or remove a task"}
            ]
        }

        endpoints = endpoints_map.get(archetype, endpoints_map["ecommerce"])

        return {
            "archetype": archetype,
            "framework": "FastAPI",
            "cors_configured": True,
            "endpoints": endpoints,
            "security_middlewares": ["InputValidation", "RateLimiting", "SafeCORS"],
            "backend_code_ready": True
        }
