from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/auth_db"

    # JWT
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALGORITHM: str = "HS256"
    
    # Security
    BCRYPT_ROUNDS: int = 12
    
    # Service
    SERVICE_NAME: str = "auth-service"
    API_V1_PREFIX: str = "/api/v1"
    
    class Config:
        env_file = ".env"


settings = Settings()