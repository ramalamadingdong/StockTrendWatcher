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

while True:
    
	gainers = si.get_day_gainers()
	gainers.columns = ['SYM', 'Company', 'Current Price', 'Price Change', 'Percentage Change', 'Volume'	, 'Avg Vol', 'Market Cap', '52 Week Range']
	gainers.sort_values("Price Change", axis = 0, ascending = False, inplace = True)

	end = datetime.date.today()
	start = end - datetime.timedelta(days=200)
	stock_watchlist = []
	if not DEBUG_MODE:
		for stock in gainers['SYM']:

		    s_hist_data = si.get_data(stock , start_date = str(start) , end_date = str(end))

		    var = s_hist_data.mean(axis=0, skipna = True)
		    avg = (float(var[0]) + float(var[1]))/2

		    curr_price = si.get_live_price(stock)
		    if (avg < curr_price):
		        stock_watchlist.append(stock)

		assetsToTrade = stock_watchlist
		print("Stock Universe for the day:", assetsToTrade)
	else:
		assetsToTrade = ["SPY","MSFT","AAPL","NFLX"]
	positionSizing = 1/len(assetsToTrade)

	# Tracks position in list of symbols to download
	iteratorPos = 0 
	assetListLen = len(assetsToTrade)

	while iteratorPos < assetListLen:
		symbol = assetsToTrade[iteratorPos]
		returned_data = api.get_barset(symbol,barTimeframe,limit=100)
		timeList = []
		openList = []
		highList = []
		lowList = []
		closeList = []
		volumeList = []

		# Reads, formats and stores the new bars
		#print(returned_data[symbol][3].t)
		for bar in returned_data[symbol]:
			#print(bar)
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
			continue
		SMA50 = talib.SMA(closeList,50)[-1]


		# Calculates the trading signals
		if SMA20 > SMA50:
			try:
				openPosition = api.get_position(symbol)
			except:
				price = si.get_live_price(symbol)
				cashBalance = api.get_account().cash
	#			print(cashBalance.cash)
				targetPositionSize = float(str(cashBalance)) / (price / positionSizing) # Calculates required position size

				returned = api.submit_order(symbol,int(targetPositionSize),"buy","market","gtc") # Market order to open position
				print(returned)

		else:
			# Closes position if SMA20 is below SMA50
			try:
				openPosition = api.get_position(symbol)

				returned = api.submit_order(symbol,openPosition,"sell","market","gtc") # Market order to fully close position
				print(returned)
			except:
				pass
		iteratorPos += 1
	time.sleep(60 * 5) 