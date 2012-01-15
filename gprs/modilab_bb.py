import serial
import time
import random
import twiggy as tw
import sqlite3
import datetime as dt
import requests
import json
import beaglebone as bb

# logging variables
stream_name = 'Modi_Lab'

# modem hardware
s = serial.Serial('/dev/ttyUSB0',
                  baudrate=115200,
                  timeout=1)

# database objects
db_connection = sqlite3.connect('./database.db')
db_cursor = db_connection.cursor()

# set up logging
tw.quickSetup(file='modilab.log')
tw.log.info('---------------------')
tw.log.info('starting modilab_bb.py')
tw.log.info('---------------------')

while (1):
    tw.log.info('-- top of loop --')

    # get sensor reading and timestamp
    data_value = bb.read_ain2()
    time_stamp = dt.datetime.now().isoformat()

    tw.log.info('data_value = ' + str(data_value))

    # post to nimbits over gprs
    bb.initiate_modem_nimbits(s)
    bb.post_nimbits_gprs(data_value, stream_name, s)
    first_response = bb.parse_response(s)
    bb.write_to_db(time_stamp, data_value, first_response, db_cursor, db_connection)

    # turn GPRS off
    s.write('AT#GPRS=0\r\n')
    time.sleep(5)
    response = bb.pause_and_read_serial(s)
    if bb.is_string_in_response('OK', response):
        tw.log.info('good GPRS off response')
    else:
        tw.log.warning('bad GPRS off response')

    # post to rackspace over HTTP
    bb.post_custom_server_http('kitchen', data_value, time_stamp)

    # sleep for a few minutes
    time.sleep(5*60)