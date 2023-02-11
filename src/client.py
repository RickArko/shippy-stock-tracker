import os
import requests
import pandas as pd
from dotenv import load_dotenv
from typing import Dict

load_dotenv()
API_KEY = os.environ.get("POLYGON_API_KEY")

URL_INFO = "https://api.polygon.io/v3/reference/tickers"
URL_PRICE = "https://api.polygon.io/v1/open-close"


def get_ticker_info(ticker: str) -> Dict:
    """Return dictionary of ticker information."""
    ticker = ticker.upper()
    url = f"{URL_INFO}/{ticker}?apiKey={API_KEY}"
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


def get_ticker_prices(ticker: str, date: str) -> Dict:
    """Return dictionary of daily open/close values.

    Specifically:
        1. ticker
        2. c (close)
        3. h (high)
        4. l (low)
        5. o (open)
        6. t (timestamp)
        7. v (volume)
    """
    ticker = ticker.upper()
    url = f"{URL_PRICE}/{ticker.upper()}/{date}?adjusted=true&apiKey={API_KEY}"
    resp = requests.get(url)
    if resp.status_code != 200:
        raise ValueError(f"Failed to retrieve stock info for {ticker}")
    resp = resp.json()
    d = dict()
    d["ticker"] = ticker
    d["close"] = resp["close"]
    d["open"] = resp["open"]
    d["low"] = resp["low"]
    d["high"] = resp["high"]
    d["timestamp"] = pd.Timestamp.utcnow()
    d["date"] = date
    d["volume"] = resp["volume"]
    return d


if __name__ == "__main__":
    ticker = "AAPL"
    info = get_ticker_info(ticker)
    print(info)
    today = pd.Timestamp("today").strftime("%Y-%m-%d")
    yesterday = (pd.Timestamp("today") - pd.Timedelta(days=1)).strftime("%Y-%m-%d")
    daily = get_ticker_prices(ticker, date=today)
    daily = get_ticker_prices(ticker, date=yesterday)
    print(daily)
