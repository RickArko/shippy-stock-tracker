#!/usr/bin/env python3
"""Read all symbols in src/data/tickers.csv 

Query Polygon API for:

1. Details - dataframe of features
2. Open/Close - dataframe of 7 days of open/close for each ticker

Save to parquet files for v0 then move to supabase and submit
"""
import time
from pathlib import Path
from typing import Dict, List

import pandas as pd
from loguru import logger

from src.client import get_ticker_info, get_ticker_prices
from src.tickers import TICKERS

FNAME_RESULTS = Path("src").joinpath("data").joinpath("tickers.snap.parquet")
FNAME_INFO = Path("src").joinpath("data").joinpath("ticker-details.snap.parquet")


def update_stocks_info(tickers: List[str], sleep_seconds: int = 20):
    """Create DataFrame of Stock Details to Upload to Database or Parquet File."""
    res = []
    for ticker in TICKERS:
        info = get_ticker_info(ticker)
        logger.info(f"Finished {ticker} sleeping for {sleep_seconds} seconds...")
        time.sleep(sleep_seconds)
        res.append(info)

    dftickers = pd.DataFrame(res)
    dftickers["address"] = dftickers["address"].map(lambda x: x.get("address1", None))
    fname = Path("src").joinpath("data", "ticker-details.snap.parquet")
    fname.parent.mkdir(parents=True, exist_ok=True)
    dftickers.to_parquet(fname)


def create_full_update_list(DF, days, tickers=TICKERS):
    require_update = []
    exists = list(DF[["ticker", "date"]].drop_duplicates().itertuples(index=False))

    for ticker in TICKERS:
        for day in dates:
            tup = (ticker, day)
            if tup in exists:
                continue
            else:
                logger.info(f"Adding {tup} to update list")
                require_update.append(tup)
    return require_update


def load_prices():
    return pd.read_parquet(FNAME_RESULTS)


def load_info():
    return pd.read_parquet(FNAME_INFO)


if __name__ == "__main__":
    main_start = time.time()
    logger.info("Begin Stock Data Refresh...")
    yesterday = pd.Timestamp("today") - pd.Timedelta(days=1)  # .strftime("%Y-%m-%d")
    start_date = (yesterday - pd.Timedelta(days=7)).strftime("%Y-%m-%d")
    end_date = yesterday.strftime("%Y-%m-%d")

    # Read dataframe (DATABASE) if exists
    try:
        DF = pd.read_parquet(FNAME_RESULTS)
    except FileNotFoundError:
        DF = pd.DataFrame(
            columns=[
                "ticker",
                "close",
                "open",
                "low",
                "high",
                "timestamp",
                "date",
                "volume",
            ]
        )

    dates = pd.bdate_range(start=start_date, end=end_date).strftime("%Y-%m-%d").tolist()


    # Update stock details
    if FNAME_INFO.exists():
        dfinfo = pd.read_parquet(FNAME_INFO)
    else:
        update_stocks_info(TICKERS, sleep_seconds=20)

    # Create a global list of tuples (ticker, date)
    # for each of these read required data then pop from the global list
    # run the global list in a while loop until empty
    REQUIRED_UPDATE_LIST = create_full_update_list(DF, dates)

    time_sleep_prices = 45

    new_prices = []

    len(REQUIRED_UPDATE_LIST)
    while len(REQUIRED_UPDATE_LIST) > 0:
        for i, tup in enumerate(REQUIRED_UPDATE_LIST):
            ticker, date = tup

            try:
                price_dict = get_ticker_prices(ticker, date=date)
                new_prices.append(price_dict)
            except Exception as e:
                logger.error(
                    f"Error getting ticker price for {ticker} on {date} sleeping for 100 seconds."
                )
                logger.error(f"Error: {e}")
                time.sleep(60)
                continue

            logger.info(
                f"Finished {date} for {ticker} sleeping {time_sleep_prices} seconds..."
            )
            time.sleep(time_sleep_prices)
            REQUIRED_UPDATE_LIST.pop(i)
            logger.debug(f"API Calls Remaining: {len(REQUIRED_UPDATE_LIST):,d}")


    if len(new_prices) > 0:
        dfnew = pd.DataFrame(new_prices)
        DF = pd.concat([DF, dfnew], axis=0)

    DF = (
        DF.sort_values("timestamp")
        .drop_duplicates(subset=["ticker", "date"], keep="last")
        .sort_values(["ticker", "date"])
        .reset_index(drop=True)
    )
    DF.to_parquet(FNAME_RESULTS)
    logger.info(f"Finished in {time.time() - main_start:,.2f} seconds")
