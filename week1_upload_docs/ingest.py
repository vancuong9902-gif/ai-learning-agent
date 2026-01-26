from sklearn.feature_extraction.text import TfidfVectorizer
import chromadb

# 1️⃣ Persistent Chroma Client
client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection("docs")

docs = [
    "Saga đảm bảo tính nhất quán dữ liệu trong hệ thống phân tán.",
    "Event-driven architecture giúp hệ thống chịu lỗi tốt hơn.",
    "Transaction cần đảm bảo atomicity và consistency."
]

vectorizer = TfidfVectorizer()
vectors = vectorizer.fit_transform(docs).toarray()

for i, text in enumerate(docs):
    collection.add(
        documents=[text],
        embeddings=[vectors[i].tolist()],
        ids=[str(i)]
    )

print("INGEST DONE (PERSIST AUTO)")
