import pytest
import requests
from unittest.mock import patch
from weather_app.core import get_weather_data

# Sample successful response from the OpenWeatherMap API
SUCCESSFUL_RESPONSE = {
    "coord": {"lon": -0.1257, "lat": 51.5085},
    "weather": [{"id": 803, "main": "Clouds", "description": "broken clouds", "icon": "04d"}],
    "base": "stations",
    "main": {"temp": 15.0, "feels_like": 14.5, "temp_min": 13.8, "temp_max": 16.1, "pressure": 1012, "humidity": 72},
    "visibility": 10000,
    "wind": {"speed": 4.1, "deg": 80},
    "clouds": {"all": 75},
    "dt": 1661870592,
    "sys": {"type": 2, "id": 2075535, "country": "GB", "sunrise": 1661834885, "sunset": 1661882586},
    "timezone": 3600,
    "id": 2643743,
    "name": "London",
    "cod": 200
}

# Sample 404 Not Found response
NOT_FOUND_RESPONSE = {
    "cod": "404",
    "message": "city not found"
}

@pytest.fixture
def mock_env(monkeypatch):
    """Fixture to mock the environment variable for the API key."""
    monkeypatch.setenv("OPENWEATHER_API_KEY", "fake_api_key")

def test_get_weather_data_success(requests_mock, mock_env):
    """Test a successful API call to get weather data."""
    city = "London"
    country = "GB"
    requests_mock.get("https://api.openweathermap.org/data/2.5/weather", json=SUCCESSFUL_RESPONSE, status_code=200)
    
    data = get_weather_data(city, country)
    
    assert data is not None
    assert data['name'] == city
    assert data['main']['temp'] == 15.0

def test_get_weather_data_city_not_found(requests_mock, mock_env):
    """Test the case where the city is not found (404 error)."""
    city = "InvalidCity"
    country = "XX"
    requests_mock.get("https://api.openweathermap.org/data/2.5/weather", json=NOT_FOUND_RESPONSE, status_code=404)
    
    # The function should catch the HTTPError and return None
    data = get_weather_data(city, country)
    
    assert data is None

def test_get_weather_data_no_api_key(monkeypatch):
    """Test that a ValueError is raised if the API key is not set."""
    monkeypatch.delenv("OPENWEATHER_API_KEY", raising=False)
    
    with pytest.raises(ValueError, match="API key not found"):
        get_weather_data("London", "GB")

def test_get_weather_data_connection_error(requests_mock, mock_env):
    """Test handling of a network connection error."""
    city = "London"
    country = "GB"
    requests_mock.get("https://api.openweathermap.org/data/2.5/weather", exc=requests.exceptions.ConnectionError)
    
    data = get_weather_data(city, country)
    
    assert data is None
