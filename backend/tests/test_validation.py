# tests/test_validation.py
import pytest
from app.crud import validate_weather_data
from app.exceptions import ValidationError
from app.config import TEMP_MIN, TEMP_MAX, HUMIDITY_MIN, HUMIDITY_MAX

def test_validate_weather_data_success():
    data = {
        "name": "Valencia",
        "main": {"temp": 25.0, "humidity": 60},
        "weather": [{"description": "sunny"}]
    }
    result = validate_weather_data(data, "Valencia")
    assert result["city"] == "Valencia"
    assert result["temperature"] == 25.0
    assert result["humidity"] == 60
    assert result["description"] == "sunny"

@pytest.mark.parametrize(
    "data",
    [
        {"name": "Valencia", "main": None, "weather": [{"description": "sunny"}]},
        {"name": "Valencia", "main": {"temp": 25}, "weather": None},
    ]
)
def test_validate_weather_data_missing_main_or_weather(data):
    with pytest.raises(ValidationError):
        validate_weather_data(data, "Valencia")


@pytest.mark.parametrize(
    "data",
    [
        {"name": None, "main": {"temp": 25, "humidity": 60}, "weather": [{"description": "sunny"}]},
        {"name": "Valencia", "main": {"temp": None, "humidity": 60}, "weather": [{"description": "sunny"}]},
        {"name": "Valencia", "main": {"temp": 25, "humidity": None}, "weather": [{"description": "sunny"}]},
    ]
)
def test_validate_weather_data_incomplete_fields(data):
    with pytest.raises(ValidationError):
        validate_weather_data(data, "Valencia")

def test_validate_weather_data_out_of_range(caplog):
    data = {
        "name": "Valencia",
        "main": {"temp": TEMP_MAX + 10, "humidity": HUMIDITY_MAX + 10},
        "weather": [{"description": "hot"}]
    }
    result = validate_weather_data(data, "Valencia")
    assert result["temperature"] == TEMP_MAX + 10
    assert result["humidity"] == HUMIDITY_MAX + 10
    assert "Temperature out of expected range" in caplog.text
    assert "Humidity out of expected range" in caplog.text

