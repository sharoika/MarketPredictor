from parsel import Selector
from playwright.sync_api import sync_playwright
from playwright.sync_api._generated import Page
import json
import time
import os
from dotenv import load_dotenv

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
            #"username": tweet.xpath(".//*[@data-testid='User-Names']/div[1]//text()").get(),
            "handle": tweet.xpath(".//*[@data-testid='User-Names']/div[2]//text()").get(),
            "datetime": tweet.xpath(".//time/@datetime").get(),
            #"verified": bool(tweet.xpath(".//svg[@data-testid='icon-verified']")),
            #"url": tweet.xpath(".//time/../@href").get(),
            #"image": tweet.xpath(".//*[@data-testid='tweetPhoto']/img/@src").get(),
            #"video": tweet.xpath(".//video/@src").get(),
            #"video_thumb": tweet.xpath(".//video/@poster").get(),
            "likes": tweet.xpath(".//*[@data-testid='like']//text()").get(),
            "retweets": tweet.xpath(".//*[@data-testid='retweet']//text()").get(),
            "replies": tweet.xpath(".//*[@data-testid='reply']//text()").get(),
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

    return tweets

def authentication(page: Page):

    page.goto("https://twitter.com/login")
    page.fill('input[type="text"]', TW_EMAIL)
    page.keyboard.press('Enter')

    if not page.get_by_label("Text"):
        print("tets1")
        page.fill('input[type="password"]', TW_PASSWORD)
        page.keyboard.press('Enter')
    else:
        print("tets2")
        page.fill('input[type="text"]', TW_USERNAME)
        page.keyboard.press('Enter')
        page.fill('input[type="password"]', TW_PASSWORD)
    
    page.keyboard.press('Enter')


with sync_playwright() as pw:

    browser = pw.chromium.launch(headless=False, channel="chrome")
    page = browser.new_page(viewport={"width": 1080, "height": 720})

    authentication(page)
    tweet_and_replies = scrape_tweet("#applestock", page)

    print("tweets grabbed: "+str(len(tweet_and_replies)))

    with open(time.strftime("%Y-%m-%d")+'.json', 'w', encoding='utf-8') as f:
        json.dump(tweet_and_replies, f, ensure_ascii=False, indent=4)