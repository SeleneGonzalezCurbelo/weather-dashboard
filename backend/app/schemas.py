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
from typing import List
from datetime import datetime
from uuid import UUID
from zoneinfo import ZoneInfo

class WeatherBase(BaseModel):
    city: str
    temperature: float
    humidity: int
    description: str


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