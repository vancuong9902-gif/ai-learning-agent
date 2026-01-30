from fastapi import FastAPI
from api.rag import router as rag_router
from api.documents import router as documents_router

app = FastAPI()

app.include_router(
    documents_router,
    prefix="/documents",
    tags=["Documents"]
)

app.include_router(
    rag_router,
    prefix="/rag",
    tags=["RAG"]
)
