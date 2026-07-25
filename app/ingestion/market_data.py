import yfinance as yf
from datetime import datetime

def fetch_ftse100() -> dict:
    """Fetch FTSE 100 index data using Yahoo Finance."""
    ftse = yf.Ticker("^FTSE")
    hist = ftse.history(period="1mo")
    if hist.empty:
        return {"error": "No data from Yahoo Finance"}
    latest = hist.iloc[-1]
    return {
        "latest_close": round(latest.Close, 2),
        "latest_date": latest.name.strftime("%Y-%m-%d"),
        "change_pct": round((latest.Close - hist.iloc[-2].Close) / hist.iloc[-2].Close * 100, 2),
        "source": "Yahoo Finance"
    }

def fetch_ftse250() -> dict:
    """Fetch FTSE 250 index data."""
    ftse = yf.Ticker("^FTMC")
    hist = ftse.history(period="1mo")
    if hist.empty:
        return {"error": "No data from Yahoo Finance"}
    latest = hist.iloc[-1]
    return {
        "latest_close": round(latest.Close, 2),
        "latest_date": latest.name.strftime("%Y-%m-%d"),
        "change_pct": round((latest.Close - hist.iloc[-2].Close) / hist.iloc[-2].Close * 100, 2),
        "source": "Yahoo Finance"
    }

def fetch_uk_stock(symbol: str) -> dict:
    """Fetch any UK stock by symbol (e.g., 'BARC.L', 'LLOY.L')."""
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period="1mo")
    if hist.empty:
        return {"error": f"No data for {symbol}"}
    latest = hist.iloc[-1]
    return {
        "symbol": symbol,
        "latest_close": round(latest.Close, 2),
        "latest_date": latest.name.strftime("%Y-%m-%d"),
        "change_pct": round((latest.Close - hist.iloc[-2].Close) / hist.iloc[-2].Close * 100, 2),
        "source": "Yahoo Finance"
    }

def fetch_all_market_data() -> dict:
    return {
        "ftse100": fetch_ftse100(),
        "ftse250": fetch_ftse250(),
        "banks": [fetch_uk_stock(s) for s in ["BARC.L", "LLOY.L", "HSBA.L"]],
        "generated_at": datetime.now().isoformat()
    }