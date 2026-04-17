from __future__ import annotations

from collections import Counter
from typing import Any

from rapidfuzz import fuzz

from app.core.config import get_settings
from app.db.qdrant_client import search_claims
from app.schemas.verify import (
    EvidenceBlock,
    FamilyTreeNode,
    SimilarMatch,
    VerifyResponse,
    VisualMeter,
)
from app.services.gemini_service import summarize_verdict
from app.services.live_search import google_custom_search
from app.utils.text import clean_for_storage, detect_language_mode, heuristics


async def verify_content(text: str, explain_tone: str = "simple", image_extracted_text: str | None = None) -> VerifyResponse:
    settings = get_settings()
    normalized = clean_for_storage(text)
    language_mode = detect_language_mode(normalized)
    qdrant_result = search_claims(normalized, limit=settings.top_k)
    points = qdrant_result.points if hasattr(qdrant_result, "points") else []

    matches: list[SimilarMatch] = []
    family_tree: list[FamilyTreeNode] = []
    label_counter: Counter = Counter()
    match_ids: list[str] = []

    top_score = 0.0
    best_label = "unverified"
    best_payload: dict[str, Any] = {}

    for idx, point in enumerate(points):
        payload = point.payload or {}
        score = float(point.score or 0.0)
        label = payload.get("label", "unknown")
        title = payload.get("title", "Untitled claim")
        match_ids.append(str(point.id))
        label_counter[label] += 1
        matches.append(
            SimilarMatch(
                id=str(point.id),
                title=title,
                label=label,
                score=round(score, 3),
                source=payload.get("source"),
                published_at=payload.get("published_at"),
                url=payload.get("url"),
                snippet=payload.get("snippet") or payload.get("text", "")[:160],
            )
        )
        if idx == 0:
            top_score = score
            best_label = label
            best_payload = payload
            family_tree = [
                FamilyTreeNode(
                    id=str(node.get("id")),
                    title=node.get("title", "Untitled variation"),
                    label=node.get("label", label),
                    year=node.get("year"),
                    variation_note=node.get("variation_note"),
                    similarity=node.get("similarity"),
                )
                for node in payload.get("family_tree", [])
            ]

    hz = heuristics(normalized)
    heuristic_fake_boost = min(0.15, hz["caps_ratio"] * 0.2 + hz["exclamations"] * 0.01 + hz["has_free"] * 0.05 + hz["has_urgent"] * 0.05)

    fake_anchor = 0.0
    if best_label in {"fake", "scam", "misleading"}:
        fake_anchor = 0.65
    elif best_label == "real":
        fake_anchor = 0.15
    elif best_label == "satire":
        fake_anchor = 0.4
    else:
        fake_anchor = 0.45

    lexical_bonus = 0.0
    if best_payload.get("text"):
        lexical_bonus = fuzz.partial_ratio(normalized.lower(), str(best_payload.get("text", "")).lower()) / 1000

    fake_probability = min(0.99, max(0.01, fake_anchor * top_score + heuristic_fake_boost + lexical_bonus))
    confidence = max(top_score, min(0.95, 0.45 + len(matches) * 0.05))

    live_search = {"used": False, "summary": None, "items": []}
    if top_score < settings.low_confidence_threshold:
        live_search = await google_custom_search(normalized[:180])

    if fake_probability >= 0.75:
        verdict = "Likely Fake"
    elif fake_probability >= 0.55:
        verdict = "Suspicious"
    elif fake_probability <= 0.3 and best_label == "real":
        verdict = "Likely Real"
    else:
        verdict = "Needs More Evidence"

    credibility_score = round(max(0.0, min(100.0, (1 - fake_probability) * 100)), 1)
    visual_meter = VisualMeter(
        fake_probability=round(fake_probability, 3),
        credibility_score=credibility_score,
        verdict_color="green" if credibility_score >= 70 else "yellow" if credibility_score >= 40 else "red",
        trust_band="High" if credibility_score >= 70 else "Medium" if credibility_score >= 40 else "Low",
    )

    evidence = EvidenceBlock(
        qdrant_score=round(top_score, 3),
        matched_label_distribution=dict(label_counter),
        matched_claim_ids=match_ids,
        live_search_used=bool(live_search.get("used")),
        live_search_summary=live_search.get("summary"),
    )

    llm_payload = {
        "verdict": verdict,
        "language_mode": language_mode,
        "normalized_input": normalized,
        "family_tree": [node.model_dump() for node in family_tree],
        "evidence": evidence.model_dump(),
        "best_match": matches[0].model_dump() if matches else None,
        "credibility_score": credibility_score,
        "fake_probability": round(fake_probability, 3),
        "explain_tone": explain_tone,
    }
    summary = summarize_verdict(llm_payload)

    return VerifyResponse(
        verdict=verdict,
        short_verdict=summary["short_verdict"],
        explanation=summary["explanation"],
        language_mode=language_mode,
        credibility_score=credibility_score,
        fake_probability=round(fake_probability, 3),
        confidence=round(confidence, 3),
        visual_meter=visual_meter,
        family_tree=family_tree,
        similar_matches=matches,
        evidence=evidence,
        normalized_input=normalized,
        extracted_text_from_image=image_extracted_text,
        raw_llm_summary=summary["explanation"],
        debug={"heuristics": hz, "best_label": best_label, "top_k": len(matches)},
    )
