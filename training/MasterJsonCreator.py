
import json


analyzedTweets = json.load(open('stock_tweets_analyzed.json'))
HistoricStockDataAAPL = json.load(open("data/AAPL.json"))
HistoricStockDataAMZN = json.load(open("data/AMZN.json"))
HistoricStockDataMSFT = json.load(open("data/MSFT.json"))
HistoricStockDataNVDA = json.load(open("data/NVDA.json"))
HistoricStockDataTSLA = json.load(open("data/TSLA.json"))

values = set()
for item in HistoricStockDataAAPL:
    values.add(item['Date'])

newJsonList = []

for value in values:
    newJson = {"date": value, "stocks": [], "tweets": []}

    for tweet in analyzedTweets:
        if (tweet["date"] == value):
            newJson["tweets"].append({"tweet": {"ticker": tweet["Stock Name"], "polarity": tweet["polarity"], "subjectivity": tweet["subjectivity"]}})

    for data in HistoricStockDataAAPL:
        if (data["Date"] == value):
            newJson["stocks"].append({"stock": {"ticker": "AAPL",       
                                                 "open": data["Open"],
                                                 "high": data["High"],
                                                 "low": data["Low"],
                                                 "close": data["Close"],
                                                 "volume": data["Volume"]}})
            

    for data in HistoricStockDataMSFT:
        if (data["Date"] == value):
            newJson["stocks"].append({"stock": {"ticker": "MSFT",       
                                                 "open": data["Open"],
                                                 "high": data["High"],
                                                 "low": data["Low"],
                                                 "close": data["Close"],
                                                 "volume": data["Volume"]}})
            

    for data in HistoricStockDataAMZN:
        if (data["Date"] == value):
            newJson["stocks"].append({"stock": {"ticker": "AMZN",       
                                                 "open": data["Open"],
                                                 "high": data["High"],
                                                 "low": data["Low"],
                                                 "close": data["Close"],
                                                 "volume": data["Volume"]}})
            

    for data in HistoricStockDataNVDA:
        if (data["Date"] == value):
            newJson["stocks"].append({"stock": {"ticker": "NVDA",       
                                                 "open": data["Open"],
                                                 "high": data["High"],
                                                 "low": data["Low"],
                                                 "close": data["Close"],
                                                 "volume": data["Volume"]}})
            
    for data in HistoricStockDataTSLA:
        if (data["Date"] == value):
            newJson["stocks"].append({"stock": {"ticker": "TSLA",       
                                                 "open": data["Open"],
                                                 "high": data["High"],
                                                 "low": data["Low"],
                                                 "close": data["Close"],
                                                 "volume": data["Volume"]}})

    newJsonList.append(newJson)
                       
with open("master_tainer.json", 'w', encoding='utf-8') as f:
    json.dump(newJsonList, f, ensure_ascii=False, indent=4)

print(values)