import csv
import json
from textblob import TextBlob
 
csvFilePath = 'stock_tweets.csv'
jsonFilePath = 'stock_tweets.json'
jsonFilePathAnalyzed = 'stock_tweets_analyzed.json'

def make_json(csvFilePath, jsonFilePath):
     
    data = []

    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)

        for rows in csvReader:
             
            data.append(rows)
 
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(data, indent=4))

def analyzeTweets(jsonFilePath, jsonFilePathAnalyzed): 
    with open(jsonFilePath) as inputData:
        tweets = json.load(inputData)

    for tweet in tweets:
        (polarity, subjectivity) = (TextBlob(tweet['Tweet']).sentiment)
        tweet['subjectivity'] = subjectivity
        tweet['polarity'] = polarity
        tweet['date'] = tweet['Date'][0:10]

    with open(jsonFilePathAnalyzed, 'w', encoding='utf-8') as f:
        json.dump(tweets, f, ensure_ascii=False, indent=4)

    print("Tweets Analyzed: " + str(len(tweets)))



make_json(csvFilePath, jsonFilePath)
analyzeTweets(jsonFilePath, jsonFilePathAnalyzed)