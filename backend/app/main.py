# app/main.py
"""
Main module for the Weather Dashboard FastAPI backend.

Defines the API endpoints for:
- Retrieving current weather for a city.
- Saving weather data to the database.
- Listing historical weather records.

Also initializes the database tables at startup.

Endpoints:
- GET / : health check
- GET /weather/{city} : fetch current weather from API
- GET /weather/save/{city} : fetch and save current weather
- GET /weather/history : list all saved weather records
- GET /weather/history/{city} : list saved weather records for a specific city
"""
from fastapi import Depends, FastAPI, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.db import Base, engine, get_db
from app.weather_client import get_weather
from app.crud import save_weather
from app.models import Weather
from app.schemas import PaginatedWeatherResponse
from app.exceptions import DatabaseError, AppError
from app.error_handlers import app_error_handler, generic_exception_handler
import logging

Base.metadata.create_all(bind=engine)

logger = logging.getLogger(__name__)
app = FastAPI(title="Weather Dashboard API")

app.add_exception_handler(AppError, app_error_handler)
app.add_exception_handler(Exception, generic_exception_handler)

@app.get("/")
def root():
    return {"message": "Weather Dashboard backend funcionando!"}


@app.get("/weather/history", response_model=PaginatedWeatherResponse)
def list_weathers(
    db: Session = Depends(get_db),
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0)
):
    """
    List all weather records with pagination and ordered by most recent.

    Parameters:
    -----------
    limit : int
        Maximum number of records to return (default 50, max 500).
    offset : int
        Number of records to skip (default 0).

    Returns:
    --------
    List[WeatherResponse]
        List of weather records sorted by created_at descending.
    """
    try:
        total = db.query(Weather).count()
        records = (
            db.query(Weather)
            .order_by(Weather.created_at.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )
        return {"total": total, "records": records}
    except SQLAlchemyError as e:
        raise DatabaseError(f"Database error listing weathers: {str(e)}")

@app.get("/weather/history/{city}", response_model=PaginatedWeatherResponse)
def weather_history_city(
    city: str,
    db: Session = Depends(get_db),
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0)
):
    """
    Get weather history for a specific city with pagination, ordered by most recent.

    Parameters:
    -----------
    city : str
        Name of the city.
    limit : int
        Maximum number of records to return (default 50, max 500).
    offset : int
        Number of records to skip (default 0).

    Returns:
    --------
    List[WeatherResponse]
        List of weather records for the given city sorted by created_at descending.
    """
    try:
        total = db.query(Weather).filter(Weather.city == city).count()
        records = (
            db.query(Weather)
            .filter(Weather.city == city)
            .order_by(Weather.created_at.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )
        return {"total": total, "records": records}
    except SQLAlchemyError as e:
        raise DatabaseError(f"Database error listing weather for {city}: {str(e)}")

@app.get("/weather/{city}")
def weather(city: str):
    data = get_weather(city)
    return {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "description": data["weather"][0]["description"]
    }

@app.get("/weather/save/{city}")
def weather_save(city: str):
    save_weather(city)  
    return {"message": f"Weather for {city} saved successfully."}