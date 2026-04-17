from functools import lru_cache
from typing import Iterable

from qdrant_client import QdrantClient
from qdrant_client.http import models

from app.core.config import get_settings
from app.services.embedding_service import embedding_size, embed_text


@lru_cache(maxsize=1)
def get_qdrant_client() -> QdrantClient:
    settings = get_settings()
    return QdrantClient(url=settings.qdrant_url, api_key=settings.qdrant_api_key)


def ensure_collection() -> None:
    settings = get_settings()
    client = get_qdrant_client()
    existing = {c.name for c in client.get_collections().collections}
    if settings.qdrant_collection in existing:
        return
    client.create_collection(
        collection_name=settings.qdrant_collection,
        vectors_config=models.VectorParams(
            size=embedding_size(),
            distance=models.Distance.COSINE,
        ),
    )


def upsert_claims(records: Iterable[dict]) -> None:
    settings = get_settings()
    client = get_qdrant_client()
    ensure_collection()
    points = []
    for record in records:
        text = record["text"]
        vector = embed_text(text)
        payload = dict(record)
        payload["vector_model"] = "intfloat/multilingual-e5-large"
        points.append(models.PointStruct(id=record["id"], vector=vector, payload=payload))
    client.upsert(collection_name=settings.qdrant_collection, points=points)


def search_claims(query: str, limit: int = 5):
    settings = get_settings()
    ensure_collection()
    vector = embed_text(query)
    return get_qdrant_client().query_points(
        collection_name=settings.qdrant_collection,
        query=vector,
        limit=limit,
        with_payload=True,
    )
