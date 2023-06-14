from pandas_datareader import data 
from datetime import date, timedelta
import time, json, yfinance
from datetime import datetime


def FinanceScraper(ticker): 

    finances = {}

    investment = yfinance.Ticker(ticker)
    info = investment.info

    print(info)
    # ticker data
    finances["ticker"]=ticker

    # bid and ask data
    finances["open"]=info["open"]
    finances["close"]=info["currentPrice"]
    finances["volume"]=info["volume"]
    finances["high"]=info["regularMarketDayHigh"]
    finances["low"]=info["regularMarketDayLow"]

    with open(time.strftime("%Y-%m-%d")+'.json', 'w', encoding='utf-8') as f:
        json.dump(finances, f, ensure_ascii=False, indent=4)


FinanceScraper("AAPL")