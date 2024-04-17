from fastapi import FastAPI
from stocks.router import stocks

app = FastAPI()
app.include_router(stocks)


@app.get("/")
async def root():
    return {"message": "Hello FastAPI!"}

