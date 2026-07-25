from .market_data import fetch_all_market_data
from .ons_indicators import fetch_all_indicators
from datetime import datetime
import json

def run_all():
    result = {
        "market_data": fetch_all_market_data(),
        "economic_indicators": fetch_all_indicators(),
        "generated_at": datetime.now().isoformat()
    }
    return result

if __name__ == "__main__":
    print(json.dumps(run_all(), indent=2, default=str))