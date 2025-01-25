from stock_market_api import YFinanceSecurity
from weather_api import get_weather_score
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


class DataVisualiser:
    def __init__(
        self, date_range: tuple, ticker: str, location: str, weather_attributes: list
    ):
        self.ticker = ticker
        self.security = YFinanceSecurity(ticker)
        self.date_range = date_range
        self.location = location
        self.weather_attributes = weather_attributes

    def create_figure(self) -> go.Figure:
        """Return the figure object for the correlation plotly chart"""
        data = self.get_chart_data()

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
        fig.update_yaxes(title_text="Weather Score", secondary_y=True)

        return fig

    def get_chart_data(self) -> pd.DataFrame:
        """Return a df for the chart data"""
        pricing = self.security.get_historical_data(self.date_range)
        weather_scores = get_weather_score(
            len(pricing.index)
        )  # Joshua come in and do this properly

        return pd.DataFrame(
            {
                "date": pricing.index,
                "price": pricing["Close"].tolist(),
                "aggregrated_weather_score": weather_scores,
            }
        )

    def get_title(self) -> str:
        """Return the title for the chart"""
        return f"{self.security.get_name()} against {", ".join(self.weather_attributes)} in {self.location} from {self.date_range[0].strftime("%d/%m/%Y")} to {self.date_range[1].strftime("%d/%m/%Y")}"
