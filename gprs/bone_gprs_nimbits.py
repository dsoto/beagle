import serial
import time
import random
import twiggy as tw
import sqlite3
import datetime as dt

stream_name = 'B_BONE_02'

def pause_and_read_serial():
    time.sleep(1)
    response = s.readlines()
    return response

def post_nimbits_staggered(data_value):

    content = ''
    content += 'secret=01787ade-c6d6-4f9b-8b86-20850af010d9'
    content += '&email=drdrsoto@gmail.com'
    content += '&value=%s' % data_value
    content += '&point=' % stream_name
    content_length = len(content)

    post_string = ''
    post_string += 'POST /service/currentvalue HTTP/1.1\r\n'
    post_string += 'Host: app.nimbits.com\r\n'
    post_string += 'Content-Length: %s\r\n' % content_length
    post_string += 'Content-Type: application/x-www-form-urlencoded\r\n'
    post_string += 'Accept-Encoding: identity\r\n'
    post_string += 'Accept: */*\r\n'
    post_string += 'User-Agent: pysoto\r\n\r\n'
    post_string += content

    # hack to work around possible 128 character limit
    for c in post_string:
        s.write(c)
        time.sleep(0.01)

def is_string_in_response(string, response):
    present = False
    for r in response:
        if string in r:
            present = True
    return present

def initiate_modem():
    tw.log.info('flushing out serial port')
    pause_and_read_serial()

    s.write('AT\r\n')
    response = pause_and_read_serial()
    if is_string_in_response('OK', response):
        tw.log.info('good AT response')
    else:
        tw.log.warning('bad AT response')

    s.write('AT#GPRS=1\r\n')
    response = pause_and_read_serial()
    if is_string_in_response('OK', response):
        tw.log.info('good GPRS response')
    else:
        tw.log.warning('bad GPRS response')

    s.write('AT+CGDCONT=1,"IP","epc.tmobile.com","0.0.0.0",0,0\r\n')
    response = pause_and_read_serial()
    if is_string_in_response('OK', response):
        tw.log.info('good CGDCONT response')
    else:
        tw.log.warning('bad CGDCONT response')

    s.write('AT#SD=2,0,80,"app.nimbits.com"\r\n')
    response = pause_and_read_serial()
    if is_string_in_response('CONNECT', response):
        tw.log.info('good SD response')
    else:
        tw.log.warning('bad SD response')

def read_ain2():
    num_avg = 10
    data_value = 0
    for i in range(num_avg):
        f = open('/sys/devices/platform/tsc/ain2')
        data_value += float(f.read())
        f.close()
    data_value = data_value / num_avg
    return data_value

def write_to_db():
    query_string = 'insert into logs (time_stamp, value, response) values (?,?,?)'
    db_cursor.execute(query_string, (dt.datetime.now(), data_value, first_response))
    db_connection.commit()


s = serial.Serial('/dev/ttyUSB0',
                  baudrate=115200,
                  timeout=1)

db_connection = sqlite3.connect('./database.db')
db_cursor = db_connection.cursor()

tw.quickSetup(file='gprs.log')
tw.log.info('---------------------')
tw.log.info('starting gprs_post.py')
tw.log.info('---------------------')


while (1):
    tw.log.info('-- top of loop --')

    def initiate_modem()

    data_value = read_ain2()

    tw.log.info('data_value = ' + str(data_value))
    post_nimbits_staggered(data_value)

    time.sleep(15) # need extra time for html response

    response = pause_and_read_serial()
    if len(response) > 0:
        first_response = response[0].strip()
    else:
        first_response = 'No Response'

    tw.log.info(first_response)

    write_to_db()

    response = ''.join(response)
    if '200 OK' in response:
        tw.log.info('nimbits POST successful')
    else:
        tw.log.error('nimbits POST unsuccessful')

    s.write('AT#GPRS=0\r\n')
    time.sleep(5)
    response = pause_and_read_serial()
    if is_string_in_response('OK', response):
        tw.log.info('good GPRS off response')
    else:
        tw.log.warning('bad GPRS off response')

    # sleep until next minute
    time.sleep(60)

