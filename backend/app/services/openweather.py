# app/openweather.py
"""
OpenWeather Client / Fetcher.

Low-level functions to consume the OpenWeather API:

- fetch_current_weather(city: str) -> dict
    Returns the current weather data of a city, ready to be stored in the database.

- fetch_historical_weather(lat: float, lon: float, dt: int) -> dict
    Returns historical weather data for a given UTC timestamp.
"""
import requests
from datetime import datetime
from app.config import OPENWEATHER_API_KEY, OPENWEATHER_BASE_URL, OPENWEATHER_FORECAST_URL
from app.exceptions import APIError
from app.utils.validation import validate_city_name

def fetch_current_weather(city: str) -> dict:
    """
    Fetch current weather from OpenWeather for a given city and return
    a dict ready to save in the database.

    Args:
        city (str): City name.

    Raises:
        ValidationError: If city name is invalid.
        APIError: If the request fails.

    Returns:
        dict: Weather data.
    """
    validate_city_name(city)
    if not OPENWEATHER_API_KEY or not OPENWEATHER_BASE_URL:
        raise APIError("API key or base URL not configured.")

    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric",
    }

    try:
        res = requests.get(OPENWEATHER_BASE_URL, params=params, timeout=10)
        res.raise_for_status()
        data = res.json()

        main = data.get("main", {})
        wind = data.get("wind", {})
        clouds = data.get("clouds", {})
        rain = data.get("rain", {})
        snow = data.get("snow", {})
        sys = data.get("sys", {})

        return {
            "city": data.get("name"),
            "country": sys.get("country"),
            "description": data["weather"][0]["description"] if data.get("weather") else "N/A",
            "icon": data["weather"][0]["icon"] if data.get("weather") else None,
            "temperature": main.get("temp"),
            "feels_like": main.get("feels_like"),
            "temp_min": main.get("temp_min"),
            "temp_max": main.get("temp_max"),
            "humidity": main.get("humidity"),
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
            "snow_1h": snow.get("1h"),
            "snow_3h": snow.get("3h"),
            "sunrise": datetime.fromtimestamp(sys.get("sunrise")) if sys.get("sunrise") else None,
            "sunset": datetime.fromtimestamp(sys.get("sunset")) if sys.get("sunset") else None,
        }
    except requests.exceptions.RequestException as e:
        raise APIError(f"Error fetching weather for {city}: {str(e)}")

def fetch_historical_weather(lat: float, lon: float, dt: int) -> dict:
    """
    Fetch historical weather data for a given location and UTC timestamp.

    Args:
        lat (float): Latitude.
        lon (float): Longitude.
        dt (int): UTC timestamp (seconds).

    Raises:
        APIError: If the request fails.

    Returns:
        dict: Historical weather data.
    """
    if not OPENWEATHER_API_KEY or not OPENWEATHER_FORECAST_URL:
        raise APIError("API key or forecast URL not configured.")

    params = {
        "lat": lat,
        "lon": lon,
        "dt": dt,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric",
    }
    try:
        res = requests.get(OPENWEATHER_FORECAST_URL, params=params, timeout=10)
        res.raise_for_status()
        return res.json()
    except requests.exceptions.RequestException as e:
        raise APIError(f"Error fetching historical weather: {str(e)}")