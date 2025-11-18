
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRES: int = 60
    REDIS_URL: str = "redis://localhost:6379"
    CHROMA_DIR: str = "./vectorstore/index"
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
