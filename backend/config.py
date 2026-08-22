"""
Application configuration loaded from environment variables (.env).
No secrets are hard-coded anywhere in this codebase.
"""
import os

from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    # Database
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./edubridge.db")

    # Auth
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "dev-only-insecure-key")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))

    # AI
    ai_provider: str = os.getenv("AI_PROVIDER", "anthropic")
    ai_api_key: str = os.getenv("AI_API_KEY", "")
    ai_model: str = os.getenv("AI_MODEL", "claude-sonnet-4-6")

    # App
    app_env: str = os.getenv("APP_ENV", "development")
    cors_origins: str = os.getenv(
        "CORS_ORIGINS", "http://localhost:5173,http://localhost:8080,http://127.0.0.1:5500"
    )

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    @property
    def demo_mode(self) -> bool:
        """DEMO MODE activates automatically when no AI API key is configured."""
        return not bool(self.ai_api_key.strip())

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
