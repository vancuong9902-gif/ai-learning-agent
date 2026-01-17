# AI Learning Agent (Project Skeleton)

Khung project cho đề tài _Cá nhân hoá chương trình học dựa trên AI Agent_.

- **Backend**: FastAPI + Swagger (/docs) + SQLAlchemy + Alembic
- **DB**: Postgres (Docker Compose) hoặc cài local
- **Frontend**: React + Vite (Home tối thiểu)
- **Docs**: Quy ước branch/PR + template báo cáo tuần

## 1) Cấu trúc thư mục

```
.
├─ backend/                 # FastAPI + DB + migrations
├─ frontend/                # React/Vite
├─ docs/                    # quy ước làm việc
├─ docker-compose.yml        # Postgres dev
└─ README.md
```

## 2) Chạy nhanh (khuyến nghị) — Postgres bằng Docker

### 2.1. Chạy Postgres

Tại thư mục root:

```bash
docker compose up -d
```

> DB mặc định: user/pass `postgres/postgres`, database `ai_agent`, port `5432`.

### 2.2. Chạy Backend

```bash
cd backend
cp .env.example .env
python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate
pip install -r requirements.txt

# chạy migrations để tạo bảng
alembic upgrade head

# chạy server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Mở Swagger:

- http://localhost:8000/docs

Health check:

- http://localhost:8000/api/health

### 2.3. Chạy Frontend

```bash
cd ../frontend
cp .env.example .env
npm install
npm run dev
```

Mở web:

- http://localhost:5173

## 3) Chạy local (không dùng Docker)

- Cài Postgres local và tạo DB `ai_agent`
- Sửa `DATABASE_URL` trong `backend/.env` cho đúng máy bạn

## 4) Quy ước làm việc nhóm

Xem:

- `docs/branch-and-pr-rules.md`
- `docs/weekly-report-template.md`
- `.github/PULL_REQUEST_TEMPLATE/pull_request_template.md`
