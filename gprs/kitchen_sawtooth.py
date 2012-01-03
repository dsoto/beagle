import requests
import json
import random
import time
import twiggy as tw
import serial
import sqlite3
import datetime as dt
import beaglebone as bb

# setup twiggy logging
tw.quickSetup(file='random.log')
tw.log.info('starting post_random.py')

nimbits_stream = "Test_Stream_2"
data_value = 0
# sleep for a minute, send random number to pachube in json format
while 1:
    tw.log.info("--- top of loop ---")

    tw.log.info("data value = " + str(data_value))
    status_code = bb.post_nimbits_http(data_value)

    data_value += 0.1
    time.sleep(60)
