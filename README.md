
# Forecastly
Advanced stock forecasting platform based on meteorological data

## Prerequisites
Make sure you're running on python version <b>3.12.6</b> when setting up, as this will ensure full compatibility with the depdendencies listed in here.
Sign up for an Open Weather API key [here](https://openweathermap.org)

## Setup
1. Run command in project terminal: ```python -m venv venv```
2. <i>Follow steps <b>3</b> and <b>4</b> in respect to machine OS</i>

### For macOS and Linux
3. Activate virtual environment via the command: ```source venv/bin/activate```
4. Install dependencies into your virtual environment: ```pip install -r requirements.txt```

### For Windows

3. Activate the virtual environment via the command: ```venv\Scripts\activate```
4. Install the required dependencies: ```pip install -r requirements.txt```

## API Setup
- Create a settings.yaml file in src/ and add the field: ```WEATHER_API_KEY: <YOUR_KEY_HERE>```

## Running the app
```streamlit run src/main.py```