from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
import models, schemas
from sqlalchemy import func

# Cấu hình Database (Dùng SQLite cho demo, thay bằng PostgreSQL URL cho production [cite: 108])
SQLALCHEMY_DATABASE_URL = "sqlite:///./learning_data.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/dbname" 

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Tạo bảng
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Agent Learning System - Tracking Module")

# Dependency để lấy DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- API ENDPOINTS ---

@app.post("/sessions/start", response_model=schemas.SessionResponse)
def start_session(session_in: schemas.SessionStart, db: Session = Depends(get_db)):
    """
    Bắt đầu một phiên học mới.
    Được gọi khi học viên bắt đầu xem tài liệu hoặc làm bài.
    """
    new_session = models.LearningSession(
        user_id=session_in.user_id,
        start_time=datetime.utcnow()
    )
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session

@app.post("/sessions/end/{session_id}", response_model=schemas.SessionResponse)
def end_session(session_id: int, db: Session = Depends(get_db)):
    """
    Kết thúc phiên học.
    Hệ thống tự động tính toán 'duration' dựa trên start_time và thời điểm hiện tại.
    Dữ liệu này phục vụ tính Effort Score cho Evaluation Agent[cite: 76].
    """
    session_record = db.query(models.LearningSession).filter(models.LearningSession.id == session_id).first()
    
    if not session_record:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if session_record.end_time:
        raise HTTPException(status_code=400, detail="Session already ended")

    # Cập nhật thời gian kết thúc
    session_record.end_time = datetime.utcnow()
    
    # Tự động tính Duration (giây)
    duration_delta = session_record.end_time - session_record.start_time
    session_record.duration = duration_delta.total_seconds()
    
    db.commit()
    db.refresh(session_record)
    return session_record

@app.post("/attempts/", response_model=schemas.AttemptResponse)
def create_attempt(attempt: schemas.AttemptCreate, db: Session = Depends(get_db)):
    """
    API phụ để log điểm bài kiểm tra (Test Score).
    Đã nâng cấp trả về đầy đủ ID và ngày tạo theo góp ý.
    """
    db_attempt = models.Attempt(**attempt.dict())
    db.add(db_attempt)
    db.commit()
    db.refresh(db_attempt)
    return db_attempt
@app.get("/evaluate/{user_id}")
def evaluate_user(user_id: int, db: Session = Depends(get_db)):
    """
    Evaluation Agent: Tính điểm tổng kết dựa trên công thức trong đề tài.
    """
    # --- 1. Tính Test Score (Trung bình cộng điểm các bài kiểm tra) ---
    avg_score = db.query(func.avg(models.Attempt.score)).filter(models.Attempt.user_id == user_id).scalar()
    test_score = avg_score if avg_score else 0.0

    # --- 2. Tính Effort Score (Dựa trên tổng thời gian học) ---
    # Lấy tổng số giây đã học
    total_duration_sec = db.query(func.sum(models.LearningSession.duration)).filter(models.LearningSession.user_id == user_id).scalar()
    total_duration = total_duration_sec if total_duration_sec else 0.0
    
    # Quy đổi: Giả sử học 60 phút (3600s) là đạt điểm nỗ lực tối đa (10 điểm)
    # Công thức: (Số giây học / 3600) * 10
    effort_score = (total_duration / 3600) * 10
    if effort_score > 10: effort_score = 10.0 # Không quá 10 điểm

    # --- 3. Tính Progress Score (Tiến bộ) ---
    # (Tạm tính: 5 điểm khuyến khích + 1 điểm cho mỗi bài test đã làm, tối đa 10)
    count_tests = db.query(models.Attempt).filter(models.Attempt.user_id == user_id).count()
    progress_score = 5.0 + count_tests
    if progress_score > 10: progress_score = 10.0

    # --- 4. TÍNH FINAL SCORE (Theo công thức đề tài) ---
    # Final = 0.5 * Test + 0.3 * Effort + 0.2 * Progress
    final_score = (0.5 * test_score) + (0.3 * effort_score) + (0.2 * progress_score)

    return {
        "user_id": user_id,
        "metrics": {
            "test_score_avg": round(test_score, 2),
            "effort_score_calc": round(effort_score, 2),
            "progress_score_est": round(progress_score, 2),
            "total_study_seconds": total_duration
        },
        "FINAL_SCORE": round(final_score, 2),
        "rank": "Xuất sắc" if final_score >= 8.5 else "Giỏi" if final_score >= 7 else "Khá"
    }