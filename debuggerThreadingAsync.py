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
import threading
# import signal #only so ctrl_c will go to main thread
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


CSV_HEADER = "Date,Time,3A,3V,2A,2V,1A,1V,1B,1V,2B,2V,3B,3V\r\n"

progStart = time.time()


btcBook = {"as": [[ "blank", "blank", "blank" ],[ "blank", "blank", "blank" ],[ "blank", "blank", "blank" ],[ "blank", "blank", "blank" ],[ "blank", "blank", "blank" ],[ "blank", "blank", "blank" ],[ "blank", "blank", "blank" ],[ "blank", "blank", "blank" ],[ "blank", "blank", "blank" ],[ "blank", "blank", "blank" ] ],"bs": [[ "blank", "blank", "blank" ],[ "blank", "blank", "blank" ],[ "blank", "blank", "blank" ],[ "blank", "blank", "blank" ],[ "blank", "blank", "blank" ],[ "blank", "blank", "blank" ],[ "blank", "blank", "blank" ],[ "blank", "blank", "blank" ],[ "blank", "blank", "blank" ],[ "blank", "blank", "blank" ] ]}
btcCRC = 0

krRecTime = time.time()
startTime = time.time()

closeKrakenWS = False
closeKrakenTHD = False



def kws_thread(kws):
    while True:
        try:
            if time.time()-startTime>3:
                pass
            else:
                payload = kws.recv()
        except websocket._exceptions.WebSocketConnectionClosedException:
            traceback.print_exc()
            print(bcolors.FAIL + 'Error: WS closed' + bcolors.ENDC)
            exit()
        except TimeoutError:
            traceback.print_exc()
            print(bcolors.FAIL + 'Error: Timeout' + bcolors.ENDC)
            exit()
        except KeyboardInterrupt:
            traceback.print_exc()
            exit()
        except:
            traceback.print_exc()
            print(bcolors.FAIL + 'Error: Unknown WS exception' + bcolors.ENDC)
            exit()
        recTime = time.time()
        # print("Kraken thread: %s" % time.time())
        #print what event is
        # recData = json.loads(payload)
        # if type(recData) is dict:
        #     if recData['event']=='heartbeat':
        #         pass
        #     elif recData['event']=='error':
        #         print(bcolors.FAIL + 'In-message error, data below' + bcolors.ENDC)
        #         print(recData)
        #         print(type(recData))
        #     elif recData['event']=='systemStatus':
        #         print(bcolors.OKBLUE + recData['event'] + bcolors.ENDC + ' Status: ' + recData['status'] + ', Version: ' + recData['version'] + ', ID:' + str(recData['connectionID']))
        #     elif recData['event']=='subscriptionStatus':
        #         print(bcolors.OKBLUE + recData['event'] + bcolors.ENDC + ' Status: ' + recData['status'] + ', channelName: ' + recData['channelName'] + ', pair:' + recData['pair'])
        if closeKrakenWS:
            kws.close()
            print(bcolors.WARNING + 'closing' + bcolors.ENDC)
            break



# Start a new thread for the WebSocket interface
kws = create_connection("wss://ws.kraken.com/")
kws.send('{"event":"subscribe", "subscription":{"name":"trade"}, "pair":["XBT/USD","XRP/USD"]}')
krThd = threading.Thread(target=kws_thread,args=(kws,))
krThd.daemon = True
krThd.start()
myThreads = threading.enumerate()
print(myThreads)


# Continue other (non WebSocket) tasks in the main thread
while True:
    time.sleep(1)
    print(bcolors.OKBLUE + "Main thread: %d" % time.time() + bcolors.ENDC)
    if krThd.is_alive():
        print('alive')
    else:
        #you can't restart it here
        print(bcolors.WARNING + 'Restarting kraken thread' + bcolors.ENDC)
        kws.close()
        kws = create_connection("wss://ws.kraken.com/")
        kws.send('{"event":"subscribe", "subscription":{"name":"trade"}, "pair":["XBT/USD","XRP/USD"]}')
        # krThd = threading.Thread(target=kws_thread,args=(kws,))
        myThreads = threading.enumerate()
        print(myThreads)
        # krThd.daemon = True
        myThreads = threading.enumerate()
        print(myThreads)
        krThd.start()
    if time.time()-startTime>10:
        # kws.close()
        #example code to be incorporated within the thread somehow, but how long does recv() take to timeout?
        #https://stackoverflow.com/questions/2719017/how-to-set-timeout-on-pythons-socket-recv-method
        print(bcolors.OKGREEN + ' closing with no internet')
        kws.close()
        kws = create_connection("wss://ws.kraken.com/") #if no internet, will do this: websocket._exceptions.WebSocketAddressException
        print('done' + bcolors.ENDC)
        # closeKrakenWS = True
    #if it really won't listen (internet is down)
        # sock.shutdown(socket.SHUT_RDWR)











# #from https://stackoverflow.com/questions/29145442/threaded-non-blocking-websocket-client
# #can close when you want
#
# import websocket
# import threading
# from time import sleep
#
# def on_message(ws, message):
#     print message
#
# def on_close(ws):
#     print "### closed ###"
#
# if __name__ == "__main__":
#     websocket.enableTrace(True)
#     ws = websocket.WebSocketApp("ws://echo.websocket.org/", on_message = on_message, on_close = on_close)
#     wst = threading.Thread(target=ws.run_forever)
#     wst.daemon = True
#     wst.start()
#
#     conn_timeout = 5
#     while not ws.sock.connected and conn_timeout:
#         sleep(1)
#         conn_timeout -= 1
#
#     msg_counter = 0
#     while ws.sock.connected:
#         ws.send('Hello world %d'%msg_counter)
#         sleep(1)
#         msg_counter += 1
















#end
