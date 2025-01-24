
# Forecastly
Advanced stock forecasting platform based on meteorological data

## Prerequisites
Make sure you're running on python version <b>3.12.6</b> when setting up, as this will ensure full compatibility with the depdendencies listed in here.
Sign up for an Open Weather API key [here](https://openweathermap.org)


## Setting up (macOS and Linux)
1. python -m venv venv
2. Activate virtual environment via the command: ```source venv/bin/activate```
3. Install dependencies into your virtual environment: ```pip install -r requirements.txt```


## Setting up (Windows)
1. python -m venv venv
2. Activate the virtual environment: ```venv\Scripts\activate```
3. Install the required dependencies: ```pip install -r requirements.txt```

## API Setup
- Create a settings.yaml file in src/ and add the field 'WEATHER_API_KEY: 'YOUR_KEY_HERE'
