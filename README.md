# TeamCity Python Weather App Demo

## 1. Project Purpose

This project is a simple Python command-line application created as a demonstration for a TeamCity tutorial. Its primary goal is to provide a clear, realistic example for showcasing a full CI/CD (Continuous Integration/Continuous Deployment) pipeline, including building, testing, and deploying stages.

## 2. Functionality

The application fetches the current weather for a specified city and country by making a request to the [OpenWeatherMap API](https://openweathermap.org/api). It then saves the retrieved data into a timestamped CSV file.

- **Input**: Takes a `--city` and `--country` (two-letter code) as command-line arguments.
- **Process**: Calls the OpenWeatherMap API to get current weather data.
- **Output**: Creates a CSV file (e.g., `weather_london_20230922110000.csv`) inside the `artifacts/` directory with the following columns:
  - `timestamp`
  - `city`
  - `country`
  - `temperature_celsius`
  - `description`

## 3. How to Run the Application Locally

### Prerequisites
- Python 3
- An API key from [OpenWeatherMap](https://home.openweathermap.org/users/sign_up)

### Setup Steps

1.  **Create and Activate a Virtual Environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Create a Secrets File:**
    Create a file named `.env` in the root of the project and add your API key to it:
    ```
    OPENWEATHER_API_KEY='YOUR_API_KEY_HERE'
    ```

### Running the Script

Execute the application using Python's `-m` flag to ensure correct module resolution. This will generate a new CSV file in the `artifacts/` directory.

```bash
python -m weather_app.main --city "London" --country "GB"
```

## 4. Project Structure

```
. 
├── artifacts/          # Directory for generated CSV files (ignored by git)
├── tests/
│   ├── __init__.py
│   └── test_core.py      # Unit tests for the core API logic
├── venv/               # Python virtual environment (ignored by git)
├── weather_app/
│   ├── __init__.py
│   ├── core.py         # Handles API calls to OpenWeatherMap
│   └── main.py         # Main script entrypoint, handles CLI args and file writing
├── .env                # Stores the secret API key (ignored by git)
├── .gitignore          # Specifies files and directories to be ignored by git
├── README.md           # This file
└── requirements.txt    # Project dependencies
```

## 5. Intended CI/CD Pipeline (TeamCity)

This project was designed to demonstrate the following CI/CD stages in TeamCity:

1.  **Build Stage:**
    - Install dependencies from `requirements.txt`.
    - Run static analysis using `pylint` to check code quality.

2.  **Test Stage:**
    - Execute unit tests using `pytest`.
    - Generate a code coverage report using `pytest-cov` to be displayed in TeamCity.

3.  **Deploy Stage:**
    - Run the main application with sample inputs (e.g., `--city "Berlin" --country "DE"`).
    - The successful execution of this step (exit code 0) and the creation of the CSV file serve as the "deployment."
    - **Publish Artifacts:** Configure TeamCity to treat the `artifacts/` directory as a build artifact, making the generated CSV downloadable from the build results page.
