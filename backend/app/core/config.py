from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://nwis_user:nwis_password@localhost:5432/nwis"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Security
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # API Keys
    OPENAI_API_KEY: Optional[str] = None
    
    # Storage
    STORAGE_PATH: str = "./data"
    
    # ML Models
    MODEL_PATH: str = "./models"
    
    # Monitoring
    PROMETHEUS_PORT: int = 9090
    
    class Config:
        env_file = ".env"

settings = Settings()
