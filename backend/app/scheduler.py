# app/scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from app.crud import save_weather
from app.db import SessionLocal
from app.config import CITIES
import time
import logging

logger = logging.getLogger(__name__)

def fetch_and_save_all_cities():
    db = SessionLocal()
    for city in CITIES:
        try:
            save_weather(city, db=db)
        except Exception as e:
            logger.error(f"Error saving {city}: {e}")
    db.close()

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetch_and_save_all_cities, 'cron', minute=0)
    scheduler.start()