import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather_data(city, country_code):
    """Fetches weather data from the OpenWeatherMap API."""
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        raise ValueError(
            "API key not found. Please set the OPENWEATHER_API_KEY "
            "environment variable."
        )

    params = {
        'q': f'{city},{country_code}',
        'appid': api_key,
        'units': 'metric'  # Request temperature in Celsius
    }

    try:
        response = requests.get(API_BASE_URL, params=params, timeout=10)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.json()
    except requests.exceptions.HTTPError as e:
        # Handle HTTP errors (e.g., 401 Unauthorized, 404 Not Found)
        print(
            f"HTTP Error: {e.response.status_code} {e.response.reason}"
        )
        print(f"Response body: {e.response.text}")
        return None
    except requests.exceptions.RequestException as e:
        # Handle connection errors, timeouts, etc.
        print(f"Error fetching weather data: {e}")
        return None
