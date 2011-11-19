import requests
import json

data_value = 200

headers = {"X-PachubeApiKey": "yKcC6HugqvNtshxI6qEreOPYs9qQG7gZfloc3JQWPbQ"}

data={"version":"1.0.0","datastreams":[{"id":"01","current_value":data_value}]}

resp=requests.put('http://api.pachube.com/v2/feeds/39985',headers=headers,data=json.dumps(data))


