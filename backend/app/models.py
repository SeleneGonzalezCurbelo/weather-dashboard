# app/models.py
"""
SQLAlchemy ORM models for Weather Dashboard.

Defines database tables and relationships.

Models:
- Weather : stores weather data for a city, including temperature, humidity, description, and timestamp.

Includes table indexes for efficient queries (e.g., by created_at date).
"""
from app.db import Base
from sqlalchemy import Column, String, Float, Integer, DateTime, Index
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Weather(Base):
    __tablename__ = "weather_data"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    
    city = Column(String(100), nullable=False, index=False)
    country = Column(String(10), nullable=True)

    description = Column(String(255), nullable=False)
    icon = Column(String(10), nullable=True)

    temperature = Column(Float, nullable=False)
    feels_like = Column(Float, nullable=True)
    temp_min = Column(Float, nullable=True)
    temp_max = Column(Float, nullable=True)


    humidity = Column(Float, nullable=False)
    pressure = Column(Integer, nullable=True)
    sea_level = Column(Integer, nullable=True)
    grnd_level = Column(Integer, nullable=True)
    
    wind_speed = Column(Float, nullable=True)
    wind_deg = Column(Integer, nullable=True)
    wind_gust = Column(Float, nullable=True)

    visibility = Column(Integer, nullable=True)
    clouds = Column(Integer, nullable=True)
    rain_1h = Column(Float, nullable=True)
    rain_3h = Column(Float, nullable=True)

    sunrise = Column(Integer, nullable=True)  
    sunset = Column(Integer, nullable=True)   

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        Index('ix_weather_created_at', 'created_at'),
        Index('ix_weather_city', 'city'),
    )