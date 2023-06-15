import json
import string
import time
from scripts.TweetScraper import scrapeTweets
from scripts.SentimentAnalyzer import analyzeTweets
from scripts.FinanceScraper import FinanceScraper
import tensorflow as tf
from tensorflow import keras
import numpy as np

# .env file contents: 
#
# TW_EMAIL = ""
# TW_USERNAME = ""
# TW_PASSWORD = ""
#

# Developed for: AAPL AMZN MSFT NVDA TSLA

ticker = input("Enter a market ticker: ").upper()

scrapeTweets(ticker)
analyzeTweets()
FinanceScraper(ticker)

with open('analyzed/'+time.strftime("%Y-%m-%d")+'.json') as inputData:
    analyzedTweets = json.load(inputData)

with open('finances/'+time.strftime("%Y-%m-%d")+'.json') as inputData:
    finances = json.load(inputData)

openPrice = finances["open"]
closePrice = finances["close"]
highPrice = finances["high"]
lowPrice = finances["low"]
polarity = float(np.mean([tweet["polarity"] for tweet in analyzedTweets]))
subjectivity = float(np.mean([tweet["subjectivity"] for tweet in analyzedTweets]))

features = []

print("Open Price: " + str(openPrice))
print("Close Price: " + str(closePrice))
print("High Price: " + str(highPrice))
print("Low Price: " + str(lowPrice))
print("Polarity: " + str(polarity))
print("Subjectivity: " + str(subjectivity))

closePrice = closePrice / openPrice
highPrice = highPrice / openPrice
lowPrice = lowPrice / openPrice

features.append([closePrice, highPrice, lowPrice, polarity, subjectivity])
features = np.array(features)

# Load the saved model
model = tf.keras.models.load_model("MarketPredictionModel")

prediction = model.predict(features)

print(time.strftime("%Y-%m-%d"))
print("Close price for " + str(ticker) + ":" + str(finances["close"]))
print("Predicted price for " + str(ticker) + " at close tomorrow: " + str(prediction * finances["close"]))
print("Difference of: " + str(prediction * finances["close"] - finances["close"]))