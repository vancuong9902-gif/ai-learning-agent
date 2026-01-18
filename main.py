import os
import time
from typing import List, Optional, Dict, Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
from dotenv import load_dotenv

import psycopg2
from psycopg2.extras import Json

# --- 1. CẤU HÌNH ---
load_dotenv()  # Tự động đọc file .env

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "lms_db"),
    "user": os.getenv("DB_USER", "postgres"),
    # Không hard-code password trong code / repo.
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
}

app = FastAPI(title="Quiz Generator Stub")

# --- 2. ĐỊNH NGHĨA DTO ---
class QuizRequest(BaseModel):
    topic: str
    level: str

    @validator("level")
    def validate_level(cls, v: str) -> str:
        allowed = ["Beginner", "Intermediate", "Advanced"]
        if v not in allowed:
            raise ValueError(f"Level không hợp lệ. Chỉ chấp nhận: {allowed}")
        return v


class QuestionDTO(BaseModel):
    content: str
    question_type: str  # "MCQ" | "Essay"
    options: Optional[Dict[str, Any]] = None
    correct_answer: str


class QuizResponse(BaseModel):
    quiz_id: int
    topic: str
    level: str
    status: str
    questions: List[QuestionDTO]


# --- 3. LOGIC PROMPT ---
def get_prompt_template(topic: str, level: str) -> str:
    if level == "Beginner":
        return f"Topic: {topic}. Level: Beginner. Focus: Định nghĩa, nhận biết."
    if level == "Intermediate":
        return f"Topic: {topic}. Level: Intermediate. Focus: Giải thích, so sánh, phân tích."
    if level == "Advanced":
        # Bám đúng rubric: "vận dụng tình huống"
        return (
            f"Topic: {topic}. Level: Advanced. Focus: Vận dụng kiến thức vào tình huống thực tế, "
            "đề xuất giải pháp/ra quyết định."
        )
    return f"Topic: {topic}."


# --- 4. GIẢ LẬP LLM (STUB) ---
def mock_llm_generate(prompt: str, level: str) -> List[Dict[str, Any]]:
    print(f"\n[SYSTEM] Đang gửi Prompt lên LLM (stub): {prompt}\n")
    time.sleep(0.2)

    topic_part = prompt.split(".")[0]

    if level == "Beginner":
        return [
            {
                "content": f"Câu hỏi Beginner về {topic_part}?",
                "question_type": "MCQ",
                "options": {"A": "Option 1", "B": "Option 2"},
                "correct_answer": "B",
            }
        ]

    if level == "Intermediate":
        return [
            {
                "content": f"Câu hỏi Intermediate về {topic_part}?",
                "question_type": "Essay",
                # Essay không cần options
                "options": None,
                "correct_answer": "Câu trả lời mẫu cho Intermediate.",
            }
        ]

    # Advanced
    return [
        {
            "content": (
                f"Tình huống Advanced: Hãy áp dụng kiến thức về {topic_part} để xử lý một bài toán thực tế. "
                "Nêu giải pháp và lập luận."
            ),
            "question_type": "Essay",
            "options": None,
            "correct_answer": "Một phương án hợp lý là... (stub)",
        }
    ]


# --- 5. API ENDPOINT ---
@app.post("/quiz/generate", response_model=QuizResponse)
def generate_quiz_endpoint(request: QuizRequest):
    if not DB_CONFIG.get("password"):
        raise HTTPException(
            status_code=500,
            detail="Thiếu DB_PASSWORD. Hãy tạo file .env (tham khảo .env.example) hoặc export biến môi trường DB_PASSWORD.",
        )

    conn = None
    try:
        # A. Lấy prompt
        prompt_text = get_prompt_template(request.topic, request.level)

        # B. Gọi AI giả
        generated_questions = mock_llm_generate(prompt_text, request.level)

        # C. Lưu vào Database
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        # C1. Insert Quiz
        cur.execute(
            "INSERT INTO quizzes (topic, difficulty_level) VALUES (%s, %s) RETURNING id",
            (request.topic, request.level),
        )
        new_quiz_id = cur.fetchone()[0]

        response_data: List[QuestionDTO] = []
        for q in generated_questions:
            options_value = Json(q["options"]) if q.get("options") is not None else None

            # C2. Insert Questions
            cur.execute(
                """
                INSERT INTO questions (quiz_id, content, question_type, options, correct_answer)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    new_quiz_id,
                    q["content"],
                    q["question_type"],
                    options_value,
                    q["correct_answer"],
                ),
            )

            response_data.append(QuestionDTO(**q))

        conn.commit()

        return {
            "quiz_id": new_quiz_id,
            "topic": request.topic,
            "level": request.level,
            "status": "Success",
            "questions": response_data,
        }

    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Lỗi: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()
