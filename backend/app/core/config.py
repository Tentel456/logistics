from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "AI Logistics Ecosystem"
    secret_key: str = "dev-secret-change-me"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 8
    cors_origins: list[str] = ["*"]

settings = Settings()
