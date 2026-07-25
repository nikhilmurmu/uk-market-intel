import pandas as pd
import numpy as np
import yfinance as yf

def forecast_ftse100_ma(days: int = 30):
    """Calculate a simple moving-average forecast for FTSE 100."""
    ftse = yf.Ticker("^FTSE")
    hist = ftse.history(period="1y")
    if hist.empty:
        return None, None
    
    df = hist[["Close"]].copy()
    df["MA20"] = df["Close"].rolling(window=20).mean()
    df["MA50"] = df["Close"].rolling(window=50).mean()
    
    # Simple forecast: last close + average daily change over the last month
    last_price = df["Close"].iloc[-1]
    daily_changes = df["Close"].pct_change().dropna().tail(30)
    avg_change = daily_changes.mean()
    std_change = daily_changes.std()
    
    forecast_dates = pd.date_range(start=df.index[-1] + pd.Timedelta(days=1), periods=days)
    forecast_prices = [last_price * (1 + avg_change) ** i for i in range(1, days+1)]
    upper = [p * (1 + 2*std_change) for p in forecast_prices]
    lower = [p * (1 - 2*std_change) for p in forecast_prices]
    
    forecast_df = pd.DataFrame({
        "ds": forecast_dates,
        "yhat": forecast_prices,
        "yhat_upper": upper,
        "yhat_lower": lower
    })
    
    # Return historical data with MAs as well
    historical_df = df.reset_index().rename(columns={"Date": "ds", "Close": "y"})
    return forecast_df, historical_df