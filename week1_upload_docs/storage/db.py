import sqlite3
from pathlib import Path

# Đảm bảo thư mục storage tồn tại
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "data.db"


def get_connection():
    """
    Tạo và trả về kết nối SQLite
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # để trả về dict-like
    return conn
# storage/db.py
def get_db():
    return get_connection()


def init_db():
    """
    Tạo bảng nếu chưa tồn tại
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        doc_id TEXT PRIMARY KEY,
        filename TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chunks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        doc_id TEXT,
        chunk_id INTEGER,
        page INTEGER,
        text TEXT
    )
    """)

    conn.commit()
    conn.close()
