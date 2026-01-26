from fastapi import FastAPI
from pydantic import BaseModel
import chromadb
from sklearn.feature_extraction.text import TfidfVectorizer

app = FastAPI(title="Mini RAG Demo")

# 1️⃣ Load Chroma (persistent)
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("docs")

# 2️⃣ Dữ liệu gốc (PHẢI GIỐNG ingest)
docs = [
    "Saga đảm bảo tính nhất quán dữ liệu trong hệ thống phân tán.",
    "Event-driven architecture giúp hệ thống chịu lỗi tốt hơn.",
    "Transaction cần đảm bảo atomicity và consistency."
]

vectorizer = TfidfVectorizer()
vectorizer.fit(docs)

# 3️⃣ Request schema
class SearchRequest(BaseModel):
    query: str
    top_k: int = 2

# 4️⃣ API search
@app.post("/rag/search")
def search(req: SearchRequest):
    query_vector = vectorizer.transform([req.query]).toarray()[0]

    results = collection.query(
        query_embeddings=[query_vector.tolist()],
        n_results=req.top_k
    )

    return {
        "query": req.query,
        "results": results["documents"][0]
    }
