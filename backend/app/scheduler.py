# app/scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from app.crud import save_weather
from app.db import SessionLocal

CITIES = ["Arrecife", "Madrid", "Barcelona", "London", "New York"]

def fetch_and_save_all_cities():
    db = SessionLocal()
    for city in CITIES:
        try:
            save_weather(city, db=db)
        except Exception as e:
            print(f"Error guardando {city}: {e}")
    db.close()

scheduler = BackgroundScheduler()
scheduler.add_job(fetch_and_save_all_cities, 'interval', minutes=60)
scheduler.start()