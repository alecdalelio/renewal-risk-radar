"""
Configuration settings for the Renewal Risk Radar application.
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings."""
    
    # API Configuration
    openai_api_key: Optional[str] = None
    
    # Database Configuration
    database_url: str = "sqlite:///./renewal_risk_radar.db"
    
    # Application Configuration
    debug: bool = False
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"


# Global settings instance
settings = Settings()
