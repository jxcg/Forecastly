import streamlit as st

def load_config():
    with open ('config.yaml') as f:
        pass
BASE_REQUEST_URL = f"https://api.openweathermap.org/data/2.5/weather?lat=44.34&lon=10.99&appid={API key}"