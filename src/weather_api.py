"""Wrapper file for querying weather data from meteostat"""

from geopy.geocoders import Nominatim
from meteostat import Daily, Stations
from sklearn.preprocessing import RobustScaler, MinMaxScaler
import pandas as pd


class WeatherAPI:
    """Wrapper for fetching weather data"""

    def __init__(self):
        self.robust_scaler = RobustScaler()
        self.minmax_scaler = MinMaxScaler()

    def get_processed_weather_data(self, city_name, dates, attrs):
        """Returns relevant weather data per city time range and attributes"""
        try:
            weather_df = self.__get_weather(city_name, dates[0], dates[-1])
        except ValueError as e:
            raise ValueError(e) from e

        filtered_df = self.__filter_data(weather_df, dates, attrs)
        normalised_df = self.__normalise_data(filtered_df, attrs)
        normalised_df["score"] = normalised_df[
            [attr + "_minmax" for attr in attrs]
        ].mean(axis=1)
        return normalised_df

    def __normalise_data(self, df, attrs):
        robust_array = self.robust_scaler.fit_transform(df)
        robust_df = pd.DataFrame(
            robust_array,
            columns=[attr + "_robust" for attr in attrs],
            index=df.index,
        )
        scaled_df = pd.concat([df, robust_df], axis=1)

        minmax_array = self.minmax_scaler.fit_transform(robust_df)
        minmax_df = pd.DataFrame(
            minmax_array,
            columns=[attr + "_minmax" for attr in attrs],
            index=df.index,
        )
        normalised_df = pd.concat([scaled_df, minmax_df], axis=1)
        return normalised_df

    def __filter_data(self, data, dates, attrs):
        cleaned_df = data.fillna(0)
        filtered_df = cleaned_df.loc[data.index.strftime("%Y-%m-%d").isin(dates)]
        filtered_df = filtered_df[attrs]
        return filtered_df

    def __get_weather(self, city_name, start_date, end_date):
        """Returns the raw weather data from meteostat"""
        coords = self.__get_city_coordinates(city_name)
        if not coords:
            raise ValueError(f"Could not get coordinates for {city_name}.")

        station = Stations().nearby(coords[0], coords[1]).fetch(1)
        if station.empty:
            raise ValueError(f"No station found near {city_name}.")

        station_id = station.index[0]
        data = Daily(station_id, start_date, end_date).fetch()
        return data

    def __get_city_coordinates(self, city_name) -> list:
        """Returns the coordinates for a city name"""
        geolocator = Nominatim(user_agent="weather_app")
        location = geolocator.geocode(city_name)
        if location:
            return [location.latitude, location.longitude]
        else:
            return None
