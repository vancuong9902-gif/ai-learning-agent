from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "AI Learning Agent"
    ENV: str = "dev"
    BACKEND_CORS_ORIGINS: str = "http://localhost:5173"
    DATABASE_URL: str
    OPENAI_API_KEY: str | None = None

    class Config:
        env_file = ".env"


settings = Settings()
