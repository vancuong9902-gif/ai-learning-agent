# AI Learning Agent

Repo demo khung project (backend FastAPI + frontend React/Vite + Postgres).

## Cấu trúc thư mục

- `backend/` FastAPI + SQLAlchemy + Alembic (migrations)
- `frontend/` React + Vite (trang Home tối thiểu)
- `docs/` quy ước branch/PR + template báo cáo tuần
- `docker-compose.yml` Postgres (dev)

---

## Yêu cầu hệ thống

- Python 3.10+ (khuyến nghị 3.11)
- Node.js 18+
- Docker Desktop (khuyến nghị để chạy Postgres nhanh)

---

## Chạy nhanh (khuyến nghị) — dùng Docker Postgres

### Bước 1: chạy Postgres

Tại thư mục root:

```bash
docker compose up -d
```
