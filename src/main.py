import streamlit as st
import requests
import yaml

def load_config() -> dict:
    try:
        with open ('settings.yaml', 'r') as f:
            config = yaml.safe_load(f)
        print(type(config))
        return config
    except FileNotFoundError as e:
        st.error("Config file not found, ensure config.yaml file is present at src/config.yaml")
        return None



# feel free to move around
config = load_config()
weather_api_key = config.get('weather_api_key')
base_weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat=44.34&lon=10.99&appid={weather_api_key}"



def get_weather(city_name: str) -> dict:
    
    """
    Fetch weather from OpenWeather API 
    """

    params = {
        'q': city_name,
        'appid':weather_api_key,
        'units':'metric'
    }
    try:
        response = requests.get(base_weather_url, params=params)
        return response.json()

    except Exception as e:
        st.error(f"Error while fetching weather data: {e}")
        return None



def main():
    st.title("Forecastly")
    weather_data = get_weather('London')
    print(weather_data) #-> returns dict of weather data for labelled city
       


if __name__ == "__main__":
    main()