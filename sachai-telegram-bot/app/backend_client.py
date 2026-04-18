import httpx
from typing import Dict, Any, Optional
from app.config import Config
from app.logger import get_logger

logger = get_logger(__name__)

async def verify_text_with_backend(text: str) -> Optional[Dict[str, Any]]:
    """
    Sends the user's text to the SachAI backend for verification.
    Returns the JSON response as a dictionary, or None if it fails.
    """
    # Use the /api/v1/verify path as per the backend's setup
    url = f"{Config.SACH_AI_BACKEND_URL.rstrip('/')}/api/v1/verify"
    
    payload = {
        "text": text,
        "mode": "text",
        "explain_tone": "simple" # This tells backend to use the simple/hinglish persona
    }

    logger.info(f"Sending verification request to backend: {url}")
    
    try:
        async with httpx.AsyncClient(timeout=Config.REQUEST_TIMEOUT) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            logger.info("Successfully received verification from backend.")
            return data
            
    except httpx.HTTPStatusError as e:
        logger.error(f"Backend returned HTTP error: {e.response.status_code} - {e.response.text}")
        return None
    except httpx.RequestError as e:
        logger.error(f"Network error while connecting to backend: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error in backend client: {str(e)}")
        return None
