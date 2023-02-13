import requests
import pandas as pd
from src.tickers import TICKERS


ENDPOINT = "http://localhost:5000/"

ENDPOINT1 = f"{ENDPOINT}average_ohlc"
ENDPOINT2 = f"{ENDPOINT}get_company_financials"
ENDPOINT3 = f"{ENDPOINT}market_cap_rank_analytics"


def test_details(ticker):
    url = f"{ENDPOINT}details/?ticker={ticker}"
    try:
        r = requests.get(url).json()
        return r
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    # test_details("AAPL")

    resp1 = requests.post(ENDPOINT1, json=TICKERS)
    resp2 = requests.get(ENDPOINT2)  # , json={"ticker": "AAPL", "source": "Morning star"})
    resp3 = requests.get(ENDPOINT3)

    print(f"First Report at {ENDPOINT1} returns: {resp1.json()}")
    print(f"Second Report at {ENDPOINT1} returns: {resp2.json()}")
    print(f"Third Report at {ENDPOINT3} returns: {resp3.json()}")
