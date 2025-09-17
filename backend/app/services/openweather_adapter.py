"""
OpenWeather Adapter.

Encapsula la comunicación con OpenWeather API y maneja errores.

Funciones:
- get_weather(city: str) -> dict
    Obtiene el clima actual de la ciudad en formato JSON y lanza APIError si falla.
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