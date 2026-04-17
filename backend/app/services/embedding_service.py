from functools import lru_cache

from sentence_transformers import SentenceTransformer

from app.utils.text import clean_for_embedding

MODEL_NAME = "intfloat/multilingual-e5-large"


@lru_cache(maxsize=1)
def get_embedding_model() -> SentenceTransformer:
    return SentenceTransformer(MODEL_NAME)


def embed_text(text: str) -> list[float]:
    model = get_embedding_model()
    vector = model.encode(clean_for_embedding(text), normalize_embeddings=True)
    return vector.tolist()


def embedding_size() -> int:
    return get_embedding_model().get_sentence_embedding_dimension()
