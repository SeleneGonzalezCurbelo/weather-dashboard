# app/models.py
"""
SQLAlchemy ORM models for Weather Dashboard.

Defines database tables and relationships.

Models:
- Weather : stores weather data for a city, including temperature, humidity, description, and timestamp.

Includes table indexes for efficient queries (e.g., by created_at date).
"""
from app.db import Base
from sqlalchemy import Column, String, Float, DateTime, Index
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Weather(Base):
    __tablename__ = "weather_data"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    city = Column(String(100), nullable=False, index=False)
    temperature = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    description = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        Index('ix_weather_created_at', 'created_at'),
        Index('ix_weather_city', 'city'),
    )