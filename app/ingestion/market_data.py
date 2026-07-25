import yfinance as yf
import time
from datetime import datetime

def _safe_fetch(ticker, retries=3, delay=5):
    """Fetch ticker history with retry logic for rate limits."""
    for attempt in range(retries):
        try:
            t = yf.Ticker(ticker)
            hist = t.history(period="1mo")
            if not hist.empty:
                latest = hist.iloc[-1]
                prev = hist.iloc[-2] if len(hist) > 1 else latest
                return {
                    "latest_close": round(latest.Close, 2),
                    "latest_date": latest.name.strftime("%Y-%m-%d"),
                    "change_pct": round((latest.Close - prev.Close) / prev.Close * 100, 2),
                    "source": "Yahoo Finance"
                }
        except Exception:
            if attempt < retries - 1:
                time.sleep(delay * (attempt + 1))
            else:
                return {"error": f"Failed to fetch {ticker} after {retries} retries"}
    return {"error": f"No data for {ticker}"}

def fetch_ftse100():
    return _safe_fetch("^FTSE")

def fetch_ftse250():
    return _safe_fetch("^FTMC")

def fetch_uk_stock(symbol: str) -> dict:
    """Fetch any UK stock by symbol and include the symbol in the result."""
    result = _safe_fetch(symbol)
    result["symbol"] = symbol
    return result

def fetch_all_market_data() -> dict:
    """Fetch FTSE indices and bank stocks with built-in delays."""
    return {
        "ftse100": fetch_ftse100(),
        "ftse250": fetch_ftse250(),
        "banks": [
            fetch_uk_stock("BARC.L"),
            fetch_uk_stock("LLOY.L"),
            fetch_uk_stock("HSBA.L")
        ],
        "generated_at": datetime.now().isoformat()
    }