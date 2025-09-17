"""
Main module for the Weather Dashboard FastAPI backend.

Responsibilities:
- Initialize the FastAPI application.
- Register routers (weather, etc.).
- Configure middlewares (CORS, error handling).
- Start the background scheduler.
- Create database tables at startup.

Exposes endpoints for:
- Health check.
- Weather retrieval from API.
- Weather history (all or by city).
- Weather daily summaries.
- Latest stored record.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db import Base, engine
from app.config import settings
from app.routers import weather
from app.scheduler import start_scheduler
from app.error_handlers import app_error_handler, generic_exception_handler
from app.exceptions import AppError

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Weather Dashboard API")
app.add_exception_handler(AppError, app_error_handler)
app.add_exception_handler(Exception, generic_exception_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(weather.router, prefix="/weather")

start_scheduler()

@app.get("/")
def root():
    return {"message": "Weather Dashboard backend funcionando!"}