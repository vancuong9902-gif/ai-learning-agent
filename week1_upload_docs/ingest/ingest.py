import sqlite3
import uuid
from pathlib import Path
from vector_db.client import collection

from ingest.extract import extract_text
from ingest.chunking import chunk_text
from embedding.embedder import embed_text
from vector_db.client import collection

# ================= PATH SETUP =================

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "storage" / "data.db"
UPLOAD_DIR = BASE_DIR / "documents" / "upload" / "raw_docs"

# ================= DB INIT =================

def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        doc_id TEXT PRIMARY KEY,
        file_name TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS chunks (
        chunk_id TEXT PRIMARY KEY,
        doc_id TEXT,
        page INTEGER,
        content TEXT
    )
    """)

    conn.commit()
    conn.close()

# ================= CORE INGEST =================

def _ingest_from_path(file_path: str):
    doc_id = str(uuid.uuid4())
    file_name = Path(file_path).name

    pages = extract_text(file_path)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO documents VALUES (?, ?)",
        (doc_id, file_name)
    )

    documents = []
    metadatas = []
    ids = []

    for page in pages:
        chunks = chunk_text([page["text"]])

        for i, chunk in enumerate(chunks):
            chunk_id = f"{doc_id}_p{page['page']}_c{i}"

            # lưu sqlite
            cur.execute(
                "INSERT INTO chunks VALUES (?, ?, ?, ?)",
                (chunk_id, doc_id, page["page"], chunk)
            )

            # chuẩn bị chroma
            documents.append(chunk)
            metadatas.append({
                "doc_id": doc_id,
                "chunk_id": chunk_id,   # 🔥 BẮT BUỘC
                "page": page["page"],
                "filename": file_name   # 🔥 đồng bộ với search
            })

            ids.append(chunk_id)

    conn.commit()
    conn.close()

    # ===== EMBEDDING + ADD TO CHROMA =====
    if documents:
        embeddings = [embed_text(text) for text in documents]

        collection.add(
            documents=documents,
            metadatas=metadatas,
            embeddings=embeddings,
            ids=ids
        )
        
        
        print("CHROMA COUNT AFTER ADD:", collection.count())

        print(f"✔ Added {len(documents)} chunks to Chroma")

    return doc_id, len(documents)


# ================= API INGEST =================

def ingest_document(file):
    """
    Dùng cho FastAPI:
    UploadFile → save → ingest
    """
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    return _ingest_from_path(str(file_path))


# ================= BATCH MODE =================

def ingest_file(file_path: str):
    """
    Giữ lại để ingest file local (debug)
    """
    return _ingest_from_path(file_path)


if __name__ == "__main__":
    print("📂 UPLOAD_DIR =", UPLOAD_DIR)

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    init_db()

    for file in UPLOAD_DIR.iterdir():
        if file.is_file():
            ingest_file(str(file))

    print("✅ Ingest xong (tuần 1 + tuần 2)")

