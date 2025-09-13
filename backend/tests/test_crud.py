# backend/tests/test_crud.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db import Base
from app.models import Weather
from app.crud import save_weather, validate_weather_data
from app.exceptions import ValidationError, APIError, DatabaseError
from unittest.mock import patch
from app.weather_client import get_weather

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

def fake_weather_api_success(city="Valencia"):
    return {
        "name": city,
        "main": {"temp": 20.0, "humidity": 50},
        "weather": [{"description": "clear sky"}]
    }

def fake_weather_api_incomplete(city):
    return {"name": city, "weather": []}

def fake_weather_api_fail(city):
    raise Exception("API connection error")

@patch("app.crud.get_weather", side_effect=fake_weather_api_success)
def test_save_weather_success(mock_get, db_session):
    save_weather("Valencia", db=db_session)
    saved = db_session.query(Weather).filter_by(city="Valencia").first()
    expected = fake_weather_api_success("Valencia")

    assert saved is not None
    assert saved.temperature == expected["main"]["temp"]
    assert saved.humidity == expected["main"]["humidity"]
    assert saved.description == expected["weather"][0]["description"]

@patch("app.crud.get_weather", side_effect=Exception("Simulated API failure"))
def test_save_weather_api_error(mock_get, db_session):
    with pytest.raises(APIError):
        save_weather("Valencia", db=db_session)

    count = db_session.query(Weather).count()
    assert count == 0

@patch("app.crud.get_weather", return_value={"name": "Valencia", "weather": []})
def test_save_weather_validation_error(mock_get, db_session):
    with pytest.raises(ValidationError):
        save_weather("Valencia", db=db_session)

    count = db_session.query(Weather).count()
    assert count == 0

@patch("app.crud.get_weather")
def test_save_weather_database_error(mock_get, db_session, monkeypatch):
    mock_get.return_value = {
        "name": "Valencia",
        "main": {"temp": 25.0, "humidity": 60},
        "weather": [{"description": "sunny"}]
    }

    def fake_commit():
        raise Exception("Commit failed!")

    monkeypatch.setattr(db_session, "commit", fake_commit)

    with pytest.raises(DatabaseError):
        save_weather("Valencia", db=db_session)

    count = db_session.query(Weather).count()
    assert count == 0