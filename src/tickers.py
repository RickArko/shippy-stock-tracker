from pathlib import Path

import pandas as pd

DATA_DIR = Path("src").joinpath("data")
DFTICKERS = pd.read_csv(DATA_DIR.joinpath("tickers.csv"))
TICKERS = DFTICKERS["Ticker"].unique().tolist()