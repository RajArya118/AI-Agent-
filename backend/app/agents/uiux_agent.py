from typing import Dict, Any
from app.agents.base_agent import BaseSpecialistAgent

class UIUXAgent(BaseSpecialistAgent):
    def __init__(self):
        super().__init__(
            name="UI/UX Agent",
            role="Lead Product & Interaction Designer",
            description="Designs modern design systems, color tokens, responsive wireframes, and interactive user micro-interactions."
        )

    async def _run(self, context: Dict[str, Any], gemini_client=None) -> Dict[str, Any]:
        plan = context.get("plan", {})
        archetype = plan.get("archetype", "custom_webapp")

        # Archetype-specific design system
        palettes = {
            "hotel_booking": {
                "primary": "#0f766e",      # Teal
                "primary_hover": "#115e59",
                "accent": "#f59e0b",       # Amber for stars & amenities
                "background": "#f8fafc",
                "card_bg": "#ffffff",
                "text": "#0f172a"
            },
            "ecommerce": {
                "primary": "#4f46e5",      # Indigo
                "primary_hover": "#4338ca",
                "accent": "#10b981",       # Emerald for checkout & discounts
                "background": "#f9fafb",
                "card_bg": "#ffffff",
                "text": "#111827"
            },
            "portfolio": {
                "primary": "#2563eb",      # Royal Blue
                "primary_hover": "#1d4ed8",
                "accent": "#8b5cf6",       # Purple
                "background": "#0f172a",   # Dark aesthetic default
                "card_bg": "#1e293b",
                "text": "#f8fafc"
            },
            "task_manager": {
                "primary": "#0284c7",      # Sky Blue
                "primary_hover": "#0369a1",
                "accent": "#ef4444",       # Red priority tags
                "background": "#f1f5f9",
                "card_bg": "#ffffff",
                "text": "#0f172a"
            }
        }

        color_system = palettes.get(archetype, palettes["ecommerce"])

        design_tokens = {
            "archetype": archetype,
            "color_system": color_system,
            "typography": {
                "font_family_sans": "Inter, system-ui, sans-serif",
                "font_family_mono": "JetBrains Mono, monospace",
                "scale": {
                    "xs": "0.75rem",
                    "sm": "0.875rem",
                    "base": "1rem",
                    "lg": "1.125rem",
                    "xl": "1.25rem",
                    "2xl": "1.5rem",
                    "3xl": "1.875rem"
                }
            },
            "viewports": {
                "mobile_sm": "360px",
                "mobile_md": "390px",
                "tablet": "768px",
                "laptop": "1024px",
                "desktop": "1440px"
            },
            "layout_structure": {
                "navigation": "Sticky top bar with responsive mobile slide-out drawer",
                "content_container": "max-w-7xl mx-auto px-4 sm:px-6 lg:px-8",
                "grid_system": "grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6",
                "card_elevation": "shadow-sm hover:shadow-md transition-shadow rounded-2xl border"
            },
            "interactive_patterns": [
                "Instant search bar with debounced filtering",
                "Dynamic tab/category switcher",
                "Modal overlays with smooth fade/scale transitions",
                "Badge tags with color-coded status pills",
                "Clear visual feedback on button taps and form submissions"
            ]
        }
        return design_tokens
