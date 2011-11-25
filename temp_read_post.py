import requests
import json
import random
import time
import twiggy as tw
import serial

s = serial.Serial('/dev/ttyUSB0', baudrate=9600, timeout=1)

tw.quickSetup(file='pachube.log')
tw.log.info('starting pachube_post.py')

# authentication headers
headers = {"X-PachubeApiKey": "yKcC6HugqvNtshxI6qEreOPYs9qQG7gZfloc3JQWPbQ"}

# sleep for a minute, send random number to pachube in json format
while 1:
    # read temperature from arduino
    s.write(chr(0x00))
    time.sleep(0.5)
    data_value=ord(s.read()) / 1024.0 * 5 * 100

    data={"version":"1.0.0","datastreams":[{"id":"01","current_value":data_value}]}
    try:
        resp=requests.put('http://api.pachube.com/v2/feeds/39985',headers=headers,data=json.dumps(data))
    except:
        tw.log.trace('error').warning('bad request')
    if resp.status_code == 200:
        tw.log.info('response value = ' + str(resp.status_code))
    else:
        tw.log.error('response value = ' + str(resp.status_code))
    time.sleep(60)
