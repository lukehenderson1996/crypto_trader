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
import signal #only so ctrl_c will go to main thread
#crc calculation
import zlib

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
# lastFinexFetch = time.time()


btcBook = {"as": [[ "blank", "blank", "blank" ],[ "blank", "blank", "blank" ],[ "blank", "blank", "blank" ],[ "blank", "blank", "blank" ],[ "blank", "blank", "blank" ],[ "blank", "blank", "blank" ],[ "blank", "blank", "blank" ],[ "blank", "blank", "blank" ],[ "blank", "blank", "blank" ],[ "blank", "blank", "blank" ] ],"bs": [[ "blank", "blank", "blank" ],[ "blank", "blank", "blank" ],[ "blank", "blank", "blank" ],[ "blank", "blank", "blank" ],[ "blank", "blank", "blank" ],[ "blank", "blank", "blank" ],[ "blank", "blank", "blank" ],[ "blank", "blank", "blank" ],[ "blank", "blank", "blank" ],[ "blank", "blank", "blank" ] ]}
btcCRC = 0

krRecTime = time.time()
startTime = time.time()





def ws_open(ws):
    #one time run code here
    ws.send('{"event":"subscribe", "subscription":{"name":"trade"}, "pair":["XBT/USD","XRP/USD"]}')

def ws_thread(*args):
    ws = create_connection("wss://ws.kraken.com/")
    ws_open(ws)
    for i in range(10):
        payload = ws.recv()
        recTime = time.time()
        print("Kraken thread: %s" % time.time())
    print(bcolors.WARNING + 'closing' + bcolors.ENDC)
    ws.close_async()


#log command line
import subprocess
file_ = open('shell_output.txt', 'w+')
subprocess.run('echo Hello from shell', shell=True, stdout=file_)
file_.close()

# Start a new thread for the WebSocket interface
my_threads = []
krThd = _thread.start_new_thread(ws_thread, ())
my_threads.append(krThd)
mythreads = _thread.enumerate()
print(mythreads)
exit()
# print('hello')
# exit()

# Continue other (non WebSocket) tasks in the main thread
while True:
    time.sleep(1)
    print(bcolors.OKBLUE + "Main thread: %d" % time.time() + bcolors.ENDC)
    if ws_thread.is_alive():
        print('alive')
    else:
        print('he dead')
    for t in range(len(my_threads)):
        print(krThd)
        exit()
        if not t.is_alive():
            # get results from thread
            print(t)
            t.handled = True
    my_threads = [t for t in my_threads if not t.handled]
    print('my threads:')
    print(my_threads)

    # if time.time()-startTime>5:
    #     ws.close()




# #how to catch errors?
# https://www.google.com/search?sxsrf=ALeKk01S7uXMl4TbsAk9XAjscdbiar-b6w%3A1612562146859&ei=4r4dYLLzM5a3tQaT0p7IBg&q=python+exit+on+any+thread+error&oq=python+exit+on+any+thread+error&gs_lcp=CgZwc3ktYWIQAzIICCEQFhAdEB46BwgAEEcQsAM6BAgjECc6BQgAEJECOgsIABCxAxCDARCRAjoFCAAQsQM6BAgAEEM6BwgAELEDEEM6CggAELEDEBQQhwI6CAgAELEDEIMBOgIIADoICAAQsQMQkQI6BwgAEBQQhwI6BggAEBYQHlDWxwVYiu4FYIHvBWgDcAJ4AIABgQGIAa4RkgEEMTkuNpgBAKABAaoBB2d3cy13aXrIAQjAAQE&sclient=psy-ab&ved=0ahUKEwiy7MOP3tPuAhWWW80KHROpB2kQ4dUDCA0&uact=5
#
# https://stackoverflow.com/questions/49663124/cause-python-to-exit-if-any-thread-has-an-exception/49665590









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
