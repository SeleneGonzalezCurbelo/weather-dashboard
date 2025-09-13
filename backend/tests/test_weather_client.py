# tests/test_weather_client.py
import pytest
from app.weather_client import get_weather
from app.exceptions import APIError
from unittest.mock import patch, MagicMock
import requests

@patch("requests.get")
def test_get_weather_success(mock_get):
    mock_get.return_value.json.return_value = {"name": "Valencia", "main": {"temp": 20}, "weather": [{"description": "sunny"}]}
    mock_get.return_value.status_code = 200
    data = get_weather("Valencia")
    assert data["name"] == "Valencia"

@patch("requests.get")
def test_get_weather_fail(mock_get):
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Client Error")
    mock_get.return_value = mock_response
    with pytest.raises(APIError) as exc_info:
        get_weather("NonexistentCity")
    assert "NonexistentCity" in str(exc_info.value)