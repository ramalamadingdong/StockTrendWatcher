import datetime
import numpy as np
import talib
import alpaca_trade_api as tradeapi
from yahoo_fin import stock_info as si
import time

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
		isOpen = self.alpaca.get_clock().is_open

while True:
	awaitMarketOpen()
######## GET TODAYS GAINERS ########

	gainers = si.get_day_gainers()
	gainers.columns = ['SYM', 'Company', 'Current Price', 'Price Change', 'Percentage Change', 'Volume'	, 'Avg Vol', 'Market Cap', '52 Week Range']
	gainers.sort_values("Percentage Change", axis = 0, ascending = False, inplace = True)

	end = datetime.date.today()
	start = end - datetime.timedelta(days=200)

	stock_watchlist = []

	######## Do some Filtering on the best ones ########

	for stock in gainers['SYM']:
		stock_watchlist.append(stock)

	assetsToTrade = stock_watchlist
	print(assetsToTrade)
	print("Stock Universe for the day:", assetsToTrade)
	
	positionSizing = 1/len(assetsToTrade)
	
	iteratorPos = 0
	assetListLen = len(assetsToTrade)

	returned_data = api.get_barset(assetsToTrade, minFrame, limit=100)

	while iteratorPos < assetListLen:
		symbol = assetsToTrade[iteratorPos]
		timeList = []
		openList = []
		highList = []
		lowList = []
		closeList = []
		volumeList = []

		# Reads, formats and stores the new bars
		for bar in returned_data[symbol]:
			timeList.append(bar.t)
			openList.append(bar.o)
			highList.append(bar.h)
			lowList.append(bar.l)
			closeList.append(bar.c)
			volumeList.append(bar.v)

		# Processes all data into numpy arrays for use by talib
		timeList = np.array(timeList)
		openList = np.array(openList,dtype=np.float64)
		highList = np.array(highList,dtype=np.float64)
		lowList = np.array(lowList,dtype=np.float64)
		closeList = np.array(closeList,dtype=np.float64)
		volumeList = np.array(volumeList,dtype=np.float64)

		# Calculated trading indicators
		try:
			SMA20 = talib.SMA(closeList,20)[-1]

		except:
			iteratorPos += 1
			print("stock doesn't exist on Alpaca don't worry about it.")
			continue
		SMA50 = talib.SMA(closeList,50)[-1]
		SMA3 = talib.SMA(closeList,3)[-1]
		KAMA = talib.KAMA(openList)[-1]
		print(KAMA)

		# Calculates the trading signals
		if SMA20 > SMA50 and SMA3 > 0 and KAMA>50:
			try:
				openPosition = api.get_position(symbol)
			except:
				price = si.get_live_price(symbol)
				cashBalance = api.get_account().cash
				targetPositionSize = float(str(cashBalance)) / (price / positionSizing) # Calculates required position size

				returned = api.submit_order(symbol,int(targetPositionSize),"buy","market","gtc") # Market order to open position
				print(returned)
				f.write(str(returned.symbol) + ' ' + str(datetime.date.today()) + '\n')
				print(str(returned.symbol) + ' ' + str(datetime.date.today()) + '\n')
		else:
			print("decided not to buy: " + symbol + " It didn't meet the requirments today")
		iteratorPos += 1
	positions = api.list_positions()

	if(len(positions) > 5):
		print("Waiting for 24 hours! already have more than 5 positions today!")	
		time.sleep(60 * 24 * 60)
	else:	
		print("Waiting for 1 mins! Then check the rest of possible stocks")
		time.sleep(60 * 5)

