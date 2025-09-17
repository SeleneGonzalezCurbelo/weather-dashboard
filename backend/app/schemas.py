# app/schemas.py
"""
Pydantic schemas for Weather Dashboard API responses.

Schemas define how data is serialized and validated for API endpoints.

Schemas:
- WeatherBase : shared fields between input and output.
- WeatherCreate : fields required to create a new weather record.
- WeatherResponse : fields returned in API responses (includes id and created_at).
- PaginatedWeatherResponse : response wrapper for lists with pagination.
"""
from pydantic import BaseModel, field_serializer
from typing import List, Optional
from datetime import datetime
from uuid import UUID
from zoneinfo import ZoneInfo

class WeatherBase(BaseModel):
    city: str
    country: Optional[str] = None
    description: str
    icon: Optional[str] = None

    temperature: float
    feels_like: Optional[float] = None
    temp_min: Optional[float] = None
    temp_max: Optional[float] = None

    humidity: float
    pressure: Optional[int] = None
    sea_level: Optional[int] = None
    grnd_level: Optional[int] = None

    wind_speed: Optional[float] = None
    wind_deg: Optional[int] = None
    wind_gust: Optional[float] = None

    visibility: Optional[int] = None
    clouds: Optional[int] = None
    rain_1h: Optional[float] = None
    rain_3h: Optional[float] = None

    sunrise: Optional[int] = None
    sunset: Optional[int] = None

class WeatherCreate(WeatherBase):
    """Schema for creating new weather entries (input)."""
    pass


class WeatherResponse(WeatherBase):
    """Schema for weather records returned to clients (output)."""
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True  

    @field_serializer("created_at")
    def serialize_created_at(self, dt: datetime, _info):
        if dt is None:
            return None
        return dt.replace(tzinfo=ZoneInfo("UTC")).astimezone(ZoneInfo("Europe/Madrid"))

class PaginatedWeatherResponse(BaseModel):
    """Schema for paginated weather responses."""
    total: int
    records: List[WeatherResponse]