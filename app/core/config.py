from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Settings for the application configuration."""
    
    DB_BACKEND: str = "changethis"
    MONGO_URI: str = "changethis"
    DB_NAME: str = "changethis"

    JWT_SECRET_KEY: str = "changethis"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8", 
        extra="ignore"
    )

settings = Settings()