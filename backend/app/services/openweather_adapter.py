"""
OpenWeather Adapter.

Encapsulates communication with the OpenWeather API and handles errors.

Functions:
- get_weather(city: str) -> dict
    Fetches the current weather for a city in JSON format.
    Raises APIError if the request fails.
"""
import requests
from app.config import OPENWEATHER_BASE_URL, OPENWEATHER_API_KEY, OPENWEATHER_FORECAST_URL
from app.exceptions import APIError

def get_weather(city: str) -> dict:
    print("city - get_weather - openweather", city)
    try:
        url = f"{OPENWEATHER_BASE_URL}?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
        res = requests.get(url)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        raise APIError(f"Error fetching weather for {city}: {e}")

def get_5day_forecast(city: str):
    """
    Fetch 5-day forecast data for a city.
    """
    params = {"q": city, "appid": OPENWEATHER_API_KEY, "units": "metric"}
    res = requests.get(OPENWEATHER_FORECAST_URL, params=params)
    if res.status_code != 200:
        raise Exception(f"OpenWeatherMap 5-day forecast API error: {res.status_code} {res.text}")
    return res.json()