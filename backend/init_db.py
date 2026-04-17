from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

# Replace with your Cloud URL and Key
client = QdrantClient(url="YOUR_QDRANT_URL", api_key="YOUR_API_KEY")

client.create_collection(
    collection_name="sach_claims",
    vectors_config=VectorParams(size=1024, distance=Distance.COSINE), # 1024 for Multilingual-E5
)
print("Collection 'sach_claims' created successfully!")