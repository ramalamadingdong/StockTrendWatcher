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
import random
import pandas_helper_calc


debugmode = True

gainers = si.get_day_gainers()
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
'''
i =0

# Creating an empty Dataframe with column names only
today_stock_price = pd.DataFrame(columns=stock_watchlist)
i = 0
while i < 100:                  #possible threading?
    if debugmode:
        i+=1
    if not (debugmode):
        time.sleep(30)
    data = {}
    for stock in stock_watchlist:
        if (debugmode):
            data[stock] = random.randint(0, 100)
        else:
            data[stock] = si.get_live_price(stock)
    today_stock_price = today_stock_price.append(data, ignore_index=True)

    if (len(today_stock_price) > 50):
        dy1dx = today_stock_price.calc.derivative()
        var = dy1dx.mean(axis=0, skipna = True)

print(today_stock_price)

'''

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