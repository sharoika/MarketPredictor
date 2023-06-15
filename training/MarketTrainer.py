from scripts.CsvToAnalyzedJson import MakeJson, AnalyzeTweets
from scripts.MasterJsonCreator import MasterJsonCreator
from scripts.AlgorithmTrainer import AlgorithmTrainer

csvFilePath = 'data/tweets.csv'
jsonFilePath = 'data/temp/tweets.json'
jsonFilePathAnalyzed = 'data/temp/analyzedTweets.json'

historicStockDataPath = ["data/AAPL.json", "data/AMZN.json", "data/MSFT.json", "data/NVDA.json", "data/TSLA.json"]

masterTrainerFilePath = 'data/temp/masterTrainer.json'

modelFilePath = '../MarketPredictionModel'

MakeJson(csvFilePath, jsonFilePath)

AnalyzeTweets(jsonFilePath, jsonFilePathAnalyzed)

MasterJsonCreator(jsonFilePathAnalyzed, historicStockDataPath, masterTrainerFilePath)

AlgorithmTrainer(masterTrainerFilePath, modelFilePath)

print("Model Built Successfully")