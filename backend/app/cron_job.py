# app/cron_job.py
"""
Scheduled job module for periodically fetching and saving weather data.

Intended to be run by a scheduler (cron, Docker loop, or APScheduler).

Function:
- run() : iterates over a list of predefined cities and saves their weather data.

Handles logging of successful and failed saves.
"""
from app.crud import save_weather
from app.config import CITIES
from app.exceptions import AppError
import logging

logger = logging.getLogger(__name__)

def run():
    """
    Fetch and save weather data for each city in CITIES.

    Logs success or failure for each city individually.
    """
    for city in CITIES:
        try:
            save_weather(city)
            logger.info(f"Weather data for {city} saved successfully.")
        except AppError as e:
            logger.error(f"AppError in cron for {city}: {e.message}")
        except Exception as e:
            logger.exception(f"Unexpected error in cron for {city}: {e}")