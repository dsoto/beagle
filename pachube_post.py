import requests
import json
import random
import time
import twiggy as tw

tw.quickSetup(file='pachube.log')
tw.log.info('starting pachube_post.py')

# authentication headers
headers = {"X-PachubeApiKey": "yKcC6HugqvNtshxI6qEreOPYs9qQG7gZfloc3JQWPbQ"}

# sleep for a minute, send random number to pachube in json format
while 1:
    data_value = 100 + random.random() * 50
    tw.log.info('logging value = ' + str(data_value))
    data={"version":"1.0.0","datastreams":[{"id":"01","current_value":data_value}]}
    resp=requests.put('http://api.pachube.com/v2/feeds/39985',headers=headers,data=json.dumps(data))
    if resp.status_code == 200:
        tw.log.info('response value = ' + str(resp.status_code))
    else:
        tw.log.error('response value = ' + str(resp.status_code))
    time.sleep(60)
