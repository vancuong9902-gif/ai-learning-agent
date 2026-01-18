-- Schema cho tuần 1: Quiz + Questions
-- Chạy: psql -U postgres -d lms_db -f schema.sql

CREATE TABLE IF NOT EXISTS quizzes (
  id SERIAL PRIMARY KEY,
  topic TEXT NOT NULL,
  difficulty_level TEXT NOT NULL CHECK (difficulty_level IN ('Beginner','Intermediate','Advanced')),
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS questions (
  id SERIAL PRIMARY KEY,
  quiz_id INT NOT NULL REFERENCES quizzes(id) ON DELETE CASCADE,
  content TEXT NOT NULL,
  question_type TEXT NOT NULL CHECK (question_type IN ('MCQ','Essay')),
  options JSONB,
  correct_answer TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);
