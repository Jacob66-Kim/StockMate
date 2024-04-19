import yfinance as yf
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from googletrans import Translator, LANGUAGES

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

    ohlcv_list = [
        {"date": date, "open": row['Open'], "low": row['Low'], "high": row['High'],
         "close": row['Close'], "volume": row['Volume']}
        for date, row in data.iterrows()
    ]

    return ohlcv_list


async def get_price_range(ticker, start, end):
    stock = yf.Ticker(ticker)

    data = stock.history(start=start, end=end)

    ohlcv_list = [
        {"date": date, "open": row['Open'], "low": row['Low'], "high": row['High'],
         "close": row['Close'], "volume": row['Volume']}
        for date, row in data.iterrows()
    ]

    return ohlcv_list


async def get_volume_realtime(ticker):
    stock = yf.Ticker(ticker)

    data = stock.history(period="1d", interval="1m")

    return data["Volume"]


async def get_volume_range(ticker, start, end):
    stock = yf.Ticker(ticker)

    data = stock.history(start=start, end=end)

    return data["Volume"]


async def find_ticker_by_comname(comname):
    # Load the CSV file
    file_path = 'stocks/TRADE_TICKER_COMNAME_ALL.csv'
    data = pd.read_csv(file_path)

    # Translator 객체 생성
    translator = Translator()

    # 입력 텍스트의 언어 감지
    detected_language = translator.detect(comname).lang

    # 대상 언어 설정: 영어면 한국어로, 한국어면 영어로 번역
    if detected_language == 'ko':
        dest_language = 'en'
    else:
        # 감지된 언어가 영어나 한국어가 아닌 경우, 기본적으로 영어로 설정
        dest_language = 'en'

    # 번역 실행
    translation_comname = translator.translate(comname, dest=dest_language)

    # Search for the company name in the COMNAME column
    match = data[data['COMNAME'].str.contains(translation_comname.text, case=False, na=False)]

    # If there's at least one match, return the first one's ticker
    if not match.empty:
        result = [{"TICKER": row['TICKER'], "COMNAME": row['COMNAME']} for index, row in match.iterrows()]

        return result
    else:
        return "Ticker not found for the given company name."


# 리눅스에서 동작 안해서 미사용
async def find_ticker_by_name(company_name):

    try:
        # Selenium 드라이버 설정
        # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        # excutable_path는 chromdriver가 위치한 경로를 적어주면 된다. code와 동일한 경로일 경우 아래처럼 'chromdriver' 만 적어주거나 아예 excutable_path 자체가 없어도 된다. 이해를 위해 써놓았을 뿐.
        # ex) driver = webdriver.Chrome(chrome_options=chrome_options)
        driver = webdriver.Chrome()
        # Yahoo Finance에서 종목명으로 검색하는 URL 구성
        search_url = f"https://finance.yahoo.com/lookup/?s={company_name}"

        # Yahoo Finance 검색 페이지로 이동
        driver.get(search_url)

        # 페이지 로딩 대기
        driver.implicitly_wait(10)  # 필요에 따라 시간 조정

        # 페이지의 HTML 소스 가져오기
        html = driver.page_source

        # BeautifulSoup 객체 생성
        soup = BeautifulSoup(html, 'html.parser')

        ticker: str = ""

        # 'data-symbol' 속성을 찾습니다.
        a_tag = soup.find('a', class_='Fw(b)', attrs={'data-symbol': True})
        # 'data-symbol' 속성의 값을 추출합니다.
        ticker = a_tag['data-symbol'] if a_tag else 'Not Found'

        driver.close()

        return ticker
    except AttributeError:
        # 검색 결과가 없거나 구조가 예상과 다를 때
        return "Ticker not found or search page structure has changed."

