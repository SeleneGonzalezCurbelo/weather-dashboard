"""
OpenWeather Adapter.

Encapsulates communication with the OpenWeather API and handles errors.

Functions:
- get_weather(city: str) -> dict
    Fetches the current weather for a city in JSON format.
    Raises APIError if the request fails.
- get_5day_forecast(city: str) -> dict
    Fetches the 5-day forecast for a city.
    Raises APIError if the request fails.
"""
import requests
from app.config import OPENWEATHER_BASE_URL, OPENWEATHER_API_KEY, OPENWEATHER_FORECAST_URL
from app.exceptions import APIError
from app.utils.validation import validate_city_name

def get_weather(city: str) -> dict:
    """Fetch current weather for a city from OpenWeatherMap.

    Args:
        city (str): City name.

    Raises:
        ValidationError: If city name is invalid.
        APIError: If the request fails.

    Returns:
        dict: Weather data in JSON format.
    """
    validate_city_name(city)
    if not OPENWEATHER_API_KEY:
        raise APIError("API key not configured.")
    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }
    try:
        res = requests.get(OPENWEATHER_BASE_URL, params=params, timeout=5)
        res.raise_for_status()
        return res.json()
    except requests.RequestException as e:
        raise APIError(f"Error fetching weather for {city}: {str(e)}")

def get_5day_forecast(city: str) -> dict:
    """Fetch 5-day forecast data for a city from OpenWeatherMap.

    Args:
        city (str): City name.

    Raises:
        ValidationError: If city name is invalid.
        APIError: If the request fails.

    Returns:
        dict: 5-day forecast data in JSON format.
    """
    validate_city_name(city)
    if not OPENWEATHER_API_KEY:
        raise APIError("API key not configured.")
    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }
    try:
        res = requests.get(OPENWEATHER_FORECAST_URL, params=params, timeout=5)
        res.raise_for_status()
        return res.json()
    except requests.RequestException as e:
        raise APIError(f"Error fetching 5-day forecast for {city}: {str(e)}")