import logging
from typing import List, Dict, Any, Optional
from app.core.config import settings

logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self):
        self.client = None
        self._init_client()

    def _init_client(self):
        if settings.is_gemini_configured:
            try:
                from google import genai
                self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
                logger.info(f"Initialized Google GenAI client with model {settings.GEMINI_MODEL}")
            except Exception as e:
                logger.error(f"Failed to initialize Google GenAI client: {e}")
                self.client = None
        else:
            self.client = None

    def is_available(self) -> bool:
        return self.client is not None

    async def call_gemini(
        self,
        prompt: str,
        system_instruction: str,
        history: List[Dict[str, Any]],
        tools: List[Any]
    ) -> Dict[str, Any]:
        """
        Execute a turn with Gemini.
        Returns a dict with:
        - 'content': str (assistant final text if no tools called or final synthesis)
        - 'tool_calls': List[Dict] (if Gemini requests tool calls)
        - 'raw_response': Any
        """
        if not self.is_available():
            raise RuntimeError("Gemini API client is not configured or GEMINI_API_KEY is missing.")

        try:
            from google.genai import types

            # Build tools configuration
            function_declarations = []
            for t in tools:
                declaration = types.FunctionDeclaration(
                    name=t.name,
                    description=t.description,
                    parameters=t.parameters
                )
                function_declarations.append(declaration)

            gemini_tools = [types.Tool(function_declarations=function_declarations)] if function_declarations else None

            # Format contents from history + current prompt
            contents = []
            for msg in history:
                role = "user" if msg["role"] == "user" else "model"
                contents.append(types.Content(
                    role=role,
                    parts=[types.Part.from_text(text=msg["content"])]
                ))

            # Append current user prompt
            contents.append(types.Content(
                role="user",
                parts=[types.Part.from_text(text=prompt)]
            ))

            config = types.GenerateContentConfig(
                system_instruction=system_instruction,
                tools=gemini_tools,
                temperature=0.7,
            )

            # Generate content
            response = self.client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=contents,
                config=config,
            )

            tool_calls = []
            text_parts = []

            # Check candidates and function calls
            if response.candidates and response.candidates[0].content:
                candidate = response.candidates[0].content
                for part in candidate.parts:
                    if part.function_call:
                        fc = part.function_call
                        args = dict(fc.args) if fc.args else {}
                        tool_calls.append({
                            "name": fc.name,
                            "arguments": args,
                            "id": getattr(fc, "id", None) or fc.name
                        })
                    elif part.text:
                        text_parts.append(part.text)

            combined_text = "\n".join(text_parts).strip()
            return {
                "content": combined_text,
                "tool_calls": tool_calls,
                "response": response
            }

        except Exception as e:
            logger.error(f"Error calling Gemini: {e}")
            raise e

    async def synthesize_tool_results(
        self,
        prompt: str,
        system_instruction: str,
        history: List[Dict[str, Any]],
        tools: List[Any],
        tool_name: str,
        tool_result: Any
    ) -> str:
        """
        Pass tool execution results back to Gemini to synthesize a natural language response.
        """
        try:
            from google.genai import types

            tool_result_str = str(tool_result)
            synthesis_prompt = f"""The user asked: "{prompt}"
The tool '{tool_name}' was executed and returned the following result:
{tool_result_str}

Please use this result to provide a clear, helpful, accurate answer to the user in Markdown format. Cite key numbers or facts directly from the result."""

            config = types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.7,
            )

            response = self.client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=[types.Content(role="user", parts=[types.Part.from_text(text=synthesis_prompt)])],
                config=config
            )
            return response.text or "Here is the result: " + tool_result_str

        except Exception as e:
            logger.error(f"Error in synthesize_tool_results: {e}")
            return f"Processed result from {tool_name}:\n```json\n{tool_result}\n```"

gemini_service = GeminiService()
