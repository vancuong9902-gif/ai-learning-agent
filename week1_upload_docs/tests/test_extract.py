from pathlib import Path
from ingest.extract import extract_text

BASE_DIR = Path(__file__).resolve().parent.parent

file_path = (
    BASE_DIR
    / "documents"
    / "upload"
    / "raw_docs"
    / "git và github cách used.docx"
)

assert file_path.exists(), "❌ File không tồn tại"

pages = extract_text(str(file_path))

# ✅ Test đúng kiểu dữ liệu
assert isinstance(pages, list), "Extract không trả về list"
assert len(pages) > 0, "Extract trả về list rỗng"

# ✅ Test từng page
for page in pages:
    assert "page" in page, "Thiếu key 'page'"
    assert "text" in page, "Thiếu key 'text'"
    assert isinstance(page["text"], str), "Text không phải string"
    assert page["text"].strip(), "Text rỗng"

print("✅ EXTRACT OK")
print("📄 Total pages:", len(pages))
print("📏 First page length:", len(pages[0]["text"]))
print("📄 Preview:\n", pages[0]["text"][:500])
