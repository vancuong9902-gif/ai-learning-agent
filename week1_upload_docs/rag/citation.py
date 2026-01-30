def cite(text, meta, score):
    return {
        "doc_id": meta["doc_id"],
        "chunk_id": meta["chunk_id"],
        "page": meta.get("page"),
        "score": score,
        "snippet": text[:200] + "..."
    }
