"""
Weather Router.

Defines all routes related to weather operations:

- GET /weather/{city} → Fetch current weather from the external API.
- POST /weather/save/{city} → Save current weather to the database.
- GET /weather/history → Retrieve all saved weather records with pagination.
- GET /weather/history/{city} → Retrieve weather history for a specific city.
- GET /weather/daily-summary/{city} → Get daily min/max/average stats for a city.
- GET /weather/latest/{city} → Get the latest weather record for a city.
"""
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.services.weather_service import (
    fetch_current_weather,
    save_weather_data,
    get_weather_history,
    get_daily_summary,
    get_latest_weather,
    fetch_5day_forecast
)
from app.schemas import PaginatedWeatherResponse
import requests
from app.config import OPENWEATHER_API_KEY

router = APIRouter()

@router.get("/history", response_model=PaginatedWeatherResponse)
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
    return get_weather_history(db=db, limit=limit, offset=offset)

@router.get("/history/{city}", response_model=PaginatedWeatherResponse)
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
    return get_weather_history(db=db, city=city, limit=limit, offset=offset)

@router.get("/{city}")
def weather(city: str):
    """
    Fetch current weather data from external API for a given city.

    Returns a structured dictionary containing temperature, humidity,
    pressure, wind, cloudiness, and description.
    """
    return fetch_current_weather(city)

@router.post("/save/{city}")
def weather_save(city: str, db: Session = Depends(get_db)):
    """
    Fetch current weather and save it to the database.
    """
    save_weather_data(city, db=db)
    return {"message": f"Weather for {city} saved successfully."}

@router.get("/{city}")
def get_weather_by_city(city: str):
    """
    Get current weather for a city.
    """
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
        print(f"[Backend weather] Fetching: {url}")
        res = requests.get(url)
        print(f"[Backend weather] Status: {res.status_code}")
        res.raise_for_status()
        return res.json()
    except Exception as e:
        print(f"[Backend weather] Error: {e}")
        raise e

@router.get("/latest/{city}")
def latest_weather(city: str, db: Session = Depends(get_db)):
    """
    Retrieve the most recent weather record for a city from the database.

    Returns:
    --------
    WeatherResponse object with all recorded metrics.
    """
    return get_latest_weather(city, db=db)

@router.get("/forecast/{city}")
def forecast(city: str):
    """
    Fetch 5-day weather forecast from external API.

    Parameters:
    -----------
    city : str
        Name of the city to fetch the forecast for.

    Returns:
    --------
    List[dict]
        List of weather records for the next 5 days with temperature, humidity, wind, cloudiness, and icon.
    """
    try:
        data = fetch_5day_forecast(city)
        if not data:
            raise HTTPException(status_code=404, detail=f"No forecast available for {city}")
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/reverse-geocode")
def geocode(lat: float = Query(...), lon: float = Query(...)):
    """
    Reverse geocode coordinates to city name using OpenWeather API.
    """
    url = f"https://api.openweathermap.org/geo/1.0/reverse?lat={lat}&lon={lon}&limit=1&appid={OPENWEATHER_API_KEY}"
    print("[Backend geocode] Fetching:", url)
    res = requests.get(url)
    print("[Backend geocode] Status:", res.status_code, res.text)
    res.raise_for_status()
    data = res.json()
    print("Data geocode:", data)
    if data and "name" in data[0]:
        return {"city": data[0]["name"]}
    return {"city": "Arrecife"}