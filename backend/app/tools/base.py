from typing import Callable, Dict, Any, List
import inspect

class Tool:
    def __init__(
        self,
        name: str,
        description: str,
        parameters: Dict[str, Any],
        func: Callable,
        requires_confirmation: bool = False
    ):
        self.name = name
        self.description = description
        self.parameters = parameters
        self.func = func
        self.requires_confirmation = requires_confirmation

    def to_gemini_declaration(self) -> Dict[str, Any]:
        """Convert tool definition to Gemini function declaration schema."""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters
        }

    async def execute(self, **kwargs) -> Any:
        if inspect.iscoroutinefunction(self.func):
            return await self.func(**kwargs)
        return self.func(**kwargs)

class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, Tool] = {}

    def register(self, tool: Tool):
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool:
        return self._tools.get(name)

    def list_tools(self) -> List[Tool]:
        return list(self._tools.values())

    def get_gemini_declarations(self) -> List[Dict[str, Any]]:
        return [tool.to_gemini_declaration() for tool in self._tools.values()]

registry = ToolRegistry()
