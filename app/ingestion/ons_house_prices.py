from .land_registry import fetch_price_paid_data
from datetime import datetime
from collections import defaultdict
import statistics

def compute_house_price_stats(postcode_prefix: str = "GU") -> dict:
    """Compute local house price statistics from Land Registry data."""
    records = fetch_price_paid_data(postcode_prefix)
    if not records:
        return {"error": "No records found"}
    prices = [r["price"] for r in records]
    avg_price = round(sum(prices) / len(prices), 2)
    median_price = round(statistics.median(prices), 2)
    monthly = defaultdict(list)
    for r in records:
        month = r["date"][:7]
        monthly[month].append(r["price"])
    monthly_avg = {m: round(sum(v)/len(v),2) for m, v in sorted(monthly.items())}
    return {
        "postcode_prefix": postcode_prefix,
        "total_sales": len(records),
        "average_price": avg_price,
        "median_price": median_price,
        "monthly_avg_prices": monthly_avg,
        "source": "HM Land Registry Price Paid Data",
        "generated_at": datetime.now().isoformat()
    }
