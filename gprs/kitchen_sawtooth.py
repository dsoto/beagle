import requests
import json
import random
import time
import twiggy as tw
import serial
import sqlite3
import datetime as dt
import beaglebone as bb

# database objects
db_connection = sqlite3.connect('./sawtooth.db')
db_cursor = db_connection.cursor()

# setup twiggy logging
tw.quickSetup(file='sawtooth.log')
tw.log.info('starting post_random.py')

nimbits_stream = "Test_Stream_2"
data_value = 0

# sleep for a minute, send random number to pachube in json format
while 1:
    tw.log.info("--- top of loop ---")
    time_stamp = dt.datetime.now()

    tw.log.info("data value = " + str(data_value))

    status_code = bb.post_nimbits_http(nimbits_stream, data_value)

    bb.write_to_db(time_stamp, data_value, status_code, db_cursor, db_connection)

    data_value += 0.1
    time.sleep(60)
