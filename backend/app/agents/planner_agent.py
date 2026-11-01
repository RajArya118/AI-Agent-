from typing import Dict, Any
from app.agents.base_agent import BaseSpecialistAgent

class PlannerAgent(BaseSpecialistAgent):
    def __init__(self):
        super().__init__(
            name="Planner Agent",
            role="Software Architect & Lead System Planner",
            description="Deconstructs product requirements into technical architecture, component trees, API schemas, and task dependency graphs."
        )

    async def _run(self, context: Dict[str, Any], gemini_client=None) -> Dict[str, Any]:
        prompt = context.get("prompt", "").lower()
        title = context.get("title", "Generated Project")

        # Classify product archetype
        if any(k in prompt for k in ["hotel", "room", "booking", "resort"]):
            archetype = "hotel_booking"
            tech_stack = ["React", "Tailwind CSS", "FastAPI", "MongoDB"]
            modules = ["RoomCatalog", "DateRangePicker", "BookingModal", "ReviewsSection", "AmenitiesFilter"]
            apis = ["GET /api/rooms", "POST /api/bookings", "GET /api/amenities", "GET /api/reviews"]
            collections = ["rooms", "bookings", "reviews"]
        elif any(k in prompt for k in ["ecommerce", "e-commerce", "shop", "store", "product", "cart"]):
            archetype = "ecommerce"
            tech_stack = ["React", "Tailwind CSS", "FastAPI", "MongoDB", "ChartJS"]
            modules = ["ProductGrid", "CartDrawer", "CheckoutModal", "AdminAnalytics", "InventoryTable"]
            apis = ["GET /api/products", "POST /api/orders", "GET /api/admin/metrics", "PUT /api/inventory"]
            collections = ["products", "orders", "customers", "inventory"]
        elif any(k in prompt for k in ["portfolio", "resume", "personal website", "freelance"]):
            archetype = "portfolio"
            tech_stack = ["React", "Tailwind CSS", "FastAPI", "MongoDB"]
            modules = ["HeroBanner", "ProjectShowcase", "SkillBadges", "Testimonials", "ContactForm"]
            apis = ["GET /api/projects", "POST /api/contact", "GET /api/skills"]
            collections = ["projects", "messages", "skills"]
        elif any(k in prompt for k in ["task", "todo", "kanban", "project management"]):
            archetype = "task_manager"
            tech_stack = ["React", "Tailwind CSS", "FastAPI", "MongoDB"]
            modules = ["KanbanBoard", "TaskModal", "PriorityFilter", "ColumnManager", "StatsSummary"]
            apis = ["GET /api/tasks", "POST /api/tasks", "PUT /api/tasks/{id}", "DELETE /api/tasks/{id}"]
            collections = ["tasks", "columns", "tags"]
        else:
            archetype = "custom_webapp"
            tech_stack = ["React", "Tailwind CSS", "FastAPI", "MongoDB"]
            modules = ["Navbar", "DashboardView", "DataTable", "InteractiveForm", "SettingsPanel"]
            apis = ["GET /api/items", "POST /api/items", "GET /api/stats"]
            collections = ["items", "users"]

        plan = {
            "title": title,
            "archetype": archetype,
            "architecture_pattern": "Client-Server Layered Architecture",
            "tech_stack": tech_stack,
            "frontend_modules": modules,
            "backend_apis": apis,
            "database_collections": collections,
            "task_dependency_graph": [
                {"step": 1, "agent": "Planner Agent", "status": "completed"},
                {"step": 2, "agent": "UI/UX Agent", "depends_on": [1]},
                {"step": 3, "agent": "Database Agent", "depends_on": [1]},
                {"step": 4, "agent": "Backend Agent", "depends_on": [1, 3]},
                {"step": 5, "agent": "Frontend Agent", "depends_on": [2, 4]},
                {"step": 6, "agent": "QA Agent", "depends_on": [5]}
            ],
            "non_functional_requirements": [
                "Responsive on mobile (360px), tablet (768px), and desktop (1440px)",
                "Accessibility compliance (WCAG AA)",
                "No fake buttons or dead interactive elements",
                "Sub-second client rendering"
            ]
        }
        return plan
