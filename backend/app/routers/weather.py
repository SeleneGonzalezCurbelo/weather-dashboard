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
import logging
from app.exceptions import APIError, ValidationError
from app.utils.validation import validate_city_name

logger = logging.getLogger("weather-router")

router = APIRouter()

@router.get("/history", response_model=PaginatedWeatherResponse)
def list_weathers(
    db: Session = Depends(get_db),
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0)
):
    """
    List all weather records with pagination and ordered by most recent.

    Args:
        db (Session): Database session.
        limit (int): Maximum number of records to return (default 50, max 500).
        offset (int): Number of records to skip (default 0).

    Returns:
        PaginatedWeatherResponse: List of weather records sorted by created_at descending.
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

    Args:
        city (str): Name of the city.
        limit (int): Maximum number of records to return (default 50, max 500).
        offset (int): Number of records to skip (default 0).

    Returns:
        PaginatedWeatherResponse: List of weather records for the given city sorted by created_at descending.
    """
    validate_city_name(city)
    return get_weather_history(db=db, city=city, limit=limit, offset=offset)

@router.post("/save/{city}")
def weather_save(city: str, db: Session = Depends(get_db)):
    """
    Fetch current weather and save it to the database.

    Args:
        city (str): Name of the city.
        db (Session): Database session.

    Returns:
        dict: Success message.
    """
    validate_city_name(city)
    try:
        save_weather_data(city, db=db)
        return {"message": f"Weather for {city} saved successfully."}
    except APIError as e:
        logger.error(f"APIError while saving weather for {city}: {e.detail}")
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(f"Unexpected error while saving weather for {city}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error.")

@router.get("/latest/{city}")
def latest_weather(city: str, db: Session = Depends(get_db)):
    """
    Retrieve the most recent weather record for a city from the database.

    Args:
        city (str): Name of the city.
        db (Session): Database session.

    Returns:
        WeatherResponse: Weather record with all recorded metrics.
    """
    validate_city_name(city)
    try:
        return get_latest_weather(city, db=db)
    except APIError as e:
        logger.error(f"APIError while fetching latest weather for {city}: {e.detail}")
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(f"Unexpected error while fetching latest weather for {city}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error.")

@router.get("/forecast/{city}")
def forecast(city: str):
    """
    Fetch 5-day weather forecast from external API.

    Args:
        city (str): Name of the city to fetch the forecast for.

    Returns:
        list[dict]: List of weather records for the next 5 days with temperature, humidity, wind, cloudiness, and icon.
    """
    validate_city_name(city)
    try:
        data = fetch_5day_forecast(city)
        if not data:
            logger.warning(f"No forecast available for {city}")
            raise APIError(status_code=404, detail=f"No forecast available for {city}")
        return data
    except APIError as e:
        logger.error(f"APIError while fetching forecast for {city}: {e.detail}")
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(f"Unexpected error while fetching forecast for {city}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error.")

@router.get("/reverse-geocode")
def reverse_geocode(lat: float = Query(...), lon: float = Query(...)):
    """
    Reverse geocode coordinates to city name using OpenWeather API.

    Args:
        lat (float): Latitude.
        lon (float): Longitude.

    Returns:
        dict: City name.
    """
    if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
        logger.warning(f"Invalid coordinates received: lat={lat}, lon={lon}")
        raise ValidationError(detail="Invalid latitude or longitude values.")
    url = f"https://api.openweathermap.org/geo/1.0/reverse?lat={lat}&lon={lon}&limit=1&appid={OPENWEATHER_API_KEY}"
    logger.info(f"Fetching reverse geocode for lat={lat}, lon={lon}")
    try:
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()
        logger.debug(f"Reverse geocode response: {data}")
        if data and "name" in data[0]:
            return {"city": data[0]["name"]}
        return {"city": "Arrecife"}
    except requests.RequestException as e:
        logger.error(f"Error during reverse geocode: {str(e)}")
        raise HTTPException(status_code=502, detail="Failed to reverse geocode coordinates.")

@router.get("/{city}")
def weather(city: str):
    """
    Fetch current weather data from external API for a given city.

    Args:
        city (str): Name of the city.

    Returns:
        dict: Structured dictionary containing temperature, humidity, pressure, wind, cloudiness, and description.
    """
    validate_city_name(city)
    logger.info(f"Weather endpoint called with city: {city}")
    try:
        return fetch_current_weather(city)
    except APIError as e:
        logger.error(f"APIError while fetching weather for {city}: {e.detail}")
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(f"Unexpected error while fetching weather for {city}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error.")