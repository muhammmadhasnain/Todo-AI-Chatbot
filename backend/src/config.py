from pydantic_settings import BaseSettings
from typing import Optional
from dotenv import load_dotenv, find_dotenv
import os 

load_dotenv(find_dotenv())

class Settings(BaseSettings):
    # Database settings

    NEON_DATABASE_URL: Optional[str] = os.getenv("NEON_DATABASE_URL")

    # Better Auth settings
    BETTER_AUTH_URL: str = os.getenv("BETTER_AUTH_URL", "http://localhost:3000/api/auth").rstrip('/')
    BETTER_AUTH_SECRET: Optional[str] = os.getenv("BETTER_AUTH_SECRET")

    # Google OAuth settings
    GOOGLE_CLIENT_ID: Optional[str] = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET: Optional[str] = os.getenv("GOOGLE_CLIENT_SECRET")


    # Google Gemini settings
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

    # Application settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Todo AI Chatbot Backend"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

    # Security settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    # Server settings
    SERVER_HOST: str = os.getenv("SERVER_HOST", "localhost")
    SERVER_PORT: int = int(os.getenv("SERVER_PORT", "8000"))

    # Other settings that might be in env files
    API_BASE_URL: Optional[str] = os.getenv("API_BASE_URL")
    FRONTEND_URL: Optional[str] = os.getenv("FRONTEND_URL")

    # MCP settings
    MCP_SERVER_URL: Optional[str] = os.getenv("MCP_SERVER_URL")
    MCP_API_KEY: Optional[str] = os.getenv("MCP_API_KEY")

    class Config:
        env_file = ".env"
        # Allow extra fields to avoid validation errors for environment variables
        # that might be used by frontend or other parts of the application
        extra = "allow"

settings = Settings()