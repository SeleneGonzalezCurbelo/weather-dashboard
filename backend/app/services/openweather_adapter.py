"""
OpenWeather Adapter.

Encapsulates communication with the OpenWeather API and handles errors.

Functions:
- get_weather(city: str) -> dict
    Fetches the current weather for a city in JSON format.
    Raises APIError if the request fails.
"""
import requests
from app.config import settings, OPENWEATHER_BASE_URL, OPENWEATHER_API_KEY
from app.exceptions import APIError

def get_weather(city: str) -> dict:
    try:
        url = f"{OPENWEATHER_BASE_URL}?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
        res = requests.get(url)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        raise APIError(f"Error fetching weather for {city}: {e}")