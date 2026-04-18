from __future__ import annotations

import json
from typing import Any

from google import genai
from google.genai import types

from app.core.config import get_settings


SYSTEM_PROMPT = """
You are SachAI, a misinformation safety assistant for India.
Explain the verdict in extremely simple, friendly language.
Rules:
1. Sound like a careful fact-check volunteer, not a legal notice.
2. Support Hindi, Tamil, English, and Hinglish.
3. Keep it concise but useful.
4. Mention what raised suspicion, what matched in history, and what the user should do next.
5. Provide a 'consequences' section: What happens if people believe this? (e.g. financial loss, panic, health risks).
6. Provide a 'social_impact' section: How does this affect community harmony or public trust?
7. Never claim certainty when evidence is weak.
Return valid JSON with keys: short_verdict, explanation, consequences, social_impact.
""".strip()


def _fallback_summary(payload: dict[str, Any]) -> dict[str, str]:
    verdict = payload["verdict"]
    evidence = payload.get("evidence", {})
    q_score = evidence.get("qdrant_score", 0)
    family_count = len(payload.get("family_tree", []))
    matched_ids = evidence.get("matched_claim_ids", []) or []
    live_summary = evidence.get("live_search_summary") or ""
    input_text = (payload.get("normalized_input") or "").strip()
    input_preview = input_text[:140] + ("..." if len(input_text) > 140 else "")
    lang = payload.get("language_mode", "en")

    if verdict == "Likely Fake":
        consequences_en = "People may lose money, panic, or act on harmful misinformation."
        social_en = "Sharing this can trigger fear and weaken trust in verified public sources."
        consequences_hi = "Log paisa kho sakte hain, ghabrahat fail sakti hai, aur log galat kadam le sakte hain."
        social_hi = "Isse samaj me darr failta hai aur sahi soochna par bharosa kam hota hai."
    elif verdict == "Suspicious":
        consequences_en = "This may mislead people into poor decisions if forwarded as fact."
        social_en = "Repeated circulation of unclear claims creates confusion and mistrust."
        consequences_hi = "Agar ise sach maan kar share kiya gaya to log galat faisle le sakte hain."
        social_hi = "Bar-bar aisi aspasht baatein failne se uljhan aur avishwas badhta hai."
    elif verdict == "Likely Real":
        consequences_en = "Risk appears low, but context can still change and old claims can resurface incorrectly."
        social_en = "Responsible sharing helps improve public trust and reduces rumor spread."
        consequences_hi = "Risk kam lagta hai, lekin context badal sakta hai aur purani baat galat tareeke se phir fail sakti hai."
        social_hi = "Jaanch kar share karna public trust badhata hai aur afwaah kam karta hai."
    else:
        consequences_en = "Unverified claims can still cause confusion, panic, or bad decisions."
        social_en = "Waiting for verification helps protect community trust."
        consequences_hi = "Bina verify kiye claims se uljhan, ghabrahat ya galat faisle ho sakte hain."
        social_hi = "Verify karke share karna samudaayik bharosa banaye rakhta hai."

    support_bits = [
        f"similarity {q_score:.2f}",
        f"matched claims {len(matched_ids)}",
        f"family links {family_count}",
    ]
    if live_summary:
        support_bits.append(f"web signal: {live_summary[:140]}")
    support_line = "; ".join(support_bits)

    if lang == "hinglish":
        explanation = (
            f"Claim check: \"{input_preview or 'N/A'}\"\n"
            f"Verdict: {verdict}. Evidence: {support_line}. "
            "Forward karne se pehle source ki pushti zarur karein."
        )
        consequences = consequences_hi
        social_impact = social_hi
    else:
        explanation = (
            f"Claim checked: \"{input_preview or 'N/A'}\"\n"
            f"Verdict: {verdict}. Evidence signals: {support_line}. "
            "Please verify with a reliable source before forwarding."
        )
        consequences = consequences_en
        social_impact = social_en
    return {
        "short_verdict": verdict, 
        "explanation": explanation,
        "consequences": consequences,
        "social_impact": social_impact
    }


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
            "consequences": data.get("consequences") or _fallback_summary(payload)["consequences"],
            "social_impact": data.get("social_impact") or _fallback_summary(payload)["social_impact"],
        }
    except Exception as e:
        import logging
        logging.error(f"Gemini API Error: {str(e)}")
        return _fallback_summary(payload)
