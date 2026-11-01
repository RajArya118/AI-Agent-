from app.tools.base import Tool, registry
from app.tools.calculator import safe_calculate
from app.tools.web_search import search_web
from app.tools.doc_reader import read_document_content
from app.tools.action_tool import request_consequential_action

# Calculator Tool
calculator_tool = Tool(
    name="calculator",
    description="Perform mathematical calculations safely (arithmetic, percentages, powers, roots, trigonometry, logarithms, factorials). Always use this tool for any math questions to ensure exact precision.",
    parameters={
        "type": "object",
        "properties": {
            "expression": {
                "type": "string",
                "description": "The mathematical expression to evaluate, e.g., '125 * 45 + sqrt(144)' or 'sin(pi/2)'"
            }
        },
        "required": ["expression"]
    },
    func=lambda expression: safe_calculate(expression)
)

# Web Search Tool
web_search_tool = Tool(
    name="web_search",
    description="Search the live web for recent information, facts, current events, weather, news, definitions, or references. Use this tool whenever you need up-to-date external information.",
    parameters={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The search query keywords"
            },
            "max_results": {
                "type": "integer",
                "description": "Maximum number of search results to retrieve (default 5)"
            }
        },
        "required": ["query"]
    },
    func=lambda query, max_results=5: search_web(query, max_results=max_results)
)

# Document Reader Tool
doc_reader_tool = Tool(
    name="read_document",
    description="Read the contents or search excerpts of an uploaded document (PDF or TXT) by its document_id.",
    parameters={
        "type": "object",
        "properties": {
            "document_id": {
                "type": "string",
                "description": "The unique ID of the uploaded document to read"
            },
            "query": {
                "type": "string",
                "description": "Optional search term or keyword to find relevant sections in the document"
            }
        },
        "required": ["document_id"]
    },
    func=lambda document_id, query=None, db=None: read_document_content(document_id, db, query=query)
)

# Register tools
registry.register(calculator_tool)
registry.register(web_search_tool)
registry.register(doc_reader_tool)

__all__ = ["registry", "calculator_tool", "web_search_tool", "doc_reader_tool"]
