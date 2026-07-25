import yfinance as yf
from datetime import datetime

SECTOR_TICKERS = {
    "Energy": ["SHEL.L", "BP.L"],
    "Financials": ["HSBA.L", "BARC.L", "LLOY.L"],
    "Technology": ["SGE.L", "AV.L"],
    "Consumer": ["ULVR.L", "TSCO.L"],
    "Healthcare": ["GSK.L", "AZN.L"],
    "Real Estate": ["LAND.L", "BLND.L"],
    "Materials": ["RIO.L", "AAL.L"],
    "Utilities": ["NG.L", "SSE.L"]
}

def fetch_sector_performance():
    """Calculate daily sector performance by averaging constituent stocks."""
    sectors = {}
    for sector, tickers in SECTOR_TICKERS.items():
        daily_changes = []
        for ticker in tickers:
            try:
                t = yf.Ticker(ticker)
                hist = t.history(period="5d")
                if len(hist) >= 2:
                    latest = hist.iloc[-1]
                    prev = hist.iloc[-2]
                    change = (latest.Close - prev.Close) / prev.Close * 100
                    daily_changes.append(change)
            except Exception:
                pass
        if daily_changes:
            sectors[sector] = round(sum(daily_changes) / len(daily_changes), 2)
        else:
            sectors[sector] = 0
    return sectors