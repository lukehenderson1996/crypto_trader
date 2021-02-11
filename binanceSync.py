#Luke Henderson
#Version 0.0
#all these are from auto_trader.py##############################################
import requests, json
import time
from time import sleep, localtime, strftime
import sys, traceback
import os
from parse import * #pip install parse (or pip3 install parse)
#from https://www.jokecamp.com/blog/examples-of-creating-base64-hashes-using-hmac-sha256-in-different-languages/#python3
import hashlib
import hmac
import base64
# #for logging
# from logger_auto_trader import *
#from kraken website:###########################################################
#Sync
from websocket import create_connection #pip3 install websocket-client
#Async
import websocket
import _thread
#crc calculation
import zlib
#error handling
import traceback

#make text look unique
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


CSV_HEADER = "Date,Time,KrAsk,KrBid,0.42% Ref\r\n"

progStart = time.time()










#Main code:-------------------------------------------------------------------------------------------------------------------------------
# Connect to WebSocket API and subscribe to trade feed
ws = create_connection("wss://stream.binance.com:9443/ws/btcusdt@depth10@1000ms")
ws.send('{"method": "SUBSCRIBE","params":["btcusdt@depth10@100ms"],"id": 1}')
# ws.send('{"method": "SUBSCRIBE","params":["btcusdt@aggTrade","btcusdt@depth"],"id": 1}')

while True:
    payload = ws.recv()
    recData = json.loads(payload)
    if len(recData) == 2:
        if 'result' in recData and 'id' in recData:
            print(recData)
        else:
            print(bcolors.FAIL + 'Error: Unexpected data in subscription response, data below' + bcolors.ENDC)
            print(recData)
            print(type(recData))
            raise ValueError('Unexpected data in subscription response')
    elif len(recData) == 3:
        if 'asks' in recData and 'bids' in recData and 'lastUpdateId' in recData:
            pass
            #print('data here')
        else:
            print(bcolors.FAIL + 'Error: Unexpected data in partial book update, data below' + bcolors.ENDC)
            print(recData)
            print(type(recData))
            raise ValueError('Unexpected data in partial book update')
    else:
        print(bcolors.FAIL + 'Error: Unexpected dictionary length, data below' + bcolors.ENDC)
        print(recData)
        print(type(recData))
        raise ValueError('Unexpected dictionary length')







































#end
