import feedparser
import json
import googlefinance
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import bs4 as bs
import urllib.request
from yahoo_fin import stock_info as si
import datetime
import time

gainers = si.get_day_gainers()
gainers.columns = ['SYM', 'Company', 'Current Price', 'Price Change', 'Percentage Change', 'Volume'	, 'Avg Vol', 'Market Cap', '52 Week Range']
gainers.sort_values("Price Change", axis = 0, ascending = False, inplace = True)

for stock in gainers['SYM']:
    end = datetime.date.today()
    start = end - datetime.timedelta(days=200)

    s_hist_data = si.get_data(stock , start_date = str(start) , end_date = str(end))

    var = s_hist_data.mean(axis=0, skipna = True)
    avg = (float(var[0]) + float(var[1]))/2

    curr_price = si.get_live_price(stock)
    if (avg < curr_price):
        print(stock)


'''
sid = SentimentIntensityAnalyzer()

NewsFeed = feedparser.parse("https://breakingthenews.net/news-feed.xml")

print ('Number of RSS posts :', len(NewsFeed.entries))

for x in range(0, len(NewsFeed.entries)):
    entry = NewsFeed.entries[x]
    print(entry.title)
    ss = sid.polarity_scores(entry.title)
    for k in sorted(ss):
        print('{0}: {1}, '.format(k, ss[k]), end='')
    print()
'''