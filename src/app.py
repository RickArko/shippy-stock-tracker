import os

from dotenv import load_dotenv
from fastapi import FastAPI

from src.client import get_ticker_info

load_dotenv()
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello Shippy"}


@app.get("/details/")
async def details(ticker: str):
    try:
        info_dict = get_ticker_info(ticker)
    except ValueError:
        return {"error": f"{ticker} not found"}
    return {"searching for", f"{ticker}"}
