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
import time

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


print('start')
for j in range(1,9): #only goes up to 8
    print(j)
