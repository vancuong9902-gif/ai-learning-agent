from vector_db.client import get_vector_db

col = get_vector_db()

print("COUNT =", col.count())

res = col.query(
    query_texts=["upload"],
    n_results=5
)

print(res)
