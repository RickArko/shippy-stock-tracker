import os
from typing import Dict, List

import pandas as pd
import requests
from dotenv import load_dotenv
from fastapi import FastAPI

from main import load_prices, load_info
from src.client import get_ticker_info

URL_INFO = "https://api.polygon.io/v3/reference/tickers"
URL_PRICE = "https://api.polygon.io/v1/open-close"
load_dotenv()
app = FastAPI()

PRICES = load_prices()

dfinfo = load_info()

dfinfo = dfinfo.sort_values("market_cap", ascending=False).reset_index(drop=True)
dfinfo["firm_size"] = "mid_cap"
dfinfo.loc[0:2,"firm_size"] = "large_cap"
dfinfo.loc[(len(dfinfo) - 3):len(dfinfo),"firm_size"] = "small_cap"

PRICES = PRICES.merge(dfinfo[["ticker", "market_cap", "firm_size", "total_employees"]], on="ticker", how="inner")


@app.get("/")
async def root():
    return {"message": "Hello Shippy"}


load_dotenv()
API_KEY = os.environ.get("POLYGON_API_KEY")


@app.get("/details/")
async def details(ticker: str):
    ticker = ticker.upper()
    url = f"{URL_INFO}/{ticker}?apiKey={API_KEY}"
    resp = requests.get(url)

    if resp.status_code != 200:
        return {"error": f"{ticker} not found"}

    resp = resp.json()["results"]
    d = dict()
    d["ticker"] = resp["ticker"]
    d["name"] = resp["name"]
    d["primary_exchange"] = resp["primary_exchange"]
    d["market_cap"] = resp["market_cap"]
    d["address"] = resp["address"]
    d["sic_description"] = resp["sic_description"]
    d["total_employees"] = resp["total_employees"]

    return {
        "ticker": d["ticker"],
        "name": d["name"],
        "primary_exchange": d["primary_exchange"],
        "market_cap": d["market_cap"],
        "address": d["address"],
        "sic_description": d["sic_description"],
        "total_employees": d["total_employees"],
    }


@app.post("/average_ohlc")
async def average_ohlc(symbols: List[str]):
    """
    example:
    symbols = ["AAPL"]
    outputs:
    """
    global PRICES

    return_list = []

    def get_price_dict(dfohlc: pd.DataFrame):
        r = {}
        r["prices"] = {
            "open": dfohlc["open"].mean().round(2),
            "close": dfohlc["close"].mean().round(2),
            "high": dfohlc["high"].mean().round(2),
            "low": dfohlc["low"].mean().round(2),
        }
        r["volume"] = dfohlc["volume"].mean()
        return r

    sym_dict = {}
    for sym in symbols:
        sym_dict[sym] = get_price_dict(PRICES[PRICES["ticker"] == sym])

    return_list.append(sym_dict)
    return {"result": return_list}


@app.get("/get_company_financials")
async def average_ohlc(ticker: str = "AAPL", source: str = "Morning star"):
    """Return a list of dictionaries with all available financials for a given ticker and source.

    INPUT: "AAPL", "Morning star"
    OUTPUT:
        [{"ticker": "AAPL",
            “year”: “2022”
                "financials": {
                    "revenue": 394330000000,
                    "gross_income": 170780000000,
                    "ebitda": 130540000000,
                    "income_tax": 14530000000
                }
            }, {
                "ticker": "AAPL",
                “year”: “2021”,
                "financials": {
                    "revenue": 365820000000,
                    "gross_income": 152840000000,
                    "ebitda": 120230000000,
                    "income_tax": 9680000000
                }
            }]
    """
    from src.parse_financials import find_local_pdf, parse_pdf_text

    try:
        fname = find_local_pdf(ticker, source)
    except ValueError:
        return {"error": f"{ticker} not found by {source}"}

    t = parse_pdf_text(fname)

    resp = {"ticker": ticker, "source": source, "path": str(fname), "raw_text": t}
    return resp


@app.get("/market_cap_rank_analytics/")
async def details():
    global PRICES

    result_list = []

    for cap, dfg in PRICES.groupby("firm_size"):
        res = dict()
        res["avg_marget_cap"] = dfg["market_cap"].mean()
        res["avg_num_employees"] = dfg["total_employees"].mean()
        res["avg_weekly_volume"] = dfg["volume"].mean()
        result_list.append(res)

    return {
        "results": result_list
    }
