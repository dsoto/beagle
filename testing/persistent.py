import twiggy as tw
import time
import sqlite3
import datetime as dt

db_connection = sqlite3.connect('./database.db')
db_cursor = db_connection.cursor()

tw.quickSetup(file='gprs.log')

while 1:
    data_value = 600
    first_response = 'response 200'
    query_string='''insert into logs (time_stamp, value, response) values ('%s', %s, '%s');''' % (dt.datetime.now(), data_value, first_response)
    tw.log.info(query_string)

    db_cursor.execute(query_string)
    db_connection.commit()

    time.sleep(5)
