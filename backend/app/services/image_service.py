from __future__ import annotations

import base64
from io import BytesIO

from PIL import Image

from app.core.config import get_settings


def image_bytes_to_text(file_bytes: bytes, mime_type: str) -> str:
    """
    Minimal image pipeline.
    If Gemini is configured, backend/api route will pass the image separately.
    For local/offline mode this function just returns a placeholder note.
    """
    try:
        image = Image.open(BytesIO(file_bytes))
        return f"Image uploaded ({image.width}x{image.height}). Configure Gemini vision in production to extract embedded text and context."
    except Exception:
        return "Image uploaded. Configure Gemini vision in production to extract embedded text and context."


def image_to_base64(file_bytes: bytes) -> str:
    return base64.b64encode(file_bytes).decode("utf-8")
