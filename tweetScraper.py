import tweepy

bearer = "AAAAAAAAAAAAAAAAAAAAACAToAEAAAAA7BETtb%2BMNYdFY8ziTVTVk9Eazeg%3DiIziBmXFRXS6TMZ5MFIscNs6afvn8QQ8ddGmZJ7syoGy0a0OSA"
  
client = tweepy.Client(bearer)

query = 'keyword:suhemparack -is:retweet'
  
# public_tweets = client.search_recent_tweets(query=query, tweet_fields=['id', 'text'], max_results=10)
# for tweet in public_tweets:
#   print(tweet.text)