from parsel import Selector
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from playwright.sync_api._generated import Page
import json, time, os

load_dotenv()
TW_EMAIL = os.getenv("TW_EMAIL")
TW_USERNAME = os.getenv("TW_USERNAME")
TW_PASSWORD = os.getenv("TW_PASSWORD")

def parse_tweets(selector: Selector):

    results = []

    tweets = selector.xpath("//article[@data-testid='tweet']")

    for i, tweet in enumerate(tweets):

        found = {
            "text": "".join(tweet.xpath(".//*[@data-testid='tweetText']//text()").getall()),
            "handle": tweet.xpath(".//*[@data-testid='User-Names']/div[2]//text()").get(),
            "datetime": tweet.xpath(".//time/@datetime").get(),
            "likes": tweet.xpath(".//*[@data-testid='like']//text()").get() or "0",
            "retweets": tweet.xpath(".//*[@data-testid='retweet']//text()").get() or "0",
            "replies": tweet.xpath(".//*[@data-testid='reply']//text()").get() or "0",
            "views": (tweet.xpath(".//*[contains(@aria-label,'Views')]").re("(\d+) Views") or [None])[0],
        }

        results.append({k: v for k, v in found.items() if v is not None})

    return results

def scrape_tweet(search: str, page: Page):

    page.fill('input[type="text"]', search)
    page.keyboard.press('Enter')

    tweets = list()
    for i in range(10):
        html = page.content()
        selector = Selector(html)
        for tweet in parse_tweets(selector):
            tweets.append(tweet)
        page.keyboard.press('Meta+ArrowDown')
        time.sleep(2)

    tweetsFiltered = list()
    for tweet in tweets:
        if tweet not in tweetsFiltered:
            tweetsFiltered.append(tweet)

    return tweetsFiltered

def authentication(page: Page):

    page.goto("https://twitter.com/login")
    page.fill('input[type="text"]', TW_EMAIL)
    page.keyboard.press('Enter')

    time.sleep(2)

    # try:
    #     page.fill('input[type="password"]', TW_PASSWORD)
    #     page.keyboard.press('Enter')
    # except:
    page.fill('input[type="text"]', TW_USERNAME)
    page.keyboard.press('Enter')
    page.fill('input[type="password"]', TW_PASSWORD)
    
    page.keyboard.press('Enter')

def scrapeTweets(ticker):
    with sync_playwright() as pw:

        browser = pw.chromium.launch(headless=False, channel="chrome", timeout=5000)
        page = browser.new_page(viewport={"width": 1080, "height": 720})

        authentication(page)
        tweet_and_replies = scrape_tweet("#"+ticker, page)

        with open('scraped/'+time.strftime("%Y-%m-%d")+'.json', 'w', encoding='utf-8') as f:
            json.dump(tweet_and_replies, f, ensure_ascii=False, indent=4)

        print("Tweets Grabbed: " + str(len(tweet_and_replies)))