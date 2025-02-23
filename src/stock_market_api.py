"""Wrapper file for querying yfinance"""

from datetime import timedelta
import yfinance as yf


class YFinanceSecurity:
    """Wrapper for each security"""

    def __init__(self, ticker: str):
        self.ticker = ticker
        self.security = yf.Ticker(ticker)

    def get_historical_data(self, date_range) -> dict:
        """Return the historical data for the security"""
        history = self.security.history(
            start=date_range[0], end=date_range[1] + timedelta(days=1)
        )
        if not history.empty:
            return history
        raise ValueError(f"yfinance: No data found for '{self.ticker}'")

    def get_name(self) -> str:
        """Return the name of the security"""
        return self.security.info.get("shortName", "Name not found")
