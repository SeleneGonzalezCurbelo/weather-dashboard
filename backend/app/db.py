# app/db.py
"""
Database configuration and session management for Weather Dashboard.

Provides:
- SQLAlchemy engine creation.
- SessionLocal for database sessions.
- Base declarative class for models.

Environment variables are loaded from .env and provide connection info.

Example usage:
    from app.db import SessionLocal, Base, engine
    Base.metadata.create_all(bind=engine)
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """
    FastAPI dependency generator for database sessions.

    Yields:
        Session: SQLAlchemy database session.

    Ensures the session is closed after use to avoid connection leaks.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()