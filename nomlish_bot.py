# System
import sys

# Nomlish
import re
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup

# Twitter
import config
from twitter import *

# Timestamp
import time
import datetime
import calendar

# Twitter Object
t = Twitter(auth=OAuth(config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET, config.CONSUMER_KEY, config.CONSUMER_SECRET))

def TrimURL1(text):
    return re.sub(r"(https?|ftp)(:\/\/[-_\.!~*\'()a-zA-Z0-9;\/?:\@&=\+\$,%#]+)", "", text)

def TrimURL2(text):
    return re.sub(r"http\S+", "", text)

def TrimReply(text):
    return re.sub(r"@\w+", "", text)

def TrimHashTag(text):
    return re.sub(r"#\S+", "", text)

def TrimInvalidString(text):
    trimed = TrimURL1(text)
    trimed = TrimURL2(text)
    trimed = TrimReply(trimed)
    trimed = TrimHashTag(trimed)
    return trimed

def TranslateTweets(original_tweets):
    print("TranslateTweets()")

    translated_count = 0
    translated_tweets = []
    url = "https://racing-lagoon.info/nomu/translate.php"

    options = Options()
    options.headless = True
    browser = webdriver.Firefox(options=options)
    '''
    browser = webdriver.Firefox()
    '''

    browser.get(url)

    print("Started translation")

    for tweet in original_tweets:

        text = TrimInvalidString(tweet)

        print(text)

        input_before = browser.find_element_by_name("before")
        input_before.send_keys(text)

        submit_button = browser.find_element_by_name("transbtn")
        submit_button.click()

        html = browser.page_source

        soup = BeautifulSoup(html, 'html.parser')

        translated_tweet = soup.find_all("textarea")[1].string
        translated_tweets.append(translated_tweet)

        translated_count += 1
        print(translated_count)

    browser.quit()

    return translated_tweets

def GetTweets(user_screen_name, get_count):

    if not hasattr(GetTweets, 'last_created_at'):
        GetTweets.last_created_at = time.strftime("%Y%m%d%H%M%S")

    print("GetTweets()")
    print("last_created_at : ", end ="")
    print(GetTweets.last_created_at)

    tweets = []
    timelines = t.statuses.user_timeline(screen_name=user_screen_name, count=get_count)

    last_created_at = None

    for timeline in timelines:
        created_at = time.strptime(timeline['created_at'], "%a %b %d %H:%M:%S +0000 %Y")
        created_at = calendar.timegm(created_at)
        created_at = time.localtime(created_at)
        created_at = time.strftime("%Y%m%d%H%M%S", created_at)
        print(created_at)

        if created_at > GetTweets.last_created_at:
            tweets.append(timeline['text'])
            if last_created_at is None:
                last_created_at = created_at

    if last_created_at is not None:
        GetTweets.last_created_at = last_created_at

    return tweets

def UpdateTweets(tweets):
    print("UpdateTweets()")
    for tweet in tweets:
        t.statuses.update(status=tweet)

def Tick(target_user):
    print("Tick()")
    tweets = GetTweets(target_user, 10)
    translatedTweets = TranslateTweets(tweets)
    UpdateTweets(translatedTweets)
    print(translatedTweets)

if __name__ == '__main__':

    if len(sys.argv) != 2:
        print("argument is invalid.")
        sys.exit()

    target_user = sys.argv[1]

    get_tweet_interval = 60
    get_tweet_count = 10

    start_time = time.time()
    Tick(target_user)

    while True:
        if time.time() - start_time > get_tweet_interval:
            start_time = time.time()
            Tick(target_user)
