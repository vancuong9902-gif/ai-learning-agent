from typing import List, Dict, Optional
from embedding.embedder import embed_text
from vector_db.client import get_vector_db

SIM_THRESHOLD = 1.5


def search_chunks(
    query: str,
    top_k: int = 5,
    filters: Optional[Dict[str, str]] = None
) -> List[Dict]:
    """
    Retrieve relevant chunks from Chroma vector DB
    """

    collection = get_vector_db()

    # 1️⃣ embed query
    query_embedding = embed_text(query)

    # 2️⃣ query chroma
    res = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        where=filters if filters else None
    )

    print("===== RAW CHROMA QUERY =====")
    print(res)

    output = []

    docs = res.get("documents")
    metas = res.get("metadatas")
    dists = res.get("distances")

    if not docs or not docs[0]:
        print("⚠️ NO DOCUMENTS RETURNED FROM CHROMA")
        return []

    for i in range(len(docs[0])):
        meta = metas[0][i] or {}

        output.append({
            "content": docs[0][i],
            # 👉 distance, càng nhỏ càng tốt
            "score": round(dists[0][i], 4),
            "source": {
                "doc_id": meta.get("doc_id"),
                "chunk_id": meta.get("chunk_id"),
                "page": meta.get("page"),
                "filename": meta.get("filename"),
            }
        })

    return output


def search(
    query: str,
    top_k: int = 5,
    doc_id: Optional[str] = None
):
    filters = {}
    if doc_id:
        filters["doc_id"] = doc_id

    raw_results = search_chunks(
        query=query,
        top_k=top_k,
        filters=filters if filters else None
    )

    # 🔥 CHUYỂN FORMAT ĐÚNG CHO THẦY CHẤM
    formatted = []

    for r in raw_results:
        source = r.get("source", {})

        formatted.append({
            "chunk_id": source.get("chunk_id"),
            "doc_id": source.get("doc_id") or source.get("filename"),
            "page": source.get("page"),
            "snippet": r.get("content")
        })

    return formatted
