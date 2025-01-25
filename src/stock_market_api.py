import yfinance as yf


class YFinanceSecurity:
    def __init__(self, ticker: str):
        self.ticker = ticker
        self.security = yf.Ticker(ticker)

    def get_historical_data(self, date_range) -> dict:
        """Return the historical data for the security"""
        try:
            return self.security.history(start=date_range[0], end=date_range[1])
        except Exception as e:
            return {"error": str(e)}

    def get_name(self) -> str:
        """Return the name of the security"""
        try:
            return self.security.info.get("shortName", "Name not found")
        except Exception as e:
            return {"error": str(e)}
