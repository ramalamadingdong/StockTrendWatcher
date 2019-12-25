import feedparser
import re
from nltk.sentiment.vader import SentimentIntensityAnalyzer

sid = SentimentIntensityAnalyzer()

REPLACE_NO_SPACE = re.compile("[.;:!\'?,\"()\[\]]")
REPLACE_WITH_SPACE = re.compile("(<br\s*/><br\s*/>)|(\-)|(\/)")

def preprocess_reviews(reviews):
    reviews = [REPLACE_NO_SPACE.sub("", line.lower()) for line in reviews]
    reviews = [REPLACE_WITH_SPACE.sub(" ", line) for line in reviews]
    return reviews

NewsFeed = feedparser.parse("https://breakingthenews.net/news-feed.xml")

print ('Number of RSS posts :', len(NewsFeed.entries))

for x in range(0, len(NewsFeed.entries)):
    entry = NewsFeed.entries[x]
    print(entry.title)
    ss = sid.polarity_scores(entry.title)
    for k in sorted(ss):
        print('{0}: {1}, '.format(k, ss[k]), end='')
    print()
