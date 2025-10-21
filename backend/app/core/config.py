from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    # Database (usa SQLite em memória se DATABASE_URL não estiver definida)
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./leggal.db")

    # JWT
    secret_key: str = "your-secret-key-here-make-it-long-and-random-at-least-32-characters"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 10080  # 7 dias

    # OpenAI
    openai_api_key: Optional[str] = None
    openai_model_name: str = "gpt-4o-mini"

    # Server
    host: str = "0.0.0.0"
    port: int = 8000

    # Redis
    redis_url: str = "redis://localhost:6379"

    # Environment
    environment: str = "development"

    # Logging
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
