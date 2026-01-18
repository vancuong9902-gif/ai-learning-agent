import requests

BACKEND_URL = "http://127.0.0.1:8000"

def check_health():
    try:
        res = requests.get(f"{BACKEND_URL}/health", timeout=5)
        return res.json()
    except Exception as e:
        return {"error": str(e)}

def upload_document(file):
    files = {
        "file": (file.name, file.getvalue())
    }
    res = requests.post(f"{BACKEND_URL}/documents/upload", files=files)
    return res.json()
