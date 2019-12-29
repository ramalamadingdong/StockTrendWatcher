url = 'https://finance.yahoo.com/quote/' + stock +'/history?period1=' + start +'&period2=' + end + '&interval=1d&filter=history&frequency=1d'
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