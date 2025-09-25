from app.exceptions import ValidationError
import re
from datetime import datetime

def validate_temperature(temp: float) -> None:
    """
    Validates that the temperature is within a reasonable range.

    Args:
        temp (float): Temperature value to validate.

    Raises:
        ValidationError: If temperature is outside the range -90 to 60 Celsius.
    """
    if not (-90 <= temp <= 60):
        raise ValidationError(detail=f"Temperature {temp} out of valid range (-90 to 60°C).")

def validate_date(date_str: str) -> None:
    """
    Validates that the date string is in ISO format (YYYY-MM-DD).

    Args:
        date_str (str): Date string to validate.

    Raises:
        ValidationError: If date format is invalid.
    """
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ValidationError(detail=f"Invalid date format: {date_str}. Expected YYYY-MM-DD.")

def validate_city_name(city: str) -> None:
    """
    Validates that the city name contains only letters, spaces, or hyphens.

    Args:
        city (str): City name to validate.

    Raises:
        ValidationError: If city name contains invalid characters.
    """
    if not re.match(r"^[a-zA-Z\s\-]+$", city):
        raise ValidationError(detail=f"Invalid city name: {city}. Only letters, spaces, and hyphens allowed.")

def validate_weather_data(data: dict, city: str) -> dict:
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
    from app.config import TEMP_MIN, TEMP_MAX, HUMIDITY_MIN, HUMIDITY_MAX
    import logging
    logger = logging.getLogger(__name__)

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
