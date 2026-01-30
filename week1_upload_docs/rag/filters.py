def apply_filters(results, doc_id=None, threshold=0.3):
    filtered = []
    for r in results:
        if doc_id and r["doc_id"] != doc_id:
            continue
        if r["score"] > threshold:
            continue
        filtered.append(r)
    return filtered
