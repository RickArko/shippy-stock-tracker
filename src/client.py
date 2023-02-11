import os
import requests
import pandas as pd
from dotenv import load_dotenv
from typing import Dict

load_dotenv()
API_KEY = os.environ.get("POLYGON_API_KEY")


def get_ticker_info(ticker: str) -> Dict:
    """Return dictionary of ticker information."""
    url = (
        f"https://api.polygon.io/v3/reference/tickers/{ticker.upper()}?apiKey={API_KEY}"
    )
    resp = requests.get(url)

    if resp.status_code != 200:
        raise ValueError(f"Failed to retrieve stock info for {ticker}")

    resp = resp.json()["results"]
    d = dict()
    d["ticker"] = resp["ticker"]
    d["name"] = resp["name"]
    d["primary_exchange"] = resp["primary_exchange"]
    d["market_cap"] = resp["market_cap"]
    d["address"] = resp["address"]
    d["sic_description"] = resp["sic_description"]
    d["total_employees"] = resp["total_employees"]
    return d
