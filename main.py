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
gainers.columns = ['SYM', 'COMPANY', 'Current Price', 'Price Change', 'Percentage Change', 'Volume'	, 'Avg Vol', 'Market Cap', '52 Week Range']
gainers.sort_values("Price Change", axis = 0, ascending = False, inplace = True)


end = datetime.date.today()
start = end - datetime.timedelta(days=200)
SYM = "AAPL"
end = str(int(time.mktime(end.timetuple())))
start = str(int(time.mktime(start.timetuple())))

url = 'https://finance.yahoo.com/quote/' + SYM +'/history?period1=' + start +'&period2=' + end + '&interval=1d&filter=history&frequency=1d'
source = urllib.request.urlopen(url).read()

soup = bs.BeautifulSoup(source, features="html.parser")

table = soup.table
table_rows = table.find_all('tr')
rows = []

for tr in table_rows:
    td = tr.find_all('td')
    row = [i.text for i in td]
    rows.append(row)
rows.pop(0)
rows.pop()
rows.pop()

s_hist_data = pd.DataFrame(rows)
s_hist_data.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Adjust Clsoe', 'Vol']

s_hist_data['High'] = s_hist_data ['High'].astype(float)
s_hist_data['Low']  = s_hist_data ['Low'].astype(float)

#print(s_hist_data)
#print(s_hist_data.mean(axis=0, skipna = True)) 
var = s_hist_data.mean(axis=0, skipna = True)
avg = (float(var[0]) + float(var[1]))/2

print(si.get_live_price("aapl"))





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