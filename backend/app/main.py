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
- POST /weather/save/{city} : fetch and save current weather
- GET /weather/history : list all saved weather records
- GET /weather/history/{city} : list saved weather records for a specific city
- GET /weather/daily-summary/{city} : min/max temperature and humidity for the day for the city.
"""
import datetime
from http.client import HTTPException
from fastapi import Depends, FastAPI, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.db import Base, engine, get_db
from app.weather_client import get_weather
from app import db
from app.crud import save_weather
from app.models import Weather
from app.schemas import PaginatedWeatherResponse, WeatherResponse
from app.exceptions import DatabaseError, AppError
from app.config import settings
from app.error_handlers import app_error_handler, generic_exception_handler
import logging
from fastapi.middleware.cors import CORSMiddleware
from app.scheduler import start_scheduler

start_scheduler()
Base.metadata.create_all(bind=engine)

logger = logging.getLogger(__name__)
app = FastAPI(title="Weather Dashboard API")

app.add_exception_handler(AppError, app_error_handler)
app.add_exception_handler(Exception, generic_exception_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,  
    allow_credentials=True,
    allow_methods=["*"],   
    allow_headers=["*"],    
)

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
    """
    Fetch current weather data from external API for a given city.

    Returns a structured dictionary containing temperature, humidity,
    pressure, wind, cloudiness, and description.
    """
    data = get_weather(city)
    main = data.get("main", {})
    weather_list = data.get("weather", [{}])
    wind = data.get("wind", {})
    clouds = data.get("clouds", {})

    return {
        "city": data.get("name"),
        "temperature": main.get("temp"),
        "feels_like": main.get("feels_like"),
        "temp_min": main.get("temp_min"),
        "temp_max": main.get("temp_max"),
        "humidity": main.get("humidity"),
        "pressure": main.get("pressure"),
        "visibility": data.get("visibility"),
        "wind_speed": wind.get("speed"),
        "wind_deg": wind.get("deg"),
        "wind_gust": wind.get("gust"),
        "cloudiness": clouds.get("all"),
        "description": weather_list[0].get("description") if weather_list else None,
    }

@app.post("/weather/save/{city}")
def weather_save(city: str):
    """
    Fetch current weather and save it to the database.
    """
    save_weather(city)  
    return {"message": f"Weather for {city} saved successfully."}

@app.get("/weather/daily-summary/{city}")
def daily_summary(city: str, db: Session = Depends(get_db)):
    """
    Compute daily summary (min/max/average) of weather metrics for a city.

    Returns:
    --------
    Dictionary with min/max temperature, min/max humidity, average feels_like,
    average pressure, min/max wind speed, and average cloudiness.
    """
    try:
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)

        records = (
            db.query(Weather)
            .filter(Weather.city == city)
            .filter(Weather.created_at >= today)
            .filter(Weather.created_at < tomorrow)
            .all()
        )

        if not records:
            raise HTTPException(status_code=404, detail="No weather data today")

        temps = [r.temperature for r in records]
        humidities = [r.humidity for r in records]
        feels_like = [r.feels_like for r in records if r.feels_like is not None]
        pressures = [r.pressure for r in records if r.pressure is not None]
        winds = [r.wind_speed for r in records if r.wind_speed is not None]
        clouds = [r.cloudiness for r in records if r.cloudiness is not None]

        return {
            "city": city,
            "temp_min": min(temps),
            "temp_max": max(temps),
            "humidity_min": min(humidities),
            "humidity_max": max(humidities),
            "feels_like_avg": round(sum(feels_like)/len(feels_like), 2) if feels_like else None,
            "pressure_avg": round(sum(pressures)/len(pressures), 2) if pressures else None,
            "wind_speed_min": min(winds) if winds else None,
            "wind_speed_max": max(winds) if winds else None,
            "cloudiness_avg": round(sum(clouds)/len(clouds), 2) if clouds else None,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/weather/latest/{city}", response_model=WeatherResponse)
def latest_weather(city: str, db: Session = Depends(get_db)):
    """
    Retrieve the most recent weather record for a city from the database.

    Returns:
    --------
    WeatherResponse object with all recorded metrics.
    """
    record = (
        db.query(Weather)
        .filter(Weather.city == city)
        .order_by(Weather.created_at.desc())
        .first()
    )
    if not record:
        raise HTTPException(status_code=404, detail=f"No weather data found for {city}")
    return record