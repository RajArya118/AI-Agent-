import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

def search_web(query: str, max_results: int = 5) -> Dict[str, Any]:
    """
    Perform a web search using DuckDuckGo search without requiring a paid API key.
    Returns a structured dictionary of search results (title, snippet, url).
    """
    query = query.strip()
    if not query:
        return {"status": "error", "error": "Search query cannot be empty"}

    try:
        from duckduckgo_search import DDGS
        ddgs = DDGS()
        raw_results = list(ddgs.text(query, max_results=max_results))
        
        results: List[Dict[str, str]] = []
        for item in raw_results:
            results.append({
                "title": item.get("title", "Untitled"),
                "snippet": item.get("body", item.get("snippet", "")),
                "url": item.get("href", item.get("link", ""))
            })

        if not results:
            return {
                "status": "success",
                "query": query,
                "results": [],
                "message": f"No web search results found for '{query}'."
            }

        return {
            "status": "success",
            "query": query,
            "count": len(results),
            "results": results
        }
    except Exception as e:
        logger.warning(f"DuckDuckGo search error: {e}")
        # Graceful fallback simulation or message
        return {
            "status": "partial_fallback",
            "query": query,
            "error": f"Live web search encountered an issue: {str(e)}",
            "results": [
                {
                    "title": f"DuckDuckGo Query Reference for '{query}'",
                    "snippet": f"The query '{query}' was processed. Check network connection or retry in a few moments.",
                    "url": f"https://duckduckgo.com/?q={query.replace(' ', '+')}"
                }
            ]
        }
