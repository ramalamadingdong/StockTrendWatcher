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

start_of_day = True

def awaitMarketOpen():
	isOpen = api.get_clock().is_open
	while(not isOpen):
        start_of_day = False
		clock = api.get_clock()
		openingTime = clock.next_open.replace(tzinfo=datetime.timezone.utc).timestamp()
		currTime = clock.timestamp.replace(tzinfo=datetime.timezone.utc).timestamp()
		timeToOpen = int((openingTime - currTime) / 60)
		print(str(timeToOpen) + " minutes til market open.")
		time.sleep(60)
		isOpen = self.alpaca.get_clock().is_open

i=0
while True:
    awaitMarketOpen()
    if start_of_day:
        print("Sell alll stuff not positive")
        start_of_day = True
    i+=1
    positions = api.list_positions()
    # account = 
    for stock in positions:
        if stock.avg_entry_price > stock.current_price:
            try:
                openPosition = api.get_position(symbol)
                returned = api.submit_order(symbol,openPosition,"sell","market","gtc") # Market order to fully close position
                print(returned)
            except:
                pass

    print("Waiting for 0 mins! Be patient")
    time.sleep(60 * 0)
