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
from app.models import Weather
from app.weather_client import get_weather
from app.exceptions import APIError, DatabaseError
from app.utils.validation import validate_weather_data

logger = logging.getLogger(__name__)

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