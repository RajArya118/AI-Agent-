import time
import json
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger("buildpilot.agents")

class BaseSpecialistAgent:
    def __init__(self, name: str, role: str, description: str):
        self.name = name
        self.role = role
        self.description = description
        self.retry_limit = 3

    async def execute(self, context: Dict[str, Any], gemini_client=None) -> Dict[str, Any]:
        """Base execution wrapper with timing, retry logic, and error containment."""
        start_time = time.perf_counter()
        attempts = 0
        last_error = None

        while attempts < self.retry_limit:
            attempts += 1
            try:
                result = await self._run(context, gemini_client)
                elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)
                return {
                    "agent": self.name,
                    "role": self.role,
                    "status": "completed",
                    "output": result,
                    "execution_time_ms": elapsed_ms,
                    "attempts": attempts,
                    "error": None
                }
            except Exception as e:
                last_error = str(e)
                logger.warning(f"Agent {self.name} attempt {attempts} failed: {e}")
                time.sleep(0.2)

        elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)
        return {
            "agent": self.name,
            "role": self.role,
            "status": "failed",
            "output": None,
            "execution_time_ms": elapsed_ms,
            "attempts": attempts,
            "error": last_error
        }

    async def _run(self, context: Dict[str, Any], gemini_client=None) -> Dict[str, Any]:
        raise NotImplementedError("Subclasses must implement _run()")
