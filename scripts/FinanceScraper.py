from pandas_datareader import data 
from datetime import date, timedelta
import time, json, yfinance
from datetime import datetime


def FinanceScraper(ticker): 

    finances = {}

    investment = yfinance.Ticker(ticker)
    info = investment.info

    # ticker data
    finances["ticker"]=ticker

    # bid and ask data
    finances["bid"]=info["bid"]
    finances["bidSize"]=info["bidSize"]
    finances["ask"]=info["ask"]
    finances["askSize"]=info["askSize"]

    finances["beta"]=info["beta"]
    finances["trailingPE"]=info["trailingPE"]
    finances["forwardPE"]=info["forwardPE"]
    finances["volume"]=info["volume"]
    finances["regularMarketVolume"]=info["regularMarketVolume"]
    finances["averageVolume"]=info["averageVolume"]
    finances["averageVolume10days"]=info["averageVolume10days"]
    finances["averageDailyVolume10Day"]=info["averageDailyVolume10Day"]
    finances["bookValue"]=info["bookValue"]
    finances["priceToBook"]=info["priceToBook"]
    finances["shortRatio"]=info["shortRatio"]
    finances["currentPrice"]=info["currentPrice"]
    finances["targetHighPrice"]=info["targetHighPrice"]
    finances["targetLowPrice"]=info["targetLowPrice"]
    finances["targetMeanPrice"]=info["targetMeanPrice"]
    finances["targetMedianPrice"]=info["targetMedianPrice"]
    finances["recommendationMean"]=info["recommendationMean"]
    finances["recommendationKey"]=info["recommendationKey"]
    finances["numberOfAnalystOpinions"]=info["numberOfAnalystOpinions"]

    with open(time.strftime("%Y-%m-%d")+'.json', 'w', encoding='utf-8') as f:
        json.dump(finances, f, ensure_ascii=False, indent=4)


FinanceScraper("AAPL")