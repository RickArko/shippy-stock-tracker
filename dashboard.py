import pandas as pd
import streamlit as st

from main import load_info, load_prices
from src.client import get_ticker_info
import plotly.express as px

st.set_page_config(layout="wide",
                   page_title="Stock Tracker",
                   page_icon="📈"
                   )

DFTICKERS = pd.read_csv("src/data/tickers.csv")
TICKERS = DFTICKERS["Ticker"].unique().tolist()

dfinfo = load_info()
dfprices = load_prices()

st.title("Stock Tracker")
tickers_selected = st.multiselect("Select Tickers", options=TICKERS, default=TICKERS[:5])

start = st.date_input("Start Date", pd.Timestamp(dfprices["date"].min())).strftime("%Y-%m-%d")
end = st.date_input("End Date", pd.Timestamp(dfprices["date"].max())).strftime("%Y-%m-%d")

dfp = dfprices[dfprices["ticker"].isin(tickers_selected)]
dfp = dfp[dfp["date"].between(start, end)]

st.header("OHLC table")
show_cols = ["ticker", "date", "open", "high", "low", "close", "volume",]
st.dataframe(dfp[show_cols].sort_values(["ticker", "date"]), use_container_width=True)

st.header("1-Week Price Chart")
dfp["symbol"] = pd.Categorical(dfp.ticker)
f  = px.line(dfp, x="date", y="close", color="symbol")
st.plotly_chart(f, use_container_width=True)
