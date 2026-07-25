from .land_registry import fetch_price_paid_data
from .ons_house_prices import compute_house_price_stats
from .ons_indicators import fetch_all_indicators
from .alpha_vantage import fetch_ftse100_index
from datetime import datetime
import json

def run_all(postcode_prefix: str = "GU"):
    result = {
        "ftse100": fetch_ftse100_index(),
        "economic_indicators": fetch_all_indicators(),
        "house_price_statistics": compute_house_price_stats(postcode_prefix),
        "generated_at": datetime.now().isoformat()
    }
    return result

if __name__ == "__main__":
    data = run_all()
    print(json.dumps(data, indent=2, default=str))
