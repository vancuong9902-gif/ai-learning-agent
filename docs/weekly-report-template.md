Weekly Report – Tuần 1 (12/01/2026 – 18/01/2026)
1) Thành viên & nhiệm vụ (Week 1 Scope)

Nguyễn Văn Cường (PM/Tech Lead + Integrator)

Setup Git repo + cấu trúc thư mục backend/ frontend/ docs/

Setup FastAPI + Swagger + .env.example

Docker Compose (Postgres)

DB khung tối thiểu (schema/migrations nền)

Quy ước branch/PR + template báo cáo tuần

Mai Trung Đức (Assessment Agent – Quiz)

Thiết kế format dữ liệu quiz (quiz, questions)

Prompt template theo level (Beginner/Intermediate/Advanced)

Endpoint stub /quiz/generate (dummy)

Trương Thùy Linh (Learner Profiling Agent)

Bài test đầu vào (15–20 câu hard-code)

Rule phân level: <40% Beginner, 40–70% Intermediate, >70% Advanced

Endpoint /profile/diagnostic

Vũ Gia Bảo (Content Agent – Upload/Extraction/Chunking)

Upload PDF/DOCX

Extract text (pdfplumber, python-docx)

Chunking 400–600 tokens + overlap

Lưu documents/chunks + metadata

Đào Quỳnh Winter (Evaluation/Effort Logging)

Thiết kế bảng log: learning_sessions, attempts

Endpoint /sessions/start, /sessions/end (hoặc FE gửi duration)

Vũ Hải Đăng (Frontend)

Setup React + routing

Trang Login giả lập / chọn user

Trang Upload tài liệu

Trang Health check gọi backend

2) Tiến độ đã hoàn thành (Week 1 Results)

✅ Main branch (PM/Tech Lead)

Repo skeleton đầy đủ backend/ frontend/ docs/

Có docker-compose.yml, .env.example, README hướng dẫn chạy

Swagger hoạt động, có endpoint healthcheck

Có quy ước branch/PR + PR template trong docs/README

✅ Branches theo từng thành viên (đã push code tuần 1)

Linh – Diagnostic/Profiling: w1/linh-profiling-adaptive

Có main.py, questions.py, service.py (rule-based level + endpoint)

Đức – Assessment/Quiz: w1/duc-add-alo-assessment-agent

Có main.py, schema.sql, requirements.txt, .env.example

Bảo – Upload/Ingestion: w1/bao-week1-upload-docs-content-agent-rag-ingestion

Có main.py + README hướng dẫn chạy

Quỳnh – Logging/Effort: w1/quynh-coevaluation-analytics

Có main.py, models.py, schemas.py, requirements.txt + README

Đăng – Frontend: w1/dang-frontend

Đã setup FE + routing + các trang cơ bản (Login/Upload/Health)

3) Demo / Evidence (nộp thầy)

Evidence tối thiểu đề xuất (3 ảnh/clip ngắn):

Ảnh trang Branches (hiển thị đủ nhánh tuần 1)

Ảnh README main (hướng dẫn chạy + cấu trúc repo)

Ảnh/clip chạy Swagger /docs + FE trang home/healthcheck

Trạng thái demo tuần 1:

Skeleton chạy được (Docker Postgres + backend + swagger + frontend skeleton).

Các module tuần 1 đã hoàn thành ở nhánh riêng, sẵn sàng tích hợp tuần 2.

4) Kế hoạch tuần tới – Tuần 2 (19/01/2026 – 25/01/2026)

Nguyễn Văn Cường

Chốt API contract (request/response JSON) để FE gọi thống nhất

Tích hợp Content Agent + Assessment Agent (end-to-end “generate quiz từ tài liệu”)

Seed data + script demo
✅ Hoàn thành khi: có demo “Upload tài liệu → RAG search → Generate quiz → Submit”

Mai Trung Đức

Tích hợp RAG: gọi /rag/search lấy context trước khi sinh câu hỏi

Sinh quiz MCQ (5 câu): 4 lựa chọn + đáp án + giải thích + sources (chunk_id)

Endpoint /quiz/{id}/submit chấm điểm
✅ Hoàn thành khi: generate → làm → submit → trả score + feedback

Vũ Gia Bảo

Embedding (chọn 1: API embedding hoặc local Sentence-BERT)

Vector DB (FAISS/Chroma) lưu embeddings + metadata

API /rag/search?q=... trả top-k chunks + nguồn
✅ Hoàn thành khi: query ra đúng đoạn + có doc/page/chunk_id

Đào Quỳnh Winter

Tính Test Score từ attempts

Effort Score: chuẩn hoá theo tuần + cap

Progress Score: dựa trên chênh lệch điểm lần gần nhất
✅ Hoàn thành khi: có API trả 3 score thành phần

Vũ Hải Đăng

Trang học viên: Generate quiz → render câu hỏi → submit

Trang kết quả: score + giải thích + sources
✅ Hoàn thành khi: user làm quiz được end-to-end
