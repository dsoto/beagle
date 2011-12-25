# script uses easy gprs commands to download website
# does not work every time run

import serial
import time
import random
import twiggy as tw

def pause_and_read_serial():
    time.sleep(1)
    response = s.readlines()
    return response

def post_nimbits_staggered():

    data_value = 20 + 10*random.random()
    tw.log.info('data_value = ' + str(data_value))

    content = ''
    content += 'secret=01787ade-c6d6-4f9b-8b86-20850af010d9'
    content += '&email=drdrsoto%40gmail.com'
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

def post_nimbits():
    s.write('GET /service/currentvalue HTTP/1.1\r\n')
    s.write('Host: app.nimbits.com\r\n')
    s.write('Content-Length: 101\r\n')
    s.write('Content-Type: application/x-www-form-urlencoded\r\n')
    s.write('Accept-Encoding: identity, deflate, compress, gzip\r\n')
    s.write('Accept: */*\r\n')
    s.write('User-Agent: python-requests/0.8.1\r\n\r\n')
    s.write('secret=01787ade-c6d6-4f9b-8b86-20850af010d9')
    s.write('&email=drdrsoto%40gmail.com')
    s.write('&value=20&point=603_Test_Stream')

def get_columbia_website():
    s.write('GET /~ds2998/ HTTP/1.1\r\n')
    s.write('HOST: www.columbia.edu 80\r\n')
    s.write('\r\n')

print 'opening serial port'
s = serial.Serial('/dev/ttyUSB0',
                  baudrate=115200,
                  timeout=1)


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

while (1):
    tw.log.info('top of loop')

    tw.log.info('flushing out serial port')
    pause_and_read_serial()

    print 'testing using AT command'
    s.write('AT\r\n')
    response = pause_and_read_serial()
    if is_string_in_response('OK', response):
        tw.log.info('good AT response')
    else:
        tw.log.error('bad AT response')

    print 'activating GPRS'
    s.write('AT#GPRS=1\r\n')
    response = pause_and_read_serial()
    if is_string_in_response('OK', response):
        tw.log.info('good GPRS response')
    else:
        tw.log.error('bad GPRS response')

    print 'activating context'
    s.write('AT+CGDCONT=1,"IP","epc.tmobile.com","0.0.0.0",0,0\r\n')
    response = pause_and_read_serial()
    if is_string_in_response('OK', response):
        tw.log.info('good CGDCONT response')
    else:
        tw.log.error('bad CGDCONT response')

    print 'socket dial'
    s.write('AT#SD=2,0,80,"app.nimbits.com"\r\n')
    #s.write('AT#SD=2,0,80,"www.columbia.edu"\r\n')
    response = pause_and_read_serial()
    if is_string_in_response('CONNECT', response):
        tw.log.info('good SD response')
    else:
        tw.log.error('bad SD response')

    print 'posting to nimbits'
    #get_columbia_website()
    #post_nimbits()
    post_nimbits_staggered()
    print 'sleeping'
    time.sleep(15) # need extra time for html response
    print 'post response'

    response = pause_and_read_serial()
    response = ''.join(response)
    print '---'
    if '200 OK' in response:
        tw.log.info('nimbits POST successful')
        print 'nimbits POST successful'
    else:
        tw.log.error('nimbits POST unsuccessful')
        print 'nimbits POST unsuccessful'
    print '---'

    print 'deactivating GPRS'
    s.write('AT#GPRS=0\r\n')
    time.sleep(5)
    response = pause_and_read_serial()
    if is_string_in_response('OK', response):
        tw.log.info('good GPRS off response')
    else:
        tw.log.error('bad GPRS off response')

    time.sleep(60)

print 'closing serial port'
s.close()
