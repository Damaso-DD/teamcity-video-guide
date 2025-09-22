import sys
from unittest.mock import patch, mock_open
from datetime import datetime

import pytest

from weather_app.main import main
from tests.test_core import SUCCESSFUL_RESPONSE


@patch("weather_app.main.get_weather_data")
def test_main_api_failure(mock_get_weather, monkeypatch, capsys):
    """Test the main function when the API call fails."""
    # Simulate providing command-line arguments
    monkeypatch.setattr(sys, 'argv', ['main.py', '--city', 'FailCity', '--country', 'XX'])

    # Simulate the API returning None
    mock_get_weather.return_value = None

    main()

    # Verify that the correct error message was printed
    captured = capsys.readouterr()
    assert "Could not retrieve weather data" in captured.out


@patch("os.makedirs")
@patch("builtins.open", new_callable=mock_open)
@patch("weather_app.main.get_weather_data")
def test_main_success(mock_get_weather, mock_file, mock_makedirs, monkeypatch, capsys):
    """Test the main function on a successful run."""
    city = "London"
    country = "GB"
    
    # Mock command-line arguments
    monkeypatch.setattr(sys, 'argv', ['main.py', '--city', city, '--country', country])

    # Mock the API call to return a successful response
    mock_get_weather.return_value = SUCCESSFUL_RESPONSE

    # Mock datetime to control the timestamp in the filename
    fixed_dt = datetime(2023, 9, 22, 12, 0, 0)
    with patch('weather_app.main.datetime') as mock_dt:
        mock_dt.now.return_value = fixed_dt
        main()

    # 1. Check that the API function was called correctly
    mock_get_weather.assert_called_once_with(city, country)

    # 2. Check that the artifacts directory creation was attempted
    mock_makedirs.assert_called_once_with("artifacts", exist_ok=True)

    # 3. Check that the CSV file was created with the correct name and content
    expected_filename = "artifacts/weather_london_20230922120000.csv"
    mock_file.assert_called_once_with(expected_filename, 'w', newline='', encoding='utf-8')

    handle = mock_file()
    # Check header
    handle.write.assert_any_call('timestamp,city,country,temperature_celsius,description\r\n')
    # Check row data
    handle.write.assert_any_call('2023-09-22 12:00:00,London,GB,15.0,broken clouds\r\n')

    # 4. Check that the success message was printed
    captured = capsys.readouterr()
    assert f"Successfully wrote weather data to {expected_filename}" in captured.out
