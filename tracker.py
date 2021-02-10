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
# lastFinexFetch = time.time()


btcBook = {"as": [[ "blank", "blank", "blank" ],[ "blank", "blank", "blank" ],[ "blank", "blank", "blank" ],[ "blank", "blank", "blank" ],[ "blank", "blank", "blank" ],[ "blank", "blank", "blank" ],[ "blank", "blank", "blank" ],[ "blank", "blank", "blank" ],[ "blank", "blank", "blank" ],[ "blank", "blank", "blank" ] ],"bs": [[ "blank", "blank", "blank" ],[ "blank", "blank", "blank" ],[ "blank", "blank", "blank" ],[ "blank", "blank", "blank" ],[ "blank", "blank", "blank" ],[ "blank", "blank", "blank" ],[ "blank", "blank", "blank" ],[ "blank", "blank", "blank" ],[ "blank", "blank", "blank" ],[ "blank", "blank", "blank" ] ]}
btcCRC = 0




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
        f = open('datedCSV/' + strftime("%Y-%m-%d", fetchTime) + '/BTC_' + strftime("%H", fetchTime) + '.csv', "a+")
        f.write(strftime("%Y-%m-%d %H:%M:%S", fetchTime) + " , " + str(iterTime) + " , ")
        f.write(btcBook['as'][askInd][0] + " , " + btcBook['bs'][bidInd][0] + " , " + str(feeRef) + "\r\n")
        f.close()

#Main code:-------------------------------------------------------------------------------------------------------------------------------
# Connect to WebSocket API and subscribe to trade feed for XBT/USD and XRP/USD
ws = create_connection("wss://ws.kraken.com/")
# ws.send('{"event":"subscribe", "subscription":{"name":"trade"}, "pair":["XBT/USD","LINK/USD"]}')
# ws.send('{"event":"subscribe", "subscription":{"name":"trade"}, "pair":["XBT/USD"]}')
ws.send('{"event":"subscribe", "subscription":{"depth":10,"name":"book"}, "pair":["XBT/USD"]}')
newSnapshot = False
wrongCRCcount = 0

# Infinite loop waiting for WebSocket data
while True:
    #start logging
    fetchTime = localtime()
    iterTime = time.time()
    if True: #int(strftime("%M", fetchTime)) % 10 == 0: #minute is a multiple of 10
        #create folder and header
        if not os.path.exists('datedCSV/' + strftime("%Y-%m-%d", fetchTime)):
            os.mkdir('datedCSV/' + strftime("%Y-%m-%d", fetchTime))
        if not os.path.exists('datedCSV/' + strftime("%Y-%m-%d", fetchTime) + '/BTC_' + strftime("%H", fetchTime) + '.csv'): #file does not yet exist
            f = open('datedCSV/' + strftime("%Y-%m-%d", fetchTime) + '/BTC_' + strftime("%H", fetchTime) + '.csv', "a+")
            f.write(CSV_HEADER)
            f.close()
    #start websocket handling
    # payload = ws.recv()
    reconnectFlag = False
    while True:
        try:
            if reconnectFlag:
                sleep(15)
                print(bcolors.WARNING + 'Reconnecting...' + bcolors.ENDC)
                ws.close
                ws = create_connection("wss://ws.kraken.com/")
                ws.send('{"event":"subscribe", "subscription":{"depth":10,"name":"book"}, "pair":["XBT/USD"]}')
                print(bcolors.WARNING + 'Done' + bcolors.ENDC)
            payload = ws.recv()
            break
        except websocket._exceptions.WebSocketConnectionClosedException:
            traceback.print_exc()
            print(bcolors.FAIL + 'Error: WS closed' + bcolors.ENDC)
            exit()
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
    recData = json.loads(payload)
    if type(recData) is dict:
        if not "event" in recData:
            print(bcolors.FAIL + 'Key error, data below' + bcolors.ENDC)
            print(recData)
            print(type(recData))
            raise ValueError('Key error')
        if recData['event']=='heartbeat':
            pass
        elif recData['event']=='error':
            print(bcolors.FAIL + 'In-message error, data below' + bcolors.ENDC)
            print(recData)
            print(type(recData))
            raise ValueError('In-message error')
        elif recData['event']=='systemStatus':
            print(bcolors.OKBLUE + recData['event'] + bcolors.ENDC + ' Status: ' + recData['status'] + ', Version: ' + recData['version'] + ', ID:' + str(recData['connectionID']))
        elif recData['event']=='subscriptionStatus':
            if newSnapshot == False:
                #print(bcolors.OKBLUE + recData['event'] + bcolors.ENDC + ' Status: ' + recData['status'] + ', channelName: ' + recData['channelName'] + ', pair:' + recData['pair'])
                btcCH = recData['channelID']
            else:
                if 'event' in recData and 'status' in recData and 'channelName' in recData and 'pair' in recData:
                    pass
                    # print(bcolors.OKBLUE + recData['event'] + bcolors.ENDC + ' Status: ' + recData['status'] + ', channelName: ' + recData['channelName'] + ', pair:' + recData['pair'])
                else:
                    print(recData)
                newSnapshot = False
                ws.send('{"event":"subscribe", "subscription":{"depth":10,"name":"book"}, "pair":["XBT/USD"]}')
                #print(bcolors.WARNING + 'resubscribed - ' + strftime("%Y-%m-%d %H:%M:%S", localtime()) + bcolors.ENDC)
        else:
            print(bcolors.FAIL + 'Error: Unknown event, data below' + bcolors.ENDC)
            print(recData)
            print(type(recData))
            raise ValueError('Unknown event')
    elif type(recData) is list:
        if recData[0]==btcCH:
            #book analysis here:
            recDict = recData[1]
            if "as" in recDict and 'bs' in recDict:
                #update the blank book with snapshot
                for i in range(10):
                    btcBook['as'][i] = recDict['as'][i]
                    btcBook['bs'][i] = recDict['bs'][i]
            elif "a" in recDict or 'b' in recDict:
                # #display old dict and new value
                # print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
                # for i in range(len(btcBook['as'])):
                #     print(btcBook['as'][i])
                # print('#######################')
                # for i in range(len(btcBook['bs'])):
                #     print(btcBook['bs'][i])
                # print('*****INFO*****')
                # print(recDict)
                #update the populated book with new values:
                if 'c' in recDict:
                    recCRC = int(recDict['c'])
                else:
                    #print(bcolors.WARNING + 'CRC not in book update' + bcolors.ENDC)
                    recCRC = -1
                if 'a' in recDict:
                    #update asks in local copy
                    for i in range(len(recDict['a'])):
                        #find index for data insertion
                        level = recDict['a'][i][0]
                        levelInd = -1
                        delElement = False
                        insElement = False
                        #check for int levels
                        for j in range(len(btcBook['as'])):
                            if level == btcBook['as'][j][0]:
                                levelInd = j
                                delElement = float(recDict['a'][i][1]) == 0
                        if levelInd<0:
                            for j in reversed(range(len(btcBook['as']))):
                                if level < btcBook['as'][j][0]:
                                    insElement = True
                                    levelInd = j
                            if insElement == False:
                                levelInd = 9
                        # print(bcolors.OKBLUE + 'levelInd: ' + str(levelInd) + bcolors.ENDC)
                        # print(bcolors.OKBLUE + 'delElement: ' + str(delElement) + bcolors.ENDC)
                        # print(bcolors.OKBLUE + 'insElement: ' + str(insElement) + bcolors.ENDC)
                        # print('----')
                        #three cases, element replace, element delete, element(s) shift
                        if levelInd>=0:
                            if delElement==False and insElement==False:
                                #element replace
                                btcBook['as'][levelInd] = recDict['a'][i][0:3]
                            elif delElement==True:
                                #element delete
                                if levelInd<=8:
                                    for j in range(levelInd,9): #only goes up to 8
                                        btcBook['as'][j] = btcBook['as'][j+1]
                                #btcBook['as'][9][0] = '60000' #really weird, for some reason this was updating both [8] and [9] only when indexing 8 or 9, like they were connected
                                btcBook['as'][9] = ['2000000000', '0.0', '0']
                            elif insElement==True:
                                #element(s) shift
                                if levelInd<=8:
                                    for j in reversed(range(levelInd+1,10)):
                                        btcBook['as'][j] = btcBook['as'][j-1]
                                btcBook['as'][levelInd] = recDict['a'][i][0:3]
                                # print('inserted: _-_-_-_-_-_-_-_-_-_-_-_-')
                                # for i in range(len(btcBook['as'])):
                                #     print(btcBook['as'][i])
                        else:
                            print(bcolors.FAIL + 'Error: Ask level index not found, data below' + bcolors.ENDC)
                            print(recData)
                            print(type(recData))
                            raise ValueError('Ask level index not found')
                else: #'b'
                    #update bids in local copy
                    for i in range(len(recDict['b'])):
                        #find index for data insertion
                        level = recDict['b'][i][0]
                        levelInd = -1
                        delElement = False
                        insElement = False
                        #check for int levels
                        for j in range(len(btcBook['bs'])):
                            if level == btcBook['bs'][j][0]:
                                levelInd = j
                                delElement = float(recDict['b'][i][1]) == 0
                        if levelInd<0:
                            for j in reversed(range(len(btcBook['bs']))):
                                if level > btcBook['bs'][j][0]:
                                    insElement = True
                                    levelInd = j
                            if insElement == False:
                                levelInd = 9
                        # print(bcolors.OKBLUE + 'BlevelInd: ' + str(levelInd) + bcolors.ENDC)
                        # print(bcolors.OKBLUE + 'BdelElement: ' + str(delElement) + bcolors.ENDC)
                        # print(bcolors.OKBLUE + 'BinsElement: ' + str(insElement) + bcolors.ENDC)
                        # print('----')
                        #three cases, element replace, element delete, element(s) shift
                        if levelInd>=0:
                            if delElement==False and insElement==False:
                                #element replace
                                btcBook['bs'][levelInd] = recDict['b'][i][0:3]
                            elif delElement==True:
                                #element delete
                                if levelInd<=8:
                                    for j in range(levelInd,9): #only goes up to 8
                                        btcBook['bs'][j] = btcBook['bs'][j+1]
                                btcBook['bs'][9] = ['0', '0.0', '0']
                            elif insElement==True:
                                #element(s) shift
                                if levelInd<=8:
                                    for j in reversed(range(levelInd+1,10)):
                                        btcBook['bs'][j] = btcBook['bs'][j-1]
                                btcBook['bs'][levelInd] = recDict['b'][i][0:3]
                                # print('inserted: _-_-_-_-_-_-_-_-_-_-_-_-')
                                # for i in range(len(btcBook['bs'])):
                                #     print(btcBook['bs'][i])
                        else:
                            print(bcolors.FAIL + 'Error: Bid level index not found, data below' + bcolors.ENDC)
                            print(recData)
                            print(type(recData))
                            raise ValueError('Bid level index not found')
                #check CRC
                if recCRC == -1:
                    pass
                    # print(bcolors.WARNING + 'CRC unable to be checked, not in book update' + bcolors.ENDC)
                else:
                    crcInput = ''
                    for i in range(len(btcBook['as'])):
                        addOnStr1 = btcBook['as'][i][0].replace('.', '').lstrip('0')
                        addOnStr2 = btcBook['as'][i][1].replace('.', '').lstrip('0')
                        crcInput = crcInput + addOnStr1 + addOnStr2
                    for i in range(len(btcBook['bs'])):
                        addOnStr1 = btcBook['bs'][i][0].replace('.', '').lstrip('0')
                        addOnStr2 = btcBook['bs'][i][1].replace('.', '').lstrip('0')
                        crcInput = crcInput + addOnStr1 + addOnStr2
                    crcOutput = 0
                    for i in range(int(len(crcInput))):
                        crcOutput = zlib.crc32(bytes(str(crcInput[i]), 'utf-8'), crcOutput)
                    if recCRC == crcOutput:
                        #correct CRC:
                        #file handling
                        if wrongCRCcount:
                            #print(bcolors.OKGREEN + 'Correct CRC after ' + str(wrongCRCcount) + 'updates' + bcolors.ENDC)
                            wrongCRCcount = 0
                        logOrderBook(fetchTime, iterTime, btcBook)
                    else:
                        #incorrect CRC
                        if newSnapshot == False: #(if the plan is not to resubscribe)
                            if wrongCRCcount >= 8:
                                #need to resubscribe
                                newSnapshot = True
                                wrongCRCcount = 0
                                ws.send('{"event":"unsubscribe", "subscription":{"depth":10,"name":"book"}, "pair":["XBT/USD"]}')
                                # print(bcolors.WARNING + 'Incorrect CRC, resubscribing' + strftime("%Y-%m-%d %H:%M:%S", localtime()) + bcolors.ENDC)
                            else:
                                wrongCRCcount = wrongCRCcount + 1
                                if wrongCRCcount%50==0:
                                    pass#print(bcolors.WARNING + '\tIncorrect CRC count=' + str(wrongCRCcount) + bcolors.ENDC)
                        # print(bcolors.FAIL + 'Error: Incorrect CRC, data below' + bcolors.ENDC)
                        # print(recData)
                        # print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
                        # for i in range(len(btcBook['as'])):
                        #     print(btcBook['as'][i])
                        # print('#######################')
                        # for i in range(len(btcBook['bs'])):
                        #     print(btcBook['bs'][i])
                        # print('recCRC:  ' + str(recCRC))
                        # print('calcCRC: ' + str(crcOutput))
                        # raise ValueError('Incorrect CRC')
            else:
                print(bcolors.FAIL + 'Error: Unknown book dictionary, data below' + bcolors.ENDC)
                print(recData)
                print(type(recData))
                raise ValueError('Unknown book dictionary')
        else:
            print(bcolors.FAIL + 'Error: Unknown channel, data below' + bcolors.ENDC)
            print(recData)
            print(type(recData))
            raise ValueError('Unknown channel')

    else:
        print(bcolors.FAIL + 'Error: json data type' + bcolors.ENDC)
