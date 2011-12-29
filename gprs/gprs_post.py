import serial
import time
import random
import twiggy as tw
import sqlite3
import datetime as dt

def pause_and_read_serial():
    time.sleep(1)
    response = s.readlines()
    return response

def post_nimbits_staggered(data_value):

    content = ''
    content += 'secret=01787ade-c6d6-4f9b-8b86-20850af010d9'
    content += '&email=drdrsoto@gmail.com'
    content += '&value=%s&point=603_Test_Stream' % data_value
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

#print 'opening serial port'
s = serial.Serial('/dev/ttyUSB0',
                  baudrate=115200,
                  timeout=1)

db_connection = sqlite3.connect('./database.db')
db_cursor = db_connection.cursor()

tw.quickSetup(file='gprs.log')
tw.log.info('---------------------')
tw.log.info('starting gprs_post.py')
tw.log.info('---------------------')

def is_string_in_response(string, response):
    present = False
    for r in response:
        if string in r:
            present = True
    return present

#data_value = 20.0

while (1):
    tw.log.info('-- top of loop --')

    tw.log.info('flushing out serial port')
    pause_and_read_serial()

    #print 'testing using AT command'
    s.write('AT\r\n')
    response = pause_and_read_serial()
    if is_string_in_response('OK', response):
        tw.log.info('good AT response')
    else:
        tw.log.warning('bad AT response')

    #print 'activating GPRS'
    s.write('AT#GPRS=1\r\n')
    response = pause_and_read_serial()
    if is_string_in_response('OK', response):
        tw.log.info('good GPRS response')
    else:
        tw.log.warning('bad GPRS response')

    #print 'activating context'
    s.write('AT+CGDCONT=1,"IP","epc.tmobile.com","0.0.0.0",0,0\r\n')
    response = pause_and_read_serial()
    if is_string_in_response('OK', response):
        tw.log.info('good CGDCONT response')
    else:
        tw.log.warning('bad CGDCONT response')

    #print 'socket dial'
    s.write('AT#SD=2,0,80,"app.nimbits.com"\r\n')
    response = pause_and_read_serial()
    if is_string_in_response('CONNECT', response):
        tw.log.info('good SD response')
    else:
        tw.log.warning('bad SD response')

    #print 'posting to nimbits'

    f = open('/sys/devices/platform/tsc/ain2')
    data_value = f.read()
    f.close()
    tw.log.info('data_value = ' + str(data_value))
    post_nimbits_staggered(data_value)
    #print 'sleeping'
    time.sleep(15) # need extra time for html response
    #print 'post response'

    response = pause_and_read_serial()
    if len(response) > 0:
        first_response = response[0].strip()
    else:
        first_response = 'No Response'

    #first_response = 'HTTP/1.1 200 OK'

    tw.log.info(first_response)

    query_string='''insert into logs (time_stamp, value, response) values (?,?,?);'''
    tw.log.info(query_string)

    db_cursor.execute(query_string, (dt.datetime.now(), data_value, first_response))
    #db_cursor.execute("insert into logs (time_stamp, value, response) values ('?', ?, '?')",(dt.datetime.now(), data_value, first_response))
    #time.sleep(5)    
    db_connection.commit()
    #time.sleep(5)

    response = ''.join(response)
    #print '---'
    if '200 OK' in response:
        tw.log.info('nimbits POST successful')
        #print 'nimbits POST successful'
    else:
        tw.log.error('nimbits POST unsuccessful')
        #print 'nimbits POST unsuccessful'
    #print '---'

    #print 'deactivating GPRS'
    s.write('AT#GPRS=0\r\n')
    time.sleep(5)
    response = pause_and_read_serial()
    if is_string_in_response('OK', response):
        tw.log.info('good GPRS off response')
    else:
        tw.log.warning('bad GPRS off response')

    # sleep until next minute
    time.sleep(60)

