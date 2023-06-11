from textblob import TextBlob
import json, time

with open('scraped/'+time.strftime("%Y-%m-%d")+'.json') as inputData:
  tweets = json.load(inputData)

  for tweet in tweets:
      (polarity, subjectivity) = (TextBlob(tweet['text']).sentiment)
      tweet['subjectivity'] = subjectivity
      tweet['polarity'] = polarity

with open('analyzed/'+time.strftime("%Y-%m-%d")+'.json', 'w', encoding='utf-8') as f:
    json.dump(tweets, f, ensure_ascii=False, indent=4)

print("Tweets Analyzed: " + str(len(tweets)))