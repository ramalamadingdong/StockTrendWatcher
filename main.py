import feedparser
import googlefinance
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import bs4 as bs
import urllib.request

source = urllib.request.urlopen("https://finance.yahoo.com/gainers").read()
soup = bs.BeautifulSoup(source, features="html.parser")
table = soup.table
table_rows = table.find_all('tr')
rows = []
for tr in table_rows:
    td = tr.find_all('td')
    row = [i.text for i in td]
    rows.append(row)
rows.pop(0)
gainers = pd.DataFrame(rows)
gainers.columns = ['SYM', 'COMPANY', 'Current Price', 'Price Change', 'Percentage Change', 'Volume'	, 'Avg Vol', 'Market Cap', '52 Week Range', 'NaN']
gainers['Price Change'] = gainers['Price Change'].str[1:]
gainers['Price Change'] = gainers['Price Change'].astype(float)
gainers.sort_values("Price Change", axis = 0, ascending = False, inplace = True)
print (gainers) 

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