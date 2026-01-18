from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()

class LearningSession(Base):
    __tablename__ = "learning_sessions"

    # Định nghĩa bảng theo yêu cầu [cite: 76]
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True) # ID của học viên
    start_time = Column(DateTime, default=func.now()) # Thời gian bắt đầu
    end_time = Column(DateTime, nullable=True) # Thời gian kết thúc
    duration = Column(Float, nullable=True) # Thời lượng (giây) - Effort data quan trọng

class Attempt(Base):
    __tablename__ = "attempts"

    # Định nghĩa bảng kết quả kiểm tra [cite: 71, 73]
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True) # Cần user_id để biết ai làm bài
    quiz_id = Column(Integer, index=True)
    score = Column(Float) # Điểm số (Test Score)
    created_at = Column(DateTime, default=func.now())