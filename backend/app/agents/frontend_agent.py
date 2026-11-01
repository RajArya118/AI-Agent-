from typing import Dict, Any
from app.agents.base_agent import BaseSpecialistAgent

class FrontendAgent(BaseSpecialistAgent):
    def __init__(self):
        super().__init__(
            name="Frontend Agent",
            role="Staff Frontend Engineer",
            description="Generates production-grade React components, responsive layouts with Tailwind CSS, state management hooks, and interactive user controls."
        )

    async def _run(self, context: Dict[str, Any], gemini_client=None) -> Dict[str, Any]:
        plan = context.get("plan", {})
        uiux = context.get("uiux", {})
        archetype = plan.get("archetype", "custom_webapp")

        component_manifest = {
            "hotel_booking": [
                {"name": "HeaderNav", "file": "src/components/HeaderNav.tsx", "purpose": "Navbar with brand logo, currency toggle, and quick contact"},
                {"name": "SearchBanner", "file": "src/components/SearchBanner.tsx", "purpose": "Interactive check-in/out date picker, guest counter, and search trigger"},
                {"name": "RoomCard", "file": "src/components/RoomCard.tsx", "purpose": "Displays room image, rating, badges, price, and 'Book Now' trigger"},
                {"name": "BookingModal", "file": "src/components/BookingModal.tsx", "purpose": "Interactive reservation form with night calculation, tax, and instant confirmation modal"},
                {"name": "AmenitiesGrid", "file": "src/components/AmenitiesGrid.tsx", "purpose": "Interactive filter pills for WiFi, Pool, Spa, Breakfast, Gym"}
            ],
            "ecommerce": [
                {"name": "Navbar", "file": "src/components/Navbar.tsx", "purpose": "Header with search input, category links, and Cart badge count indicator"},
                {"name": "ProductGrid", "file": "src/components/ProductGrid.tsx", "purpose": "Responsive product catalog with category filter tabs and price sorting"},
                {"name": "CartDrawer", "file": "src/components/CartDrawer.tsx", "purpose": "Slide-over shopping cart with quantity increment/decrement and price total"},
                {"name": "CheckoutModal", "file": "src/components/CheckoutModal.tsx", "purpose": "Interactive checkout dialog with shipping form and order confirmation"},
                {"name": "AdminDashboard", "file": "src/components/AdminDashboard.tsx", "purpose": "Toggleable admin view with revenue metrics, chart stats, and inventory manager"}
            ],
            "portfolio": [
                {"name": "HeroSection", "file": "src/components/HeroSection.tsx", "purpose": "Modern developer intro with CTA buttons and social links"},
                {"name": "ProjectGallery", "file": "src/components/ProjectGallery.tsx", "purpose": "Interactive project cards with technology tag filtering"},
                {"name": "SkillMatrix", "file": "src/components/SkillMatrix.tsx", "purpose": "Visual proficiency meters for Frontend, Backend, DevOps"},
                {"name": "ContactForm", "file": "src/components/ContactForm.tsx", "purpose": "Validated contact submission with instant feedback alert"}
            ],
            "task_manager": [
                {"name": "KanbanBoard", "file": "src/components/KanbanBoard.tsx", "purpose": "Three column Kanban layout (To Do, In Progress, Done)"},
                {"name": "TaskCard", "file": "src/components/TaskCard.tsx", "purpose": "Movable card with priority tags, assignee avatar, and status toggle"},
                {"name": "NewTaskModal", "file": "src/components/NewTaskModal.tsx", "purpose": "Creation dialog with title, description, and priority selection"}
            ]
        }

        components = component_manifest.get(archetype, component_manifest["ecommerce"])

        return {
            "archetype": archetype,
            "components": components,
            "styling_framework": "Tailwind CSS v3",
            "state_management": "React hooks (useState, useEffect, useMemo)",
            "frontend_code_ready": True
        }
