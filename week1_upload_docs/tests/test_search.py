from vector_db.client import collection
from rag.search import search_chunks

print("=== DEBUG CHROMA ===")
print("COLLECTION NAME:", collection.name)
print("COUNT:", collection.count())

print("\n=== RUN SEARCH ===")
results = search_chunks("machine learning", top_k=3)

print("TOTAL RESULTS:", len(results))

for r in results:
    print("----")
    print(r["score"])
    print(r["content"][:200])
