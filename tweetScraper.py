from parsel import Selector
from playwright.sync_api import sync_playwright
from playwright.sync_api._generated import Page
import json
import time

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

        # if i == 0:
        #     found["views"] = tweet.xpath('.//span[contains(text(),"Views")]/../preceding-sibling::div//text()').get()
        #     found["retweets"] = tweet.xpath('.//a[contains(@href,"retweets")]//text()').get()
        #     found["quote_tweets"] = tweet.xpath('.//a[contains(@href,"retweets/with_comments")]//text()').get()
        #     found["likes"] = tweet.xpath('.//a[contains(@href,"likes")]//text()').get()

        results.append({k: v for k, v in found.items() if v is not None})

    return results


def scrape_tweet(search: str, page: Page):

    page.fill('input[type="text"]', search)
    page.keyboard.press('Enter')

    # page.locator("//span[text()='Latest']").click()

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
    page.fill('input[type="text"]', '[REDACTED]')
    page.keyboard.press('Enter')

    if page.locator("//span[text()='Phone']"):
        page.fill('input[type="text"]', '[REDACTED]')
        page.keyboard.press('Enter')

    page.fill('input[type="password"]', '[REDACTED]')
    page.keyboard.press('Enter')


with sync_playwright() as pw:

    browser = pw.chromium.launch(headless=False, channel="chrome")
    page = browser.new_page(viewport={"width": 1080, "height": 720})

    authentication(page)
    tweet_and_replies = scrape_tweet("#apple", page)

    print("tweets grabbed: "+str(len(tweet_and_replies)))

    with open(time.strftime("%Y-%m-%d")+'.json', 'w', encoding='utf-8') as f:
        json.dump(tweet_and_replies, f, ensure_ascii=False, indent=4)