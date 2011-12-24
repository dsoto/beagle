import requests
import json
import random
import time
import twiggy as tw
import serial
import sqlite3
import datetime as dt

# set up database connection
db_connection = sqlite3.connect('./random.db')
db_cursor = db_connection.cursor()

# setup twiggy logging
tw.quickSetup(file='random.log')
tw.log.info('starting post_random.py')


def post_nimbits(value):
    nimbits_data = {"email":"drdrsoto@gmail.com",
                    "secret":"01787ade-c6d6-4f9b-8b86-20850af010d9",
                    "point":"603_Test_Stream",
                    "value":value}

    try:
        r = requests.post("http://app.nimbits.com/service/currentvalue", data=nimbits_data)
    except:
        tw.log.trace('error').error('bad post to nimbits')
    log_message = 'nimbits response value = ' + str(r.status_code)
    if r.status_code == 200:
        tw.log.info(log_message)
    else:
        tw.log.error(log_message)
    return r.status_code


# sleep for a minute, send random number to pachube in json format
while 1:
    tw.log.info("top of loop")

    data_value = 20 + random.random() * 10
    tw.log.info("data value = " + str(data_value))
    status_code = post_nimbits(data_value)

    # place date, value, and http result code in database
    query_string=  '''insert into posts (time_stamp, value, response)
                      values ('%s', %s, %s)''' % (dt.datetime.now(), data_value, status_code)
    db_cursor.execute(query_string)
    db_connection.commit()

    time.sleep(60)
