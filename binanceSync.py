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


CSV_HEADER = "Date,Time,BnAsk,BnBid,0.42% Ref\r\n"

btcBook = {"as": [["blank", "blank"],["blank", "blank"],["blank", "blank"],["blank", "blank"],["blank", "blank"],["blank", "blank"],["blank", "blank"],["blank", "blank"],["blank", "blank"],["blank", "blank"] ],"bs": [["blank", "blank"],["blank", "blank"],["blank", "blank"],["blank", "blank"],["blank", "blank"],["blank", "blank"],["blank", "blank"],["blank", "blank"],["blank", "blank"],["blank", "blank"] ]}

progStart = time.time()
fetchTime = localtime(0)
iterTime = 0


def wsGetPayload(ws, recAddr, recSubInfo): #wsGetPayload(kws, "wss://ws.kraken.com/", '{"event":"subscribe", "subscription":{"depth":10,"name":"book"}, "pair":["XBT/USD"]}')
    reconnectFlag = False
    while True:
        try:
            if reconnectFlag: #something is wrong, start connection from scratch
                sleep(15)
                print(bcolors.WARNING + 'Reconnecting...' + bcolors.ENDC)
                ws.close
                ws = create_connection(recAddr) #"wss://ws.kraken.com/"
                ws.send(recSubInfo) #'{"event":"subscribe", "subscription":{"depth":10,"name":"book"}, "pair":["XBT/USD"]}'
                print(bcolors.WARNING + 'Done' + bcolors.ENDC)
            return ws.recv(), ws
            # break
        except websocket._exceptions.WebSocketConnectionClosedException:
            # traceback.print_exc()
            print(bcolors.FAIL + 'Error: WS closed' + bcolors.ENDC)
            reconnectFlag = True
            # exit()
        except websocket._exceptions.WebSocketProtocolException:
            print(bcolors.FAIL + 'Error: protocol exception' + bcolors.ENDC)
            reconnectFlag = True
        except TimeoutError:
            # traceback.print_exc()
            print(bcolors.FAIL + 'Error: Timeout' + bcolors.ENDC)
            reconnectFlag = True
            # exit()
        except websocket._exceptions.WebSocketAddressException:
            print(bcolors.FAIL + 'Error: WS Address Exception (usually means no internet)' + bcolors.ENDC)
            reconnectFlag = True
        except KeyboardInterrupt:
            traceback.print_exc()
            exit()
        except:
            traceback.print_exc()
            print(bcolors.FAIL + 'Error: Unknown WS exception' + bcolors.ENDC)
            exit()

def logOrderBook(fetchTime, iterTime, btcBook): #btcBook is a dictionary of the top ten bids/asks

    #find nearest $0.03BTC (about $1100 in feb 2021)
    for askInd in range(10):
        total = 0
        for i in range(askInd+1):
            total = total + float(btcBook['as'][i][1])
        if total >= 0.03:
            break
        total = None
    for bidInd in range(10):
        total = 0
        for i in range(bidInd+1):
            total = total + float(btcBook['bs'][i][1])
        if total >= 0.03:
            break
        total = None
    if askInd is None or bidInd is None:
        print(bcolors.FAIL + 'Error: Ask or bid volume not found' + bcolors.ENDC)
        print('askInd: ' + str(askInd) + ' bidInd: ' + str(bidInd))
        print(recData)
        print(type(recData))
        print(btcBook)
        print(bcolors.FAIL + 'End of Ask or bid volume not found' + bcolors.ENDC)
        # raise ValueError('Ask or bid volume not found')
    else:
        #generate additional columns
        feeRef = float(btcBook['as'][askInd][0])*100.42/100
        #log values
        if not os.path.exists('datedCSV/' + strftime("%Y-%m-%d", fetchTime)):
            os.mkdir('datedCSV/' + strftime("%Y-%m-%d", fetchTime))
        f = open('datedCSV/' + strftime("%Y-%m-%d", fetchTime) + '/BTC_BN_' + strftime("%H", fetchTime) + '.csv', "a+")
        f.write(strftime("%Y-%m-%d %H:%M:%S", fetchTime) + " , " + str(iterTime) + " , ")
        f.write(btcBook['as'][askInd][0] + " , " + btcBook['bs'][bidInd][0] + " , " + str(feeRef) + "\r\n")
        f.close()





#Main code:-------------------------------------------------------------------------------------------------------------------------------
# Connect to WebSocket API and subscribe to trade feed
bws = create_connection("wss://stream.binance.com:9443/ws/btcusdt@depth10@1000ms")
bws.send('{"method": "SUBSCRIBE","params":["btcusdt@depth10@100ms"],"id": 1}')
# bws.send('{"method": "SUBSCRIBE","params":["btcusdt@aggTrade","btcusdt@depth"],"id": 1}')

while True:
    #start websocket handling
    # payload = bws.recv()
    # recData = json.loads(payload)
    payload, bws = wsGetPayload(bws, "wss://stream.binance.com:9443/ws/btcusdt@depth10@1000ms", '{"method": "SUBSCRIBE","params":["btcusdt@depth10@100ms"],"id": 1}')
    # print(bcolors.OKGREEN + 'succesful call of get payload' + bcolors.ENDC)
    #load data (had recent bug)
    try:
        recData = json.loads(payload)
    except KeyboardInterrupt:
        traceback.print_exc()
        exit()
    except:
        print(bcolors.FAIL + 'Error: Unknown json loads exception' + bcolors.ENDC)
        print(bcolors.OKBLUE + 'payload:' + bcolors.ENDC)
        print(payload)
        print(bcolors.OKBLUE + 'type:' + bcolors.ENDC)
        print(type(payload))
        print(bcolors.OKBLUE + 'traceback:' + bcolors.ENDC)
        traceback.print_exc()
        exit()

    #start logging
    fetchTime = localtime()
    iterTime = time.time()
    if True: #int(strftime("%M", fetchTime)) % 10 == 0: #minute is a multiple of 10
        #create folder and header
        if not os.path.exists('datedCSV/' + strftime("%Y-%m-%d", fetchTime)):
            os.mkdir('datedCSV/' + strftime("%Y-%m-%d", fetchTime))
        if not os.path.exists('datedCSV/' + strftime("%Y-%m-%d", fetchTime) + '/BTC_BN_' + strftime("%H", fetchTime) + '.csv'): #file does not yet exist
            f = open('datedCSV/' + strftime("%Y-%m-%d", fetchTime) + '/BTC_BN_' + strftime("%H", fetchTime) + '.csv', "a+")
            f.write(CSV_HEADER)
            f.close()

    #analyze received data
    if len(recData) == 2:
        if 'result' in recData and 'id' in recData:
            if recData['result'] == None and recData['id'] == 1:
                print(bcolors.OKBLUE + 'Binance Status: Connected' + bcolors.ENDC)
            else:
                print(bcolors.FAIL + 'Error: Unexpected content in subscription response, data below' + bcolors.ENDC)
                print(recData)
                print(type(recData))
                raise ValueError('Unexpected content in subscription response')
        else:
            print(bcolors.FAIL + 'Error: Unexpected data in subscription response, data below' + bcolors.ENDC)
            print(recData)
            print(type(recData))
            raise ValueError('Unexpected data in subscription response')
    elif len(recData) == 3:
        if 'asks' in recData and 'bids' in recData and 'lastUpdateId' in recData:
            if len(recData['asks'])==10 and len(recData['bids'])==10:
                #update the book with snapshot
                for i in range(10):
                    btcBook['as'][i] = recData['asks'][i]
                    btcBook['bs'][i] = recData['bids'][i]
                #log results
                logOrderBook(fetchTime, iterTime, btcBook)
            else:
                print(bcolors.FAIL + 'Error: Unexpected number of bids or asks in partial book update, data below' + bcolors.ENDC)
                print(recData)
                print(type(recData))
                print('# of asks: ' + str(len(recData['asks'])) + '    # of bids: ' + str(len(recData['bids'])))
                raise ValueError('Unexpected number of bids or asks in partial book update')
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
