import argparse
import csv
import os
from datetime import datetime
from weather_app.core import get_weather_data


def main():
    """Main function to run the weather CLI tool."""
    parser = argparse.ArgumentParser(
        description="Get current weather data for a city."
    )
    parser.add_argument(
        "--city", type=str, required=True, help="The city name."
    )
    parser.add_argument(
        "--country", type=str, required=True, help="The two-letter country code."
    )
    args = parser.parse_args()

    city = args.city
    country = args.country

    weather_data = get_weather_data(city, country)

    if weather_data:
        # Extract relevant information
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        temperature = weather_data.get('main', {}).get('temp')
        description = weather_data.get('weather', [{}])[0].get('description')

        # Prepare data for CSV
        output_data = {
            'timestamp': timestamp,
            'city': city,
            'country': country,
            'temperature_celsius': temperature,
            'description': description
        }

        # Define the output directory and ensure it exists
        output_dir = "artifacts"
        os.makedirs(output_dir, exist_ok=True)

        # Generate a unique filename
        file_timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        city_slug = city.lower().replace(' ', '_')
        filename = os.path.join(
            output_dir, f"weather_{city_slug}_{file_timestamp}.csv"
        )

        # Write to CSV
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = output_data.keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                writer.writerow(output_data)

            print(f"Successfully wrote weather data to {filename}")
        except IOError as e:
            print(f"Error writing to file: {e}")
    else:
        print(
            "Could not retrieve weather data. "
            "Please check your inputs and API key."
        )


if __name__ == "__main__":
    main()
