import datetime
import time

import alpaca_trade_api as tradeapi
import feedparser
import nltk
import numpy as np
import pandas as pd
import pandas_helper_calc
import requests
import talib
from fuzzywuzzy import process
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from yahoo_fin import stock_info as si

def getCompany(text):
    r = requests.get('https://api.iextrading.com/1.0/ref-data/symbols')
    stockList = r.json()
    return process.extractOne(text, stockList)[0]

keys_file = open("keys.txt")
lines = keys_file.readlines()

API_KEY = lines[0].rstrip()
API_SECRET = lines[1].rstrip()
APCA_API_BASE_URL = "https://paper-api.alpaca.markets"

api = tradeapi.REST(API_KEY, API_SECRET, APCA_API_BASE_URL, 'v2')

minFrame = "1Min"
dayFrame = "1Day"

f = open("log.txt","w+")

def awaitMarketOpen():
	isOpen = api.get_clock().is_open
	while(not isOpen):
		clock = api.get_clock()
		openingTime = clock.next_open.replace(tzinfo=datetime.timezone.utc).timestamp()
		currTime = clock.timestamp.replace(tzinfo=datetime.timezone.utc).timestamp()
		timeToOpen = int((openingTime - currTime) / 60)
		print(str(timeToOpen) + " minutes til market open.")
		time.sleep(60)
		isOpen = api.get_clock().is_open


nltk.download('vader_lexicon')



while True:
    awaitMarketOpen()
    url = "https://www.investing.com/rss/news.rss"
    sid = SentimentIntensityAnalyzer()
    NewsFeed = feedparser.parse(url)
    for x in range(0, len(NewsFeed.entries)):
        entry = NewsFeed.entries[x]
        ss = sid.polarity_scores(entry.title)
        if ss['compound'] > 0.5:
            for word in entry.title:
                ticker = ''
                ticker = getCompany(word)['symbol']
                if ticker != '':
                    print(ticker)
                    break
            print("BUY", entry.title)
            print(ss['compound'])

            returned = api.submit_order(symbol,int(5),"buy","market","gtc") # Market order to open position
            print(returned)
            print(str(returned.symbol) + ' ' + str(datetime.date.today()) + '\n')
            
        if ss['compound'] < 0.5:
            print("SELL", entry.title)
            print(ss['compound'])
        else:
            print("Neutral:  ", entry.title)
            for k in sorted(ss):
                print('{0}: {1}, '.format(k, ss[k]), end='')
            print()

######## GET TODAYS GAINERS ########