import pandas as pd
import streamlit as st

from main import load_info, load_prices
from src.tickers import TICKERS
from src.client import get_ticker_info
import plotly.express as px

st.set_page_config(layout="wide", page_title="Stock Tracker", page_icon="📈")

dfinfo = load_info()
dfprices = load_prices()

st.title("Stock Tracker")
tickers_selected = st.multiselect("Select Tickers", options=TICKERS, default=TICKERS[:5])

start = st.date_input("Start Date", pd.Timestamp(dfprices["date"].min())).strftime("%Y-%m-%d")
end = st.date_input("End Date", pd.Timestamp(dfprices["date"].max())).strftime("%Y-%m-%d")

dfp = dfprices[dfprices["ticker"].isin(tickers_selected)]
dfp = dfp[dfp["date"].between(start, end)]

st.header("OHLC table")
show_cols = [
    "ticker",
    "date",
    "open",
    "high",
    "low",
    "close",
    "volume",
]
st.dataframe(dfp[show_cols].sort_values(["ticker", "date"]), use_container_width=True)

st.header("1-Week Price Chart")
dfp["symbol"] = pd.Categorical(dfp.ticker)
f = px.line(dfp, x="date", y="close", color="symbol")
st.plotly_chart(f, use_container_width=True)


import plotly.graph_objects as go

st.header("Candlestick Charts")

for ticker, dfg in dfp.groupby("ticker"):
    fig_candle = go.Candlestick(x=dfg["date"], open=dfg["open"], high=dfg["high"], low=dfg["low"], close=dfg["close"])

    fig = go.Figure(data=[fig_candle])
    fig.update_layout(title=f"Candlestick Chart for {ticker}")
    st.plotly_chart(fig, use_container_width=True)
