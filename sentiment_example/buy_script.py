import datetime
import json
import random
import time
import urllib.request

import bs4 as bs
import feedparser
import googlefinance
import nltk
import pandas as pd
import pandas_helper_calc
import requests
from fuzzywuzzy import process
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from yahoo_fin import stock_info as si


def getCompany(text):
    r = requests.get('https://api.iextrading.com/1.0/ref-data/symbols')
    stockList = r.json()
    return process.extractOne(text, stockList)[0]


'''
DEBUG = True

gainers = si.get_day_gainltners()
gainers.columns = ['SYM', 'Company', 'Current Price', 'Price Change', 'Percentage Change', 'Volume'	, 'Avg Vol', 'Market Cap', '52 Week Range']
gainers.sort_values("Price Change", axis = 0, ascending = False, inplace = True)

end = datetime.date.today()
start = end - datetime.timedelta(days=200)
stock_watchlist = []
for stock in gainers['SYM']:

    s_hist_data = si.get_data(stock , start_date = str(start) , end_date = str(end))

    var = s_hist_data.mean(axis=0, skipna = True)
    avg = (float(var[0]) + float(var[1]))/2

    curr_price = si.get_live_price(stock)
    if (avg < curr_price):
        stock_watchlist.append(stock)
        
print(stock_watchlist)


i =0

# Creating an empty Dataframe with column names only
today_stock_price = pd.DataFrame(columns=stock_watchlist)
i = 0
while i < 100:                  #possible threading?
    if DEBUG:
        i+=1
    if not (DEBUG):
        time.sleep(30)
    data = {}
    for stock in stock_watchlist:
        if (DEBUG):
            data[stock] = random.randint(0, 100)
        else:
            data[stock] = si.get_live_price(stock)
    today_stock_price = today_stock_price.append(data, ignore_index=True)

    if (len(today_stock_price) > 50):
        dy1dx = today_stock_price.calc.derivative()
        var = dy1dx.mean(axis=0, skipna = True)

print(today_stock_price)

'''
url = "https://www.investing.com/rss/news.rss"

nltk.download('vader_lexicon')

sid = SentimentIntensityAnalyzer()

NewsFeed = feedparser.parse(url)

print ('Number of RSS posts :', len(NewsFeed.entries))

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
    if ss['compound'] < 0.5:
        print("SELL", entry.title)
        print(ss['compound'])
    else:
        print("Neutral:  ", entry.title)
        for k in sorted(ss):
            print('{0}: {1}, '.format(k, ss[k]), end='')
        print()
