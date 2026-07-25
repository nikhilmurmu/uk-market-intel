import requests
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ALPHA_VANTAGE_KEY", "demo")
BASE_URL = "https://www.alphavantage.co/query"

def fetch_daily_stock(symbol: str = "IBM") -> dict:
    """Fetch daily time series for a given stock symbol."""
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": API_KEY,
        "outputsize": "compact"
    }
    try:
        resp = requests.get(BASE_URL, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        time_series = data.get("Time Series (Daily)", {})
        if not time_series:
            return {"error": f"No data for {symbol}", "raw": data}
        latest_date = list(time_series.keys())[0]
        latest_close = float(time_series[latest_date]["4. close"])
        return {
            "symbol": symbol,
            "latest_date": latest_date,
            "latest_close": latest_close,
            "source": "Alpha Vantage"
        }
    except Exception as e:
        return {"error": str(e)}

def fetch_ftse100_index() -> dict:
    """Fetch FTSE 100 index."""
    return fetch_daily_stock("^FTSE")
