import re
from html import unescape
from unidecode import unidecode


SPACE_RE = re.compile(r"\s+")
URL_RE = re.compile(r"https?://\S+|www\.\S+", re.IGNORECASE)
PUNCT_RE = re.compile(r"[\u200b\ufeff]")


HINDI_HINTS = {"hai", "nahi", "kya", "dhyan", "dekho", "sach", "jhooth", "modi", "sarkar", "free", "link"}
TAMIL_RANGE = re.compile(r"[\u0B80-\u0BFF]")
DEVANAGARI_RANGE = re.compile(r"[\u0900-\u097F]")


def normalize_text(text: str) -> str:
    text = unescape(text or "")
    text = PUNCT_RE.sub(" ", text)
    text = text.replace("\n", " ").replace("\r", " ")
    text = SPACE_RE.sub(" ", text).strip()
    return text


def clean_for_embedding(text: str) -> str:
    text = normalize_text(text)
    return f"query: {text}"


def clean_for_storage(text: str) -> str:
    return normalize_text(text)


def detect_language_mode(text: str) -> str:
    normalized = normalize_text(text).lower()
    ascii_version = unidecode(normalized)
    if TAMIL_RANGE.search(normalized):
        return "ta"
    if DEVANAGARI_RANGE.search(normalized):
        return "hi"
    if any(token in ascii_version.split() for token in HINDI_HINTS) and re.search(r"[a-z]", ascii_version):
        return "hinglish"
    return "en"


def extract_urls(text: str) -> list[str]:
    return URL_RE.findall(text or "")


def heuristics(text: str) -> dict:
    normalized = normalize_text(text)
    alpha = max(sum(ch.isalpha() for ch in normalized), 1)
    caps_ratio = sum(ch.isupper() for ch in normalized) / alpha
    exclamations = normalized.count("!")
    has_free = int("free" in normalized.lower())
    has_urgent = int(any(k in normalized.lower() for k in ["urgent", "immediately", "last chance", "act now", "limited"]))
    url_count = len(extract_urls(normalized))
    return {
        "caps_ratio": round(caps_ratio, 3),
        "exclamations": exclamations,
        "has_free": has_free,
        "has_urgent": has_urgent,
        "url_count": url_count,
    }
