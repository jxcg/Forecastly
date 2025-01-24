import yaml
import requests
import random

# make this file a class like the other files
# see data visualiser and the stock market one

def load_config() -> dict:
    try:
        with open("settings.yaml", "r") as file:
            config = yaml.safe_load(file)
        return config
    except FileNotFoundError:
        return {}


def get_api_key() -> str:
    config = load_config()
    return config.get("WEATHER_API_KEY", "")


weather_api_key = get_api_key()
base_weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat=44.34&lon=10.99&appid={weather_api_key}"


def get_weather(city_name: str) -> dict:
    """
    Fetch weather from OpenWeather API
    """

    params = {"q": city_name, "appid": weather_api_key, "units": "metric"}
    try:
        response = requests.get(base_weather_url, params=params)
        return response.json()

    except Exception as e:
        return {"error": str(e)}

def get_weather_score(amount: int) -> list:
    return [random.uniform(0, 100) for _ in range(amount)]
    # Make this function work properly please
    # It needs to return a list of numbers
    # It should take in a list of weather attributes. eg [temp, uv]
    # get 1 data point for that day each. eg [25C and 12UV]
    # aggregate that into 1 score for the day (make a new func for this) (i recomend it fits the data to some standard (i say between 0 and 1)
    # do this for every day in the date range
    # get this aggregated into a list and return
    # if u did it properly the code should still run
    # ping me (junaid) if u disagree/need help/have questions