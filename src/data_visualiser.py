"""File handling class responsibile for data visualisation"""

from typing import Tuple
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from stock_market_api import YFinanceSecurity
from weather_api import WeatherAPI
from constants import WEATHER_ATTRIBUTES


class DataVisualiser:
    """Class handling data formatting and graph preparation"""

    def __init__(
        self, date_range: tuple, ticker: str, location: str, weather_attributes: list
    ):
        self.ticker = ticker
        self.security = YFinanceSecurity(ticker)
        self.location = location
        self.weather_attributes = weather_attributes
        self.weather_api = WeatherAPI()

        if date_range[0] == date_range[1]:
            raise ValueError("Date range must be at least 1 day")
        self.date_range = date_range

    def create_figure(self) -> go.Figure:
        """Return the figure object for the correlation plotly chart"""
        data = self.get_chart_data()
        start_date = data["date"].iloc[0]
        end_date = data["date"].iloc[-1]
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            go.Scatter(x=data["date"], y=data["price"], name="Price"),
            secondary_y=True,
        )
        fig.add_trace(
            go.Scatter(
                x=data["date"],
                y=data["aggregrated_weather_score"],
                name="Aggregated Weather Score",
            ),
            secondary_y=False,
        )

        fig.update_layout(
            title_text=self.get_title(start_date, end_date),
        )

        fig.update_xaxes(title_text="Date")
        fig.update_yaxes(title_text="Price", secondary_y=True)
        fig.update_yaxes(title_text="Weather Score", secondary_y=False, range=[0, 1])

        return fig

    def get_chart_data(self) -> pd.DataFrame:
        """Return a df for the chart data"""
        pricing = self.security.get_historical_data(self.date_range)
        pricing_data_dates = pricing.index.tolist()

        weather_attrs = [WEATHER_ATTRIBUTES[key] for key in self.weather_attributes]
        weather_data = self.weather_api.get_processed_weather_data(
            self.location, pricing_data_dates, weather_attrs
        )
        self.weather_attributes = [
            key
            for key, value in WEATHER_ATTRIBUTES.items()
            if value in weather_data.columns.tolist()
        ]

        weather_data_dates = weather_data.index.strftime("%Y-%m-%d").tolist()
        pricing = pricing.loc[
            pricing.index.strftime("%Y-%m-%d").isin(weather_data_dates)
        ]

        granularity = self.__calculate_granularity(pricing.index[0], pricing.index[-1])
        pricing = pricing.iloc[::granularity]
        weather_data = weather_data.iloc[::granularity]

        return pd.DataFrame(
            {
                "date": pricing.index.strftime("%Y-%m-%d"),
                "price": pricing["Close"].tolist(),
                "aggregrated_weather_score": weather_data["score"].tolist(),
            }
        )

    def get_correlation(self) -> Tuple[str, str]:
        """Return the correlation between the price and the weather score"""
        data = self.get_chart_data()
        correlation = data["price"].corr(data["aggregrated_weather_score"])
        interpretation = self.__interpret_correlation(correlation)
        message = f"Pearson Correlation Coefficient of {round(correlation,2)}."
        return interpretation.title(), message

    def get_title(self, start_date, end_date) -> str:
        """Return the title for the chart"""
        return (
            f"{self.security.get_name()} against {', '.join(self.weather_attributes)}"
            f" in {self.location.title()} from {start_date} to {end_date}"
        )

    def __interpret_correlation(self, value):
        """Return the interpretation of the correlation value"""
        if value > 0.5:
            correlation = "strong positive correlation"
        elif 0.3 < value <= 0.5:
            correlation = "moderate positive correlation"
        elif 0.1 < value <= 0.3:
            correlation = "weak positive correlation"
        elif -0.1 <= value < 0.1:
            correlation = "no correlation"
        elif -0.3 <= value < -0.1:
            correlation = "weak negative correlation"
        elif -0.5 <= value < -0.3:
            correlation = "moderate negative correlation"
        else:
            correlation = "strong negative correlation"

        return correlation

    def __calculate_granularity(self, start_date, end_date):
        """Return the what granularity to use between two dates"""
        delta = (end_date - start_date).days

        if delta <= 365:
            return 1
        if delta <= 3650:
            return 5
        return 20
