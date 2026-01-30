from typing import List
from sentence_transformers import SentenceTransformer

print(">>> embedder.py LOADED")  # debug xem file có chạy không

# Load model 1 lần duy nhất
model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_text(text: str) -> List[float]:
    return model.encode(text).tolist()


# ===== EMBEDDING FUNCTION CHUẨN CHO CHROMA >= 0.4.16 =====
class ChromaEmbeddingFunction:
    def __call__(self, input: List[str]) -> List[List[float]]:
        # ⚠️ tên tham số BẮT BUỘC là "input"
        return model.encode(input).tolist()

    def name(self) -> str:
        return "sentence-transformers-all-MiniLM-L6-v2"


def get_embedding_function():
    return ChromaEmbeddingFunction()


if __name__ == "__main__":
    print(">>> RUNNING MAIN TEST")
    emb = embed_text("hello world")
    print("Vector length:", len(emb))
    print("First 5 values:", emb[:5])
