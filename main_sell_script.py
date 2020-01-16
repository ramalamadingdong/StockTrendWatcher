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
while i < 1:
    i+=1
    positions = api.list_positions()

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
