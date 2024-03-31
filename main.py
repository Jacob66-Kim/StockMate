from fastapi import FastAPI
from stocks.yfgetter import get_info, get_per, get_price_realtime, get_price_range
from fastapi.responses import JSONResponse

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello FastAPI!"}


@app.get("/stocks/{ticker}", response_class=JSONResponse)
async def get_stock_info(ticker: str):
    info = await get_info(ticker)

    return info


@app.get("/stocks_per/{ticker}", response_class=JSONResponse)
async def get_stock_per(ticker: str):
    per = await get_per(ticker)

    return per

@app.get("/stocks_price_realtime/", response_class=JSONResponse)
async def get_stock_price_realtime(ticker: str):
    price = await get_price_realtime(ticker)

    return price


@app.get("/stocks_price_range/", response_class=JSONResponse)
async def get_stock_price_range(ticker: str, start: str, end: str):
    price = await get_price_range(ticker, start, end)

    return price