from scripts.TweetScraper import scrapeTweets
from scripts.SentimentAnalyzer import analyzeTweets
from scripts.FinanceScraper import FinanceScraper

# .env file contents: 
#
# TW_EMAIL = ""
# TW_USERNAME = ""
# TW_PASSWORD = ""
#

ticker = input("Enter a market ticker: ").upper()

scrapeTweets(ticker)
analyzeTweets()
FinanceScraper(ticker)