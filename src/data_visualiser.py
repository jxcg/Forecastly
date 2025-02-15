"""File handling class responsibile for data visualisation"""

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
        self.date_range = date_range
        self.location = location
        self.weather_attributes = weather_attributes
        self.weather_api = WeatherAPI()

    def create_figure(self) -> go.Figure:
        """Return the figure object for the correlation plotly chart"""
        try:
            data = self.get_chart_data()
        except ValueError as e:
            raise ValueError(e) from e

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            go.Scatter(x=data["date"], y=data["price"], name="Price"),
            secondary_y=False,
        )
        fig.add_trace(
            go.Scatter(
                x=data["date"],
                y=data["aggregrated_weather_score"],
                name="Aggregated Weather Score",
            ),
            secondary_y=True,
        )

        fig.update_layout(
            title_text=self.get_title(),
        )

        fig.update_xaxes(title_text="Date")
        fig.update_yaxes(title_text="Price", secondary_y=False)
        fig.update_yaxes(title_text="Weather Score", secondary_y=True, range=[0, 1])

        return fig

    def get_chart_data(self) -> pd.DataFrame:
        """Return a df for the chart data"""
        pricing = self.security.get_historical_data(self.date_range)
        pricing.index = pricing.index.strftime("%Y-%m-%d")

        pricing_data_dates = pricing.index.tolist()
        weather_attrs = [WEATHER_ATTRIBUTES[key] for key in self.weather_attributes]
        try:
            weather_data = self.weather_api.get_processed_weather_data(
                self.location, pricing_data_dates, weather_attrs
            )
        except ValueError as e:
            raise ValueError(e) from e

        weather_data_dates = weather_data.index.strftime("%Y-%m-%d").tolist()
        pricing = pricing.loc[pricing.index.isin(weather_data_dates)]

        weather_scores = weather_data["score"].tolist()
        print(weather_scores)

        return pd.DataFrame(
            {
                "date": pricing.index,
                "price": pricing["Close"].tolist(),
                "aggregrated_weather_score": weather_scores,
            }
        )

    def get_title(self) -> str:
        """Return the title for the chart"""
        formatted_start_date = self.date_range[0].strftime("%d/%m/%Y")
        formatted_end_date = self.date_range[1].strftime("%d/%m/%Y")
        return f"{self.security.get_name()} against {", ".join(self.weather_attributes)} in {self.location} from {formatted_start_date} to {formatted_end_date}"
