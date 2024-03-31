import yfinance as yf
import pandas as pd


async def get_per(ticker):
    stock = yf.Ticker(ticker)

    financials = stock.financials
    info = stock.info

    diluted_eps: float

    diluted_eps = financials.loc["Diluted EPS"][0]
    if pd.isna(diluted_eps):
        diluted_eps = financials.loc["Diluted EPS"][1]

    current_price = info["currentPrice"]
    per = round(float(current_price) / float(diluted_eps), 2)

    result_dict = {
        "Diluted_EPS": diluted_eps,
        "Current_Price": current_price,
        "PER": per
    }

    return result_dict


async def get_info(ticker):
    stock = yf.Ticker(ticker)

    info = stock.info

    return info


async def get_price_realtime(ticker):
    stock = yf.Ticker(ticker)

    data = stock.history(period="1d", interval="1m")

    return data["Close"]


async def get_price_range(ticker, start, end):
    stock = yf.Ticker(ticker)

    data = stock.history(start=start, end=end)

    return data["Close"]