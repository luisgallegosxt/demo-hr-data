import secrets
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding='utf-8'
    )
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    SQLALCHEMY_DATABASE_URI: str
    FIRST_SUPERUSER: str
    FIRST_SUPERUSER_PASSWORD: str
    API_V1_STR: str
    ALGORITHM: str = "HS256"

    # class Config:
    #     env_file = ".env"

settings = Settings()
