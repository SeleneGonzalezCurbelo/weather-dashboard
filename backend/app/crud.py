# app/crud.py
"""
Module for fetching weather data from an external API and saving it to the database.

Responsibilities:
- Fetch weather data for a given city.
- Validate fetched data.
- Save validated data to the database.
- Log warnings and errors consistently.

This module uses custom exceptions to standardize error handling:
- APIError: problems fetching data from the weather API.
- ValidationError: incomplete or invalid data received.
- DatabaseError: issues when committing to the database.
"""

import logging
from typing import Dict, Any
from app.models import Weather
from app.weather_client import get_weather
from app.exceptions import APIError, DatabaseError, ValidationError
from app.config import TEMP_MIN, TEMP_MAX, HUMIDITY_MIN, HUMIDITY_MAX

logger = logging.getLogger(__name__)


def validate_weather_data(data: Dict[str, Any], city: str) -> Dict[str, Any]:
    """
    Validate the structure and values of fetched weather data and map to DB fields.

    Args:
        data (dict): Raw weather data from the API.
        city (str): City name (for logging/exceptions).

    Returns:
        dict: Validated and cleaned weather data.

    Raises:
        ValidationError: If required fields are missing or None.
    """
    if not data.get("main") or not data.get("weather"):
        raise ValidationError(f"Incomplete data received for {city}")

    main = data.get("main", {})
    weather_list = data.get("weather", [{}])
    wind = data.get("wind", {})
    rain = data.get("rain", {})
    clouds = data.get("clouds", {})
    sys = data.get("sys", {})

    temp = main.get("temp")
    humidity = main.get("humidity")
    desc = weather_list[0].get("description") if weather_list else "No description available"
    icon = weather_list[0].get("icon") if weather_list else None
    name = data.get("name")

    if name is None or temp is None or humidity is None:
        raise ValidationError(f"Incomplete data received for {city}: {data}")

    if not (TEMP_MIN <= temp <= TEMP_MAX):
        logger.warning(f"Temperature out of expected range for {city}: {temp}°C")
    if not (HUMIDITY_MIN <= humidity <= HUMIDITY_MAX):
        logger.warning(f"Humidity out of expected range for {city}: {humidity}%")

    return {
        "city": name,
        "country": sys.get("country"),
        "description": desc,
        "icon": icon,

        "temperature": temp,
        "feels_like": main.get("feels_like"),
        "temp_min": main.get("temp_min"),
        "temp_max": main.get("temp_max"),

        "humidity": humidity,
        "pressure": main.get("pressure"),
        "sea_level": main.get("sea_level"),
        "grnd_level": main.get("grnd_level"),

        "wind_speed": wind.get("speed"),
        "wind_deg": wind.get("deg"),
        "wind_gust": wind.get("gust"),

        "visibility": data.get("visibility"),
        "clouds": clouds.get("all"),
        "rain_1h": rain.get("1h"),
        "rain_3h": rain.get("3h"),

        "sunrise": sys.get("sunrise"),
        "sunset": sys.get("sunset"),
    }


def save_weather(city: str, db=None) -> None:
    """
    Fetch, validate, and save weather data for a given city.

    Args:
        city (str): Name of the city.

    Raises:
        APIError: If fetching weather data fails.
        ValidationError: If data is incomplete or invalid.
        DatabaseError: If committing to the database fails.
    """
    try:
        data = get_weather(city)
    except Exception as e:
        raise APIError(f"Failed to fetch weather for {city}: {e}")

    validated_data = validate_weather_data(data, city)

    new_session = False
    if db is None:
        from app.db import SessionLocal
        db = SessionLocal()
        new_session = True

    try:
        weather_entry = Weather(**validated_data)
        db.add(weather_entry)
        db.commit()
        logger.info(f"Saved enriched weather data for {city} to the database.")
    except Exception as e:
        db.rollback()
        raise DatabaseError(f"Failed to save weather for {city}: {e}")
    finally:
        if new_session:
            db.close()