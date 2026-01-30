import sqlite3
from embedding.embedder import embed_text
from vector_db.client import collection


def vectorize_all():
    conn = sqlite3.connect("storage/data.db")
    cur = conn.cursor()

    # ❗ SỬA text → content
    cur.execute("SELECT doc_id, chunk_id, page, content FROM chunks")
    rows = cur.fetchall()

    print(f"📄 TOTAL CHUNKS FROM DB: {len(rows)}")

    for doc_id, chunk_id, page, content in rows:
        if not content or not content.strip():
            continue  # tránh rác

        collection.add(
            ids=[f"{doc_id}_{chunk_id}"],
            documents=[content],
            embeddings=[embed_text(content)],
            metadatas=[{
                "doc_id": doc_id,
                "chunk_id": chunk_id,
                "page": page
            }]
        )

    conn.close()
    print("✅ VECTORIZE DONE")
if __name__ == "__main__":
    vectorize_all()
