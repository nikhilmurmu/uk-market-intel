import requests
import csv
import io
from datetime import datetime

def fetch_price_paid_data(postcode_prefix: str = "GU") -> list:
    """Fetch HM Land Registry Price Paid Data."""
    url = "http://prod.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/pp-2024.csv"
    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        reader = csv.DictReader(io.StringIO(resp.text))
        data = []
        for row in reader:
            pc = row.get("postcode") or row.get("Postcode") or ""
            if pc.startswith(postcode_prefix):
                data.append({
                    "price": int(row.get("price") or row.get("price", 0)),
                    "date": row.get("date_of_transfer") or row.get("date", ""),
                    "postcode": pc,
                    "property_type": row.get("property_type") or row.get("type", ""),
                    "new_build": row.get("new_build_flag") == "Y" or row.get("new_build", "") == "Y",
                    "tenure": row.get("tenure_type") or row.get("tenure", ""),
                    "street": row.get("street") or "",
                    "city": row.get("city") or ""
                })
        return data
    except Exception as e:
        print(f"Error fetching Land Registry data: {e}")
        return []
