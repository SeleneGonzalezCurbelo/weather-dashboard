# app/config.py
import os
from dotenv import load_dotenv
from typing import List
from pydantic_settings import BaseSettings

load_dotenv()  

# --- DATABASE ---
POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_DB: str = os.getenv("POSTGRES_DB", "weather")
DB_HOST: str = os.getenv("DB_HOST", "localhost")
DB_PORT: int = int(os.getenv("DB_PORT", 5432))
DATABASE_URL: str = os.getenv(
    "DATABASE_URL",
    f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:{DB_PORT}/{POSTGRES_DB}"
)

# --- FASTAPI ---
FASTAPI_PORT: int = int(os.getenv("FASTAPI_PORT", 8000))

# --- OPENWEATHER ---
OPENWEATHER_API_KEY: str = os.getenv("OPENWEATHER_API_KEY", "")
OPENWEATHER_BASE_URL: str = os.getenv("OPENWEATHER_BASE_URL", "http://api.openweathermap.org/data/2.5/weather")
OPENWEATHER_FORECAST_URL: str = os.getenv("OPENWEATHER_FORECAST_URL", "http://api.openweathermap.org/data/2.5/forecast")

# --- CRON / SCHEDULER ---
CITIES: List[str] = os.getenv("CITIES", "Arrecife,Madrid,Barcelona,London,New York").split(",")
CRON_INTERVAL_SECONDS: int = int(os.getenv("CRON_INTERVAL_SECONDS", 1800)) 

# --- LIMITE DE DATOS ---
TEMP_MIN: float = float(os.getenv("TEMP_MIN", -50))
TEMP_MAX: float = float(os.getenv("TEMP_MAX", 60))
HUMIDITY_MIN: int = int(os.getenv("HUMIDITY_MIN", 0))
HUMIDITY_MAX: int = int(os.getenv("HUMIDITY_MAX", 100))

# --- LOGGING ---
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

VITE_API_BASE_URL: str = os.getenv("VITE_API_BASE_URL")

class Settings(BaseSettings):
    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

settings = Settings()