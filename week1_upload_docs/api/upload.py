from fastapi import APIRouter, UploadFile, File
import shutil
import uuid
from pathlib import Path

from ingest.extract import extract_text
from ingest.chunking import chunk_text

router = APIRouter()

UPLOAD_DIR = Path("documents/upload/raw_docs")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # 1️⃣ Tạo doc_id
    doc_id = str(uuid.uuid4())

    # 2️⃣ Lưu file (giữ doc_id để tránh trùng tên)
    file_path = UPLOAD_DIR / f"{doc_id}_{file.filename}"
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # 3️⃣ Extract text (PDF hoặc DOCX)
    text = extract_text(str(file_path))

    # 4️⃣ Chunk text
    chunks = chunk_text(text)

    # 5️⃣ Trả response đúng TEST CASE
    return {
        "doc_id": doc_id,
        "filename": file.filename,
        "num_chunks": len(chunks)
    }
