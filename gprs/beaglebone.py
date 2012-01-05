import serial
import time
import random
import twiggy as tw
import sqlite3
import datetime as dt
import requests
import json

def post_nimbits_http(stream, value):
    nimbits_data = {"email":"drdrsoto@gmail.com",
                    "secret":"01787ade-c6d6-4f9b-8b86-20850af010d9",
                    "point":stream,
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

def write_to_db(time_stamp, data_value, response, db_cursor, db_connection):
    query_string = 'insert into logs (time_stamp, value, response) values (?,?,?)'
    db_cursor.execute(query_string, (time_stamp, data_value, response))
    db_connection.commit()

def post_nimbits_staggered(data_value):

    content = ''
    content += 'secret=01787ade-c6d6-4f9b-8b86-20850af010d9'
    content += '&email=drdrsoto@gmail.com'
    content += '&value=%s' % data_value
    content += '&point=%s' % stream_name
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


def initiate_modem(s):
    tw.log.info('flushing out serial port')
    pause_and_read_serial(s)

    s.write('AT\r\n')
    response = pause_and_read_serial(s)
    if is_string_in_response('OK', response):
        tw.log.info('good AT response')
    else:
        tw.log.warning('bad AT response')

    s.write('AT#GPRS=1\r\n')
    response = pause_and_read_serial(s)
    if is_string_in_response('OK', response):
        tw.log.info('good GPRS response')
    else:
        tw.log.warning('bad GPRS response')

    s.write('AT+CGDCONT=1,"IP","epc.tmobile.com","0.0.0.0",0,0\r\n')
    response = pause_and_read_serial(s)
    if is_string_in_response('OK', response):
        tw.log.info('good CGDCONT response')
    else:
        tw.log.warning('bad CGDCONT response')

    connection_attempt = 1
    while 1:
        s.write('AT#SD=2,0,80,"app.nimbits.com"\r\n')
        response = pause_and_read_serial(s)
        if is_string_in_response('CONNECT', response):
            tw.log.info('good SD response ' + str(connection_attempt))
            break
        else:
            tw.log.warning('bad SD response ' + str(connection_attempt))
            time.sleep(5)
            connection_attempt += 1

def read_ain2():
    num_avg = 20
    data_value = 0
    for i in range(num_avg):
        f = open('/sys/devices/platform/tsc/ain2')
        data_value_string = ''
        while 1:
            char = f.read(1)
            if char == '\x00':
                break
            else:
                data_value_string += char
        #tw.log.info(data_value_string)
        data_value += float(data_value_string)
        f.close()
        time.sleep(1.0)
    data_value = data_value / num_avg
    tw.log.info('avg = ' + str(data_value))
    return data_value

def parse_response(s):
    time.sleep(15) # need extra time for html response

    response = pause_and_read_serial()
    if len(response) > 0:
        first_response = response[0].strip()
    else:
        first_response = 'No Response'

    tw.log.info(first_response)

    if '200 OK' in first_response:
        tw.log.info('nimbits POST successful')
    else:
        tw.log.error('nimbits POST unsuccessful')

    return first_response

def post_pachube_http(value):
    headers = {"X-PachubeApiKey": "yKcC6HugqvNtshxI6qEreOPYs9qQG7gZfloc3JQWPbQ"}
    data={"version":"1.0.0","datastreams":[{"id":"01","current_value":value}]}
    try:
        r = requests.put('http://api.pachube.com/v2/feeds/43073',headers=headers,data=json.dumps(data))
    except:
        tw.log.trace('error').error('bad put to pachube')
    log_message = 'pachube response value = ' + str(r.status_code)
    if r.status_code == 200:
        tw.log.info(log_message)
    else:
        tw.log.error(log_message)


def pause_and_read_serial(s):
    time.sleep(1)
    response = s.readlines()
    return response


