# app/weather_client.py
"""
Weather Client Module.

This module provides functions to fetch weather data from OpenWeatherMap API.
It loads the API key from environment variables and handles requests/responses.

Functions:
----------
get_weather(city: str, units: str = "metric", lang: str = "en") -> dict
    Fetches current weather for a given city, returning the data as a JSON dictionary.
"""
import os
import requests
from app.config import OPENWEATHER_API_KEY, OPENWEATHER_BASE_URL
from app.exceptions import APIError

def get_weather(city: str, units: str = "metric", lang: str = "en") -> dict:
    """
    Fetch current weather for a given city from OpenWeatherMap API.

    Parameters
    ----------
    city : str
        City name to query.
    units : str, optional
        Measurement units ("metric", "imperial", "standard").
        Default is "metric".
    lang : str, optional
        Response language code (e.g., "en", "es").
        Default is "en".

    Returns
    -------
    dict
        JSON response from OpenWeatherMap API.

    Raises
    ------
    APIError
        If the API request fails or returns a non-200 status code.
    """
    print("city - get_weather - weather_client:", city)
    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": units,
        "lang": lang,
    }
    print("params - get_weather:", params)
    try:
        response = requests.get(OPENWEATHER_BASE_URL, params=params, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise APIError(f"Error fetching weather for {city}: {str(e)}")

    return response.json()