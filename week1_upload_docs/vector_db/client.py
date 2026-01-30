import chromadb
from chromadb.config import Settings
from embedding.embedder import get_embedding_function
from pathlib import Path

_client = None
_collection = None

BASE_DIR = Path(__file__).resolve().parent.parent
CHROMA_DIR = BASE_DIR / "storage" / "chroma"

def get_vector_db():
    global _client, _collection

    if _collection is None:
        embedding_fn = get_embedding_function()

        _client = chromadb.PersistentClient(
            path=str(CHROMA_DIR),
            settings=Settings(anonymized_telemetry=False)
        )

        _collection = _client.get_or_create_collection(
            name="documents",
            embedding_function=embedding_fn
        )

    return _collection


collection = get_vector_db()
print(">>> Chroma collection READY")
print("📦 CHROMA DIR =", CHROMA_DIR)
