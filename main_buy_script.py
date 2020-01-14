import datetime
import numpy as np
import talib
import alpaca_trade_api as tradeapi
from yahoo_fin import stock_info as si
import time

DEBUG_MODE = False

keys_file = open("keys.txt")
lines = keys_file.readlines()

API_KEY = lines[0].rstrip()
API_SECRET = lines[1].rstrip()
APCA_API_BASE_URL = "https://paper-api.alpaca.markets"

api = tradeapi.REST(API_KEY, API_SECRET, APCA_API_BASE_URL, 'v2')

barTimeframe = "1Min"

i=0
while i<1:
######## GET TODAYS GAINERS ########
	i+=1
	gainers = si.get_day_gainers()
	gainers.columns = ['SYM', 'Company', 'Current Price', 'Price Change', 'Percentage Change', 'Volume'	, 'Avg Vol', 'Market Cap', '52 Week Range']
	gainers.sort_values("Percentage Change", axis = 0, ascending = False, inplace = True)

	end = datetime.date.today()
	start = end - datetime.timedelta(days=200)
	#print(gainers)
	stock_watchlist = []
	######## Do some Filtering on the best ones ########
	if not DEBUG_MODE:
		for stock in gainers['SYM']:
		    #s_hist_data = si.get_data(stock , start_date = str(start) , end_date = str(end))

		    #var = s_hist_data.mean(axis=0, skipna = True)
		    #avg = (float(var[0]) + float(var[1]))/2

		    #curr_price = si.get_live_price(stock)
		    #if (avg < curr_price):	
			stock_watchlist.append(stock)
		assetsToTrade = stock_watchlist[0:8]
		print(assetsToTrade)
		print("Stock Universe for the day:", assetsToTrade)
	else:
		assetsToTrade = ["SPY","MSFT","AAPL","NFLX"]
	
	positionSizing = 1/len(assetsToTrade)
	
	iteratorPos = 0 	# Tracks position in list of symbols to download 
	assetListLen = len(assetsToTrade)


	returned_data = api.get_barset(assetsToTrade,barTimeframe,limit=100)
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
			continue
		SMA50 = talib.SMA(closeList,50)[-1]
		SMA3 = talib.SMA(closeList,3)[-1]

		# Calculates the trading signals
		if SMA20 > SMA50:
			if SMA3 > 0:
				try:
					openPosition = api.get_position(symbol)
				except:
					price = si.get_live_price(symbol)
					cashBalance = api.get_account().cash
					targetPositionSize = float(str(cashBalance)) / (price / positionSizing) # Calculates required position size
	
					returned = api.submit_order(symbol,int(targetPositionSize),"buy","market","gtc") # Market order to open position
					print(returned)
		iteratorPos += 1

	print("Waiting for 0 mins! Be patient")
	time.sleep(60 * 0)