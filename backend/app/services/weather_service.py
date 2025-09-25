"""
Weather Service.

Service layer that centralizes weather-related business logic:

- fetch_current_weather(city: str) -> dict
    Retrieves current weather using openweather_adapter.

- save_weather_data(city: str, db: Session)
    Saves the current weather of a city into the database.

- get_weather_history(db: Session, city: str, limit: int, offset: int) -> PaginatedWeatherResponse
    Fetches historical weather records (with optional pagination).

- get_daily_summary(city: str, db: Session) -> dict
    Computes min/max/average weather metrics for the current day.

- get_latest_weather(city: str, db: Session) -> Weather
    Returns the most recent weather record for a city.
"""
from sqlalchemy.orm import Session
from app.crud import save_weather
from app.models import Weather
from app.services.openweather_adapter import get_weather
from app.schemas import PaginatedWeatherResponse
from fastapi import HTTPException
from datetime import date, timedelta
from app.services.openweather_adapter import get_5day_forecast
from app.utils.validation import validate_city_name
from app.exceptions import AppError

def fetch_current_weather(city: str) -> dict:
    """
    Retrieves current weather using openweather_adapter.

    Args:
        city (str): Name of the city.

    Returns:
        dict: Weather data for the city.

    Raises:
        ValidationError: If city name is invalid.
        APIError: If external API fails.
    """
    validate_city_name(city)
    try:
        return get_weather(city)
    except Exception as e:
        raise AppError(message=f"Error fetching weather for {city}: {str(e)}", code=502)

def save_weather_data(city: str, db: Session):
    """
    Saves the current weather of a city into the database.

    Args:
        city (str): Name of the city.
        db (Session): Database session.

    Raises:
        ValidationError: If city name is invalid.
        APIError, DatabaseError: On failure.
    """
    validate_city_name(city)
    try:
        save_weather(city, db=db)
    except Exception as e:
        raise AppError(message=f"Error saving weather for {city}: {str(e)}", code=502)

def get_weather_history(db: Session, city: str = None, limit: int = 50, offset: int = 0) -> PaginatedWeatherResponse:
    """
    Fetches historical weather records (with optional pagination).

    Args:
        db (Session): Database session.
        city (str, optional): City name.
        limit (int): Max records to return.
        offset (int): Records to skip.

    Returns:
        PaginatedWeatherResponse: Paginated weather records.

    Raises:
        ValidationError: If city name is invalid.
    """
    if city:
        validate_city_name(city)
    try:
        query = db.query(Weather)
        if city:
            query = query.filter(Weather.city == city)
        total = query.count()
        records = query.order_by(Weather.created_at.desc()).offset(offset).limit(limit).all()
        return {"total": total, "records": records}
    except Exception as e:
        raise AppError(message=f"Error fetching weather history: {str(e)}", code=502)

def get_daily_summary(city: str, db: Session):
    """
    Computes min/max/average weather metrics for the current day.

    Args:
        city (str): Name of the city.
        db (Session): Database session.

    Returns:
        dict: Daily summary metrics.

    Raises:
        ValidationError: If city name is invalid.
        APIError: If DB query fails.
        HTTPException: If no weather data for today.
    """
    validate_city_name(city)
    try:
        today = date.today()
        tomorrow = today + timedelta(days=1)
        records = db.query(Weather).filter(
            Weather.city == city,
            Weather.created_at >= today,
            Weather.created_at < tomorrow
        ).all()
        if not records:
            raise HTTPException(status_code=404, detail="No weather data today")

        temps = [r.temperature for r in records]
        humidities = [r.humidity for r in records]
        feels_like = [r.feels_like for r in records if r.feels_like is not None]
        pressures = [r.pressure for r in records if r.pressure is not None]
        winds = [r.wind_speed for r in records if r.wind_speed is not None]
        clouds = [r.clouds for r in records if r.clouds is not None]

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
    except HTTPException:
        raise
    except Exception as e:
        raise AppError(message=f"Error getting daily summary for {city}: {str(e)}", code=502)

def get_latest_weather(city: str, db: Session):
    """
    Returns the most recent weather record for a city.

    Args:
        city (str): Name of the city.
        db (Session): Database session.

    Returns:
        Weather: Latest weather record or current weather from API.

    Raises:
        ValidationError: If city name is invalid.
        APIError: If DB/API fails.
    """
    validate_city_name(city)
    try:
        record = db.query(Weather).filter(Weather.city == city).order_by(Weather.created_at.desc()).first()
        if record:
            return record
        return fetch_current_weather(city)
    except Exception as e:
        raise AppError(message=f"Error getting latest weather for {city}: {str(e)}", code=502)

def fetch_5day_forecast(city: str):
    """
    Fetch the 5-day forecast for a given city from the external API.

    Args:
        city (str): Name of the city.

    Returns:
        list[dict]: List of forecast records.

    Raises:
        ValidationError: If city name is invalid.
        APIError: If external API fails.
    """
    validate_city_name(city)
    try:
        data = get_5day_forecast(city)
        if not data or "list" not in data:
            return []
        forecast = []
        for item in data["list"]:
            forecast.append({
                "created_at": item.get("dt_txt"),
                "temperature": item.get("main", {}).get("temp"),
                "feels_like": item.get("main", {}).get("feels_like"),
                "humidity": item.get("main", {}).get("humidity"),
                "pressure": item.get("main", {}).get("pressure"),
                "wind_speed": item.get("wind", {}).get("speed"),
                "wind_deg": item.get("wind", {}).get("deg"),
                "cloudiness": item.get("clouds", {}).get("all"),
                "icon": item.get("weather", [{}])[0].get("icon"),
            })
        return forecast
    except Exception as e:
        raise AppError(message=f"Error fetching 5-day forecast for {city}: {str(e)}", code=502)