from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, Dict
from rag.search import search_chunks

router = APIRouter()


class SearchRequest(BaseModel):
    query: str
    top_k: int = 5
    filters: Optional[Dict[str, str]] = None


@router.post("/rag/search")
def rag_search(req: SearchRequest):
    results = search_chunks(
        query=req.query,
        top_k=req.top_k,
        filters=req.filters
    )
    return {"results": results}
class AskRequest(BaseModel):
    query: str


@router.post("/rag/ask")
def rag_ask(req: AskRequest):
    results = search_chunks(req.query, top_k=3)

    answer = " ".join([r["snippet"] for r in results])
    sources = [
        {
            "doc_id": r["doc_id"],
            "chunk_id": r["chunk_id"],
            "page": r["page"]
        }
        for r in results
    ]

    return {
        "answer": answer,
        "sources": sources
    }
