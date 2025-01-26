
# Forecastly
Advanced stock forecasting platform based on meteorological data

## Prerequisites
Make sure you're running on python version <b>3.12.6</b> when setting up, as this will ensure full compatibility with the depdendencies listed in here.
Sign up for an Open Weather API key [here](https://openweathermap.org)
## Setup
1. Run the command in your project terminal: ```python -m venv venv```
2. <i>Follow step <b>3</b> below in respect to your machine OS</i>

- ### For macOS and Linux
3. Activate virtual environment via the command: ```source venv/bin/activate```

- ### For Windows
3. Activate virtual environment via the command: ```venv\Scripts\activate```
    
     - Refer to <b>Windows Help</b> section if an error occurs
4. Install dependencies into the virtual environment: ```pip install -r requirements.txt```

#### Windows Help
    Error: Running scripts is disabled on your system
<b>Fix:</b> Run the command ``` Set-ExecutionPolicy Unrestricted -Scope Process```

## API Setup
- Create a settings.yaml file in src/ and add the field: ```WEATHER_API_KEY: <YOUR_KEY_HERE>```

## Running the app
```streamlit run src/main.py```