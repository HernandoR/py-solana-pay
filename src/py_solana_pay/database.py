"""Database configuration and session management"""

from pydantic_settings import BaseSettings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class Settings(BaseSettings):
    database_url: str = "sqlite:///./solana_pay.db"
    secret_key: str = "your-secret-key-here"
    candypay_private_api_key: str = ""
    candypay_public_api_key: str = ""
    candypay_endpoint: str = "https://api.candypay.fun"

    class Config:
        env_file = ".env"


settings = Settings()

engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False}
    if "sqlite" in settings.database_url
    else {},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
