from typing import Any, Literal

from pydantic import BaseModel, Field


class SimilarMatch(BaseModel):
    id: str
    title: str
    label: str
    score: float
    source: str | None = None
    published_at: str | None = None
    url: str | None = None
    snippet: str | None = None


class FamilyTreeNode(BaseModel):
    id: str
    title: str
    label: str
    year: int | None = None
    variation_note: str | None = None
    similarity: float | None = None


class EvidenceBlock(BaseModel):
    qdrant_score: float = 0.0
    matched_label_distribution: dict[str, int] = Field(default_factory=dict)
    matched_claim_ids: list[str] = Field(default_factory=list)
    live_search_used: bool = False
    live_search_summary: str | None = None


class VisualMeter(BaseModel):
    fake_probability: float
    credibility_score: float
    verdict_color: Literal["red", "yellow", "green"]
    trust_band: Literal["Low", "Medium", "High"]


class VerifyRequest(BaseModel):
    text: str | None = None
    mode: Literal["text", "image"] = "text"
    explain_tone: Literal["simple", "mentor-demo"] = "simple"


class VerifyResponse(BaseModel):
    verdict: Literal["Likely Fake", "Suspicious", "Likely Real", "Needs More Evidence"]
    short_verdict: str
    explanation: str
    language_mode: str
    credibility_score: float
    fake_probability: float
    confidence: float
    visual_meter: VisualMeter
    family_tree: list[FamilyTreeNode]
    similar_matches: list[SimilarMatch]
    evidence: EvidenceBlock
    normalized_input: str
    extracted_text_from_image: str | None = None
    raw_llm_summary: str | None = None
    consequences: str | None = None
    social_impact: str | None = None
    community_flags: int = 0
    debug: dict[str, Any] | None = None
