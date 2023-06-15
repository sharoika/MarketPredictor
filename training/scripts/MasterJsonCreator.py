import json

def between(left,right,s):
    before,_,a = s.partition(left)
    a,_,after = a.partition(right)
    return a

def MasterJsonCreator(analyzedTweetsPath, historicStockDataPath, masterTrainerFilePath): 
    analyzedTweets = json.load(open(analyzedTweetsPath))

    HistoricStockTickers = []
    HistoricStockData = []

    for path in historicStockDataPath:
        ticker = between("/", ".", path)
        historicStockData = json.load(open(path))

        HistoricStockTickers.append(ticker)
        HistoricStockData.append(historicStockData)

    dates = []

    for item in HistoricStockData[0]:
        dates.append(item['Date'])

    newJsonList = []

    for date in dates:

        newJson = {"date": date, "stocks": [], "tweets": []}

        for tweet in analyzedTweets:
            if (tweet["date"] == date):
                newJson["tweets"].append({"tweet": {"ticker": tweet["Stock Name"], "polarity": tweet["polarity"], "subjectivity": tweet["subjectivity"]}})

        HistoricStockDataFiltered = []
        for HistoricData in HistoricStockData: 
            for stock in HistoricData:
                if (stock["Date"] == date):
                    HistoricStockDataFiltered.append(stock)

        for ticker, stock in zip(HistoricStockTickers, HistoricStockDataFiltered):

                newJson["stocks"].append({"stock": {"ticker": ticker,       
                                                    "open": stock["Open"],
                                                    "high": stock["High"],
                                                    "low": stock["Low"],
                                                    "close": stock["Close"],
                                                    "volume": stock["Volume"]}})
                
        newJsonList.append(newJson)
                        
    with open(masterTrainerFilePath, 'w', encoding='utf-8') as f:
        json.dump(newJsonList, f, ensure_ascii=False, indent=4)