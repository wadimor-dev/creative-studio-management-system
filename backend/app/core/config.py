from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
import os

class Settings(BaseSettings):
    APP_NAME: str = "CSMS"
    APP_ENV: str = os.getenv("APP_ENV", "development")
    APP_DEBUG: bool = os.getenv("APP_DEBUG", "true").lower() == "true"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "temporary_secret_key")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "mysql+pymysql://root:@localhost/csms_db")
    
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))
    
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173", 
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://csms.idekode.web.id",
        "http://csms.idekode.web.id",
    ]
    CORS_ALLOW_CREDENTIALS: bool = False

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="ignore")

settings = Settings()
