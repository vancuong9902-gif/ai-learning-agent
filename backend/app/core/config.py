from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Đọc đúng backend/.env và tránh BOM + key thừa làm chết app
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    APP_NAME: str = "AI Learning Agent"
    ENV: str = "dev"
    BACKEND_CORS_ORIGINS: str = "http://localhost:5173"

    DATABASE_URL: str
    OPENAI_API_KEY: str | None = None


# QUAN TRỌNG: main.py đang import "settings"
settings = Settings()
