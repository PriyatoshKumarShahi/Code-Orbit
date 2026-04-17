from __future__ import annotations

import json
from typing import Any

from google import genai
from google.genai import types

from app.core.config import get_settings


SYSTEM_PROMPT = """
You are Veritas-AI, a misinformation safety assistant for India.
Explain the verdict in extremely simple, friendly language.
Rules:
1. Sound like a careful fact-check volunteer, not a legal notice.
2. Support Hindi, Tamil, English, and Hinglish.
3. Keep it concise but useful.
4. Mention what raised suspicion, what matched in history, and what the user should do next.
5. Never claim certainty when evidence is weak.
Return valid JSON with keys: short_verdict, explanation.
""".strip()


def _fallback_summary(payload: dict[str, Any]) -> dict[str, str]:
    verdict = payload["verdict"]
    q_score = payload["evidence"].get("qdrant_score", 0)
    family_count = len(payload.get("family_tree", []))
    lang = payload.get("language_mode", "en")
    if lang == "hinglish":
        explanation = (
            f"Dhyan dein! Yeh message {verdict.lower()} lag raha hai. "
            f"Hamare database me iska similarity score {q_score:.2f} mila aur {family_count} purane versions bhi mile. "
            "Link ya forward ko bina verify kiye share mat kariye."
        )
    else:
        explanation = (
            f"This looks {verdict.lower()}. We found a similarity score of {q_score:.2f} and matched it with "
            f"{family_count} earlier versions. Please avoid forwarding it until you verify the source."
        )
    return {"short_verdict": verdict, "explanation": explanation}


def summarize_verdict(payload: dict[str, Any]) -> dict[str, str]:
    settings = get_settings()
    if not settings.gemini_api_key:
        return _fallback_summary(payload)

    client = genai.Client(api_key=settings.gemini_api_key)
    prompt = json.dumps(payload, ensure_ascii=False)
    try:
        response = client.models.generate_content(
            model=settings.gemini_model,
            config=types.GenerateContentConfig(
                temperature=0.3,
                response_mime_type="application/json",
                system_instruction=SYSTEM_PROMPT,
            ),
            contents=prompt,
        )
        text = response.text or "{}"
        data = json.loads(text)
        return {
            "short_verdict": data.get("short_verdict") or payload["verdict"],
            "explanation": data.get("explanation") or _fallback_summary(payload)["explanation"],
        }
    except Exception:
        return _fallback_summary(payload)
