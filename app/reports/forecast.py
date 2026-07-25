import pandas as pd
from prophet import Prophet
import yfinance as yf

def forecast_ftse100(days: int = 30):
    """Train Prophet on FTSE 100 history and return forecast dataframe."""
    ftse = yf.Ticker("^FTSE")
    hist = ftse.history(period="2y")
    if hist.empty:
        return None
    
    df = hist.reset_index()[["Date", "Close"]].rename(columns={"Date": "ds", "Close": "y"})
    model = Prophet(daily_seasonality=True)
    model.fit(df)
    future = model.make_future_dataframe(periods=days)
    forecast = model.predict(future)
    return forecast, model