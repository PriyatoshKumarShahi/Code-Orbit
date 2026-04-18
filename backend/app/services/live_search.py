from __future__ import annotations

import httpx

from app.core.config import get_settings


async def google_custom_search(query: str) -> dict:
    settings = get_settings()
    if not settings.google_search_api_key or not settings.google_search_engine_id:
        return {
            "used": False,
            "summary": "Live web verification skipped because Google Custom Search credentials are not configured.",
            "items": [],
        }

    params = {
        "key": settings.google_search_api_key,
        "cx": settings.google_search_engine_id,
        "q": query,
        "num": 5,
    }
    try:
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.get("https://www.googleapis.com/customsearch/v1", params=params)
            response.raise_for_status()
            data = response.json()

        items = [
            {
                "title": item.get("title"),
                "link": item.get("link"),
                "snippet": item.get("snippet"),
            }
            for item in data.get("items", [])
        ]
    except Exception as e:
        return {
            "used": False,
            "summary": f"Live search failed: {str(e)}",
            "items": [],
        }

    if not items:
        return {
            "used": True,
            "summary": "Live search ran, but no strong public results were returned.",
            "items": [],
        }

    summary = " | ".join(f"{idx+1}. {item['title']}: {item['snippet']}" for idx, item in enumerate(items[:3]))
    return {"used": True, "summary": summary, "items": items}
