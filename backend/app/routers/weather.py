"""
Weather Router for Weather Dashboard API.

Exposes endpoints for weather operations: fetch, save, history, summary, forecast, and reverse geocoding.
All endpoints implement input validation, error handling, and response typing for security and maintainability.
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
import requests
from urllib.parse import urlencode

from app.db import get_db
from app.schemas import PaginatedWeatherResponse
from app.config import OPENWEATHER_API_KEY, OPENWEATHER_REVERSE_URL
from app.exceptions import AppError, ValidationError, APIError, DatabaseError
from app.utils.validation import validate_city_name
from app.services.weather_service import (
    fetch_current_weather,
    save_weather_data,
    get_weather_history,
    get_daily_summary,
    get_latest_weather,
    fetch_5day_forecast
)

router = APIRouter()


@router.get("/history", response_model=PaginatedWeatherResponse)
def list_weathers(
    db: Session = Depends(get_db),
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0)
) -> PaginatedWeatherResponse:
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
) -> PaginatedWeatherResponse:
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


@router.post("/save/{city}", response_model=dict)
def weather_save(city: str, db: Session = Depends(get_db)) -> dict:
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
    except (AppError, APIError, DatabaseError, ValidationError) as e:
        raise e
    except Exception as e:
        raise AppError(message="Internal server error.", code=500, log=True)


@router.get("/latest/{city}", response_model=dict)
def latest_weather(city: str, db: Session = Depends(get_db)) -> dict:
    """
    Retrieve the most recent weather record for a city from the database.

    Args:
        city (str): Name of the city.
        db (Session): Database session.

    Returns:
        dict: Weather record with all recorded metrics.
    """
    validate_city_name(city)
    try:
        return get_latest_weather(city, db=db)
    except (AppError, APIError, DatabaseError, ValidationError) as e:
        raise e
    except Exception as e:
        raise AppError(message="Internal server error.", code=500, log=True)


@router.get("/daily-summary/{city}", response_model=dict)
def daily_summary(city: str, db: Session = Depends(get_db)) -> dict:
    """
    Get daily min/max/average stats for a city.

    Args:
        city (str): Name of the city.
        db (Session): Database session.

    Returns:
        dict: Daily summary metrics.
    """
    validate_city_name(city)
    try:
        return get_daily_summary(city, db=db)
    except (AppError, APIError, DatabaseError, ValidationError) as e:
        raise e
    except Exception as e:
        raise AppError(message="Internal server error.", code=500, log=True)


@router.get("/forecast/{city}", response_model=list)
def forecast(city: str) -> list:
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
            raise APIError(message=f"No forecast available for {city}", log=True)
        return data
    except (AppError, APIError, DatabaseError, ValidationError) as e:
        raise e
    except Exception as e:
        raise AppError(message="Internal server error.", code=500, log=True)


@router.get("/reverse-geocode", response_model=dict)
def reverse_geocode(lat: float = Query(...), lon: float = Query(...)) -> dict:
    """
    Reverse geocode coordinates to city name using OpenWeather API.

    Args:
        lat (float): Latitude.
        lon (float): Longitude.

    Returns:
        dict: City name.

    Raises:
        HTTPException: If coordinates are invalid or city not found.
    """
    if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
        raise ValidationError(message="Invalid latitude or longitude values.")
    if not OPENWEATHER_API_KEY:
        raise APIError(message="API key not configured.", log=True)
    params = {
        "lat": lat,
        "lon": lon,
        "limit": 1,
        "appid": OPENWEATHER_API_KEY
    }
    url = f"{OPENWEATHER_REVERSE_URL}?{urlencode(params)}"
    try:
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()
        if not data or "name" not in data[0]:
            raise APIError(message="City not found for given coordinates.", code=404, log=True)
        return {"city": data[0]["name"]}
    except requests.RequestException as e:
        raise APIError(message="Failed to reverse geocode coordinates.", log=True)


@router.get("/{city}", response_model=dict)
def weather(city: str) -> dict:
    """
    Fetch current weather data from external API for a given city.

    Args:
        city (str): Name of the city.

    Returns:
        dict: Structured dictionary containing temperature, humidity, pressure, wind, cloudiness, and description.

    Example:
        {
            "temperature": 22.5,
            "humidity": 60,
            "pressure": 1012,
            "wind_speed": 3.5,
            "cloudiness": 40,
            "description": "clear sky"
        }
    """
    validate_city_name(city)
    try:
        return fetch_current_weather(city)
    except (AppError, APIError, DatabaseError, ValidationError) as e:
        raise e
    except Exception as e:
        raise AppError(message="Internal server error.", code=500, log=True)