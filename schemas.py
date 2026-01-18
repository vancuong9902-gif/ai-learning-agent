from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Schema cho input bắt đầu phiên học
class SessionStart(BaseModel):
    user_id: int

# Schema cho output phiên học
class SessionResponse(BaseModel):
    id: int
    user_id: int
    start_time: datetime
    end_time: Optional[datetime] = None
    duration: Optional[float] = None

    class Config:
        from_attributes = True

# Schema ghi nhận làm bài quiz (để test bảng attempts)
class AttemptCreate(BaseModel):
    user_id: int
    quiz_id: int
    score: float

class AttemptResponse(BaseModel):
    id: int
    user_id: int
    quiz_id: int
    score: float
    created_at: datetime

    class Config:
        from_attributes = True  # Quan trọng: Để đọc được dữ liệu từ SQLAlchemy