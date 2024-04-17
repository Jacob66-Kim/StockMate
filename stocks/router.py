from .yfgetter import (get_per, get_info, get_volume_range, get_volume_realtime, get_price_realtime
, get_price_range, find_ticker_by_name, find_ticker_by_comname)
from fastapi.responses import JSONResponse
from fastapi import APIRouter

stocks = APIRouter(
    tags=["stocks"]
)


@stocks.get("/stocks/{ticker}", summary="주식 정보 조회", response_class=JSONResponse)
async def get_stock_info(ticker: str):
    info = await get_info(ticker)

    return info


@stocks.get("/stocks_per/{ticker}", summary="재무제표 PER 값 호출", response_class=JSONResponse)
async def get_stock_per(ticker: str):
    per = await get_per(ticker)

    return per

@stocks.get("/stocks_price_realtime/", summary="주식 실시간 가격 정보 조회", response_class=JSONResponse)
async def get_stock_price_realtime(ticker: str):
    price = await get_price_realtime(ticker)

    return price


@stocks.get("/stocks_price_range/", summary="주식 범위 가격 정보 조회", response_class=JSONResponse)
async def get_stock_price_range(ticker: str, start: str, end: str):
    price = await get_price_range(ticker, start, end)

    return price


@stocks.get("/stocks_volume_realtime/", summary="주식 실시간 거래량 정보 조회", response_class=JSONResponse)
async def get_stock_volume_realtime(ticker: str):
    volume = await get_volume_realtime(ticker)

    return volume.to_dict()


@stocks.get("/stocks_volume_range/", summary="주식 범위 거래량 정보 조회", response_class=JSONResponse)
async def get_stock_volume_range(ticker: str, start: str, end: str):
    volume = await get_volume_range(ticker, start, end)

    return volume.to_dict()


@stocks.get("/find_ticker/", summary="주식 Ticker 정보 검색용", response_class=JSONResponse)
async def find_ticker(comname: str):
    ticker = await find_ticker_by_comname(comname)

    return ticker


'''
@app.get("/search_ticker/{en_comname}", response_class=JSONResponse)
async def get_search_ticker(en_comname: str):
    ticker = await find_ticker_by_name(en_comname)

    return {"ticker": ticker}
'''