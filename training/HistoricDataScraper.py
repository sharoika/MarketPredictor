# 30-09-2021 to 30-09-2022
# https://www.kaggle.com/datasets/equinxx/stock-tweets-for-sentiment-analysis-and-prediction

import yfinance as yf
import json
from datetime import datetime

def FinanceScraper(ticker):
    investment = yf.Ticker(ticker)
    info = investment.history(interval="1d", start=datetime(2021, 9, 30), end=datetime(2022, 9, 30))

    info.reset_index(inplace=True)  # Added parentheses to call the method
    info["Date"] = info["Date"].dt.strftime("%Y-%m-%d")  # Corrected column name

    records = info.to_dict("records")

    with open(datetime.today().strftime("%Y-%m-%d") + '.json', 'w', encoding='utf-8') as f:
        json.dump(records, f, ensure_ascii=False, indent=4)

FinanceScraper("AAPL")