Weekly Report – Tuần 1 (12/01/2026 – 18/01/2026)
1) Thành viên & nhiệm vụ

+) Nguyễn Văn Cường (PM/Tech Lead + Integrator):

Tạo Git repo + cấu trúc thư mục backend/ frontend/ docs/

Thiết lập backend FastAPI + Swagger + .env

Docker Compose (Postgres)

DB tối thiểu (migrations/khung DB)

Quy ước branch/PR + template báo cáo tuần

+) Trương Thùy Linh

 Tạo bài test đầu vào (có thể hard-code 15–20 câu ban đầu)
 
 Xây rule phân level:
    
    <40% Beginner, 40–70 Intermediate, >70 Advanced
 
 Endpoint /profile/diagnostic nhận answers → trả level

Hoàn thành khi: test xong ra level

Hoàn thành khi: sau quiz, mastery thay đổi

+) Mai Trung Đức:

Thiết kế format dữ liệu quiz (quiz, questions)

Prompt template theo level (Beginner/Intermediate/Advanced)

Endpoint stub /quiz/generate (dummy)

+) Trương Thùy Linh:

Tạo bài test đầu vào (15–20 câu hard-code)

Rule phân level: <40% Beginner, 40–70 Intermediate, >70 Advanced

Endpoint /profile/diagnostic

+) Vũ Gia Bảo:

Upload PDF/DOCX

Extract text (pdfplumber, python-docx)

Chunking 400–600 tokens + overlap

Lưu documents/chunks + metadata

+) Đào Quỳnh Winter:

Thiết kế bảng log: learning_sessions, attempts

Endpoint /sessions/start, /sessions/end (hoặc FE gửi duration)

+) Vũ Hải Đăng:

Setup React + routing

Trang Login giả lập / chọn user

Trang Upload tài liệu

Trang Health check gọi backend

2) Tiến độ đã hoàn thành
✅ PM/Tech Lead (main branch)

 Project skeleton đã có đủ backend/ frontend/ docs/ + docker-compose.yml + .env.example + README hướng dẫn chạy

Evidence: repo main có đủ cấu trúc và hướng dẫn chạy backend + frontend + swagger + healthcheck.

 Đã có template PR và docs quy ước làm việc (theo README trỏ tới docs + PR template)

✅ Nhánh theo từng thành viên (đã push code lên branch)

 Linh – Diagnostic/Profiling: branch w1/linh-profiling-adaptive có main.py, questions.py, service.py (đúng hướng bài test + rule level).

 Đức – Assessment/Quiz: branch w1/duc-add-alo-assessment-agent có main.py, schema.sql, requirements.txt, .env.example.

 Bảo – Upload/Docs ingestion: branch w1/bao-week1-upload-docs-content-agent-rag-ingestion có main.py + README hướng dẫn chạy.

 Quỳnh – Logging/Effort analytics: branch w1/quynh-coevaluation-analytics có main.py, models.py, schemas.py, requirements.txt + README hướng dẫn chạy.

 Đăng – Frontend: branch w1/dang-frontend có thư mục backend/ và frontend/ (đã bắt đầu ghép FE/BE theo nhánh).

3) Demo / Bằng chứng

Repo main (skeleton chạy được):

Có README hướng dẫn chạy Docker Postgres, chạy backend (uvicorn + alembic), và chạy frontend Vite.

Branches đã push theo từng hạng mục tuần 1: danh sách branch hoạt động hiển thị đầy đủ trên trang Branches.

Gợi ý format nộp thầy: bạn có thể chụp màn hình 3 thứ:
(1) trang Branches, (2) README main, (3) chạy swagger /docs + FE trang home.

4) Kế hoạch tuần tới (Tuần 2)

+) Nguyễn Văn Cường

 Chốt API contract: request/response JSON (để FE gọi)
 
 Tích hợp Content Agent + Assessment Agent (end-to-end generate quiz)
 
 Tạo seed data + script demo
 
Hoàn thành khi: có demo “generate quiz từ tài liệu”

+) Trương Thùy Linh 

 Lưu learner_profile vào DB (level + mastery theo topic dạng JSON)

 Tạo logic cập nhật mastery sau quiz:

   đúng +α, sai -β (đơn giản)

Hoàn thành khi: sau quiz, mastery thay đổi

+) Mai Trung Đức

 Tích hợp RAG: gọi /rag/search lấy context chunks trước khi sinh câu hỏi
 
 Sinh câu hỏi MCQ (5 câu):
 
  có 4 lựa chọn
  
  có đáp án
  
  có giải thích ngắn
  
  có sources (chunk_id)
  
 Endpoint /quiz/{id}/submit chấm điểm
 
Hoàn thành khi: generate → làm → submit → có điểm

+) Vũ Gia Bảo

 Embedding (chọn 1):
 
  nhanh nhất: dùng API embedding
  
  hoặc local Sentence-BERT nếu nhóm làm local
  
 Vector DB (FAISS/Chroma) lưu embeddings + metadata
 
 API /rag/search?q=... trả về top-k chunks
 
Hoàn thành khi: query “tìm đoạn liên quan” trả về đúng + có nguồn

+) Đào Như Quỳnh

 Tính Test Score từ attempts
 
 Effort Score: chuẩn hoá theo tuần (cap để tránh “cày giờ”)
 
 Progress Score: dựa trên chênh lệch điểm lần gần nhất

Hoàn thành khi: có API trả điểm 3 thành phần

+) Vũ Hải Đăng

 Trang học viên: “Generate quiz” + hiển thị câu hỏi + submit
 
 Trang kết quả: score + giải thích + sources (nếu có)
 
Hoàn thành khi: học viên làm quiz được thêm icon cho đẹp
