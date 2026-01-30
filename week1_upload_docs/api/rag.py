from fastapi import APIRouter
from rag.search import search
from rag.filters import apply_filters
from rag.ask import answer

router = APIRouter()

@router.get("/search")
def rag_search(q: str, top_k: int = 5, doc_id: str | None = None):
    results = search(q, top_k)

    # CHỈ FILTER KHI CÓ doc_id
    if doc_id:
        results = apply_filters(results, doc_id)

    return results


@router.get("/ask")
def rag_ask(q: str):
    results = search(q, 5)
    return {
        "answer": answer(q, results),
        "sources": results
    }
