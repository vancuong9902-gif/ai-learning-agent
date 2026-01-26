from sklearn.feature_extraction.text import TfidfVectorizer
import chromadb

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("docs")

query = "đảm bảo tính nhất quán trong giao dịch"

docs = [
    "Saga đảm bảo tính nhất quán dữ liệu trong hệ thống phân tán.",
    "Event-driven architecture giúp hệ thống chịu lỗi tốt hơn.",
    "Transaction cần đảm bảo atomicity và consistency."
]

vectorizer = TfidfVectorizer()
vectorizer.fit(docs)

query_vector = vectorizer.transform([query]).toarray()[0]

results = collection.query(
    query_embeddings=[query_vector.tolist()],
    n_results=2
)

print("KẾT QUẢ:")
for doc in results["documents"][0]:
    print("-", doc)
