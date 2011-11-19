import requests
import json
import random
import time

# authentication headers 
headers = {"X-PachubeApiKey": "yKcC6HugqvNtshxI6qEreOPYs9qQG7gZfloc3JQWPbQ"}

# sleep for a minute, send random number to pachube in json format
while 1:
    time.sleep(60)
    data_value = 100 + random.random() * 50
    data={"version":"1.0.0","datastreams":[{"id":"01","current_value":data_value}]}
    resp=requests.put('http://api.pachube.com/v2/feeds/39985',headers=headers,data=json.dumps(data))
