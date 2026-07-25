import requests
import csv
import io
from datetime import datetime

def _parse_ons_csv(url: str, indicator_name: str) -> dict:
    """Download and parse any ONS CSV file automatically."""
    try:
        resp = requests.get(url, timeout=20)
        resp.raise_for_status()
        lines = resp.text.splitlines()
        # Find the first non‑empty line that looks like a header (contains a date or "Title")
        header_idx = None
        for i, line in enumerate(lines):
            if "Title" in line or any(year in line for year in ["2024", "2025", "2026"]):
                header_idx = i
                break
        if header_idx is None:
            # Fallback: use the first line after skipping blank lines
            for i, line in enumerate(lines):
                if line.strip():
                    header_idx = i
                    break
        if header_idx is None:
            return {"error": "Could not find any data in CSV"}
        reader = csv.DictReader(io.StringIO("\n".join(lines[header_idx:])))
        rows = list(reader)
        if not rows:
            return {"error": "Empty CSV after header"}
        # Remove 'Title' column from consideration
        cols = [h for h in rows[0].keys() if h.strip().lower() != "title"]
        # Find the last column with a non‑empty value
        for col in reversed(cols):
            val = rows[0].get(col, "").strip()
            if val and val != "" and val != "N/A":
                return {
                    "indicator": indicator_name,
                    "latest_month": col.strip(),
                    "latest_value": val,
                    "source_url": url
                }
        return {"error": "No valid data found in columns"}
    except Exception as e:
        return {"error": str(e)}

def fetch_cpi_inflation() -> dict:
    url = "https://www.ons.gov.uk/generator?format=csv&uri=/economy/inflationandpriceindices/timeseries/d7g7/mm23"
    return _parse_ons_csv(url, "CPI Inflation (D7G7)")

def fetch_gdp_growth() -> dict:
    url = "https://www.ons.gov.uk/generator?format=csv&uri=/economy/grossdomesticproductgdp/timeseries/ybez/pn2"
    return _parse_ons_csv(url, "GDP Growth (YBEZ)")

def fetch_unemployment() -> dict:
    url = "https://www.ons.gov.uk/generator?format=csv&uri=/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/timeseries/mgsx/lms"
    return _parse_ons_csv(url, "Unemployment Rate (MGSX)")

def fetch_all_indicators() -> dict:
    return {
        "inflation": fetch_cpi_inflation(),
        "gdp": fetch_gdp_growth(),
        "unemployment": fetch_unemployment(),
        "generated_at": datetime.now().isoformat()
    }