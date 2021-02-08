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
#crc
# import binascii
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




'''
{
"as": [
    [ "0.05005", "0.00000500", "1582905487.684110" ],
    [ "0.05010", "0.00000500", "1582905486.187983" ],
    [ "0.05015", "0.00000500", "1582905484.480241" ],
    [ "0.05020", "0.00000500", "1582905486.645658" ],
    [ "0.05025", "0.00000500", "1582905486.859009" ],
    [ "0.05030", "0.00000500", "1582905488.601486" ],
    [ "0.05035", "0.00000500", "1582905488.357312" ],
    [ "0.05040", "0.00000500", "1582905488.785484" ],
    [ "0.05045", "0.00000500", "1582905485.302661" ],
    [ "0.05050", "0.00000500", "1582905486.157467" ] ],
"bs": [
    [ "0.05000", "0.00000500", "1582905487.439814" ],
    [ "0.04995", "0.00000500", "1582905485.119396" ],
    [ "0.04990", "0.00000500", "1582905486.432052" ],
    [ "0.04980", "0.00000500", "1582905480.609351" ],
    [ "0.04975", "0.00000500", "1582905476.793880" ],
    [ "0.04970", "0.00000500", "1582905486.767461" ],
    [ "0.04965", "0.00000500", "1582905481.767528" ],
    [ "0.04960", "0.00000500", "1582905487.378907" ],
    [ "0.04955", "0.00000500", "1582905483.626664" ],
    [ "0.04950", "0.00000500", "1582905488.509872" ] ]
}
'''

btcBook = {"as": [[ "0.05005", "0.00000500", "1582905487.684110" ],[ "0.05010", "0.00000500", "1582905486.187983" ],[ "0.05015", "0.00000500", "1582905484.480241" ],[ "0.05020", "0.00000500", "1582905486.645658" ],[ "0.05025", "0.00000500", "1582905486.859009" ],[ "0.05030", "0.00000500", "1582905488.601486" ],[ "0.05035", "0.00000500", "1582905488.357312" ],[ "0.05040", "0.00000500", "1582905488.785484" ],[ "0.05045", "0.00000500", "1582905485.302661" ],[ "0.05050", "0.00000500", "1582905486.157467" ] ],"bs": [[ "0.05000", "0.00000500", "1582905487.439814" ],[ "0.04995", "0.00000500", "1582905485.119396" ],[ "0.04990", "0.00000500", "1582905486.432052" ],[ "0.04980", "0.00000500", "1582905480.609351" ],[ "0.04975", "0.00000500", "1582905476.793880" ],[ "0.04970", "0.00000500", "1582905486.767461" ],[ "0.04965", "0.00000500", "1582905481.767528" ],[ "0.04960", "0.00000500", "1582905487.378907" ],[ "0.04955", "0.00000500", "1582905483.626664" ],[ "0.04950", "0.00000500", "1582905488.509872" ] ]}



crcInput = ''
for i in range(len(btcBook['as'])):
    addOnStr1 = btcBook['as'][i][0].replace('.', '').lstrip('0')
    addOnStr2 = btcBook['as'][i][1].replace('.', '').lstrip('0')
    crcInput = crcInput + addOnStr1 + addOnStr2
for i in range(len(btcBook['bs'])):
    addOnStr1 = btcBook['bs'][i][0].replace('.', '').lstrip('0')
    addOnStr2 = btcBook['bs'][i][1].replace('.', '').lstrip('0')
    crcInput = crcInput + addOnStr1 + addOnStr2

# crcInputConverted = int(crcInput).to_bytes(2, byteorder='big')
# print(crcInputConverted)
# crcOutput = binascii.crc32(bytes(int(crcInput)))

# testVar = zlib.crc32(bytes(int('2782387234')))
# print(testVar)


# print('length: ')
# print(len(crcInput))
# binList = []
# binList.append(bytes(int(crcInput[0])))
# print(binList)

# print(bytes([8]))
# exit()

# testString = '9'
# crcOutput = 0
# for i in range(len(testString)):
#     crcOutput = zlib.crc32(bytes([int(testString[i])]), crcOutput)


crcOutput = 0
for i in range(int(len(crcInput))):
    crcOutput = zlib.crc32(bytes(str(crcInput[i]), 'utf-8'), crcOutput)

print('final check:')

print("50055005010500501550050205005025500503050050355005040500504550050505005000500499550049905004980500497550049705004965500496050049555004950500")
print(crcInput)
print("974947235")
print(crcOutput)
