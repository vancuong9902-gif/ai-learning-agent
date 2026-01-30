from pathlib import Path
import pdfplumber
from docx import Document


def extract_pdf(file_path: str):
    pages = []
    with pdfplumber.open(file_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text() or ""
            pages.append({
                "page": i + 1,
                "text": text
            })
    return pages


def extract_docx(file_path: str):
    doc = Document(file_path)
    full_text = []

    for para in doc.paragraphs:
        if para.text.strip():
            full_text.append(para.text)

    return [{
        "page": 1,
        "text": "\n".join(full_text)
    }]


def extract_text(file_path: str):
    ext = Path(file_path).suffix.lower()

    if ext == ".pdf":
        return extract_pdf(file_path)

    if ext == ".docx":
        return extract_docx(file_path)

    raise ValueError(f"❌ Unsupported file type: {ext}")
