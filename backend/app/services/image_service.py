from __future__ import annotations

import base64
from io import BytesIO

from PIL import Image
from google import genai

from app.core.config import get_settings


def image_bytes_to_text(file_bytes: bytes, mime_type: str) -> str:
    """
    Extracts text and claims from an image using Gemini Vision.
    """
    settings = get_settings()
    try:
        image = Image.open(BytesIO(file_bytes))
        
        if settings.gemini_api_key:
            client = genai.Client(api_key=settings.gemini_api_key)
            prompt = (
                "Extract any readable text and describe the core claims or statements "
                "made in this image. Do not invent information. Just describe what you see."
            )
            response = client.models.generate_content(
                model=settings.gemini_model,
                contents=[image, prompt],
            )
            return response.text or "No text extracted."
            
        return f"Image uploaded ({image.width}x{image.height}). Configure Gemini vision in production to extract embedded text and context."
    except Exception as e:
        return f"Image uploaded but could not be processed. Error: {str(e)}"


def image_to_base64(file_bytes: bytes) -> str:
    return base64.b64encode(file_bytes).decode("utf-8")
