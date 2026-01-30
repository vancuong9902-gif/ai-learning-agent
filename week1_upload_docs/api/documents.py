from fastapi import APIRouter, UploadFile, File
from storage.db import get_db
from fastapi.concurrency import run_in_threadpool
from ingest.ingest import ingest_document

router = APIRouter()

# 1️⃣ Upload document
@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload PDF/DOCX → extract → chunk → save DB
    """
    doc_id, num_chunks = await run_in_threadpool(
        ingest_document, file
    )

    return {
        "doc_id": doc_id,
        "filename": file.filename,
        "num_chunks": num_chunks
    }



# 2️⃣ GET /documents
@router.get("")
def list_documents():
    """
    Lấy danh sách documents đã upload
    """
    db = get_db()
    rows = db.execute(
        "SELECT doc_id, file_name FROM documents"
    ).fetchall()

    return [
        {
            "doc_id": r["doc_id"],
            "filename": r["file_name"]
        }
        for r in rows
    ]


# 3️⃣ GET /documents/{doc_id}/chunks
@router.get("/{doc_id}/chunks")
def get_chunks_by_doc(doc_id: str):
    db = get_db()
    rows = db.execute(
        """
        SELECT chunk_id
        FROM chunks
        WHERE doc_id = ?
        ORDER BY chunk_id
        """,
        (doc_id,)
    ).fetchall()

    return [
        {
            "chunk_id": r["chunk_id"],
            "note": "Text nằm trong Chroma (vector DB)"
        }
        for r in rows
    ]
