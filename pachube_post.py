import requests
import json

headers = {"X-PachubeApiKey": "yKcC6HugqvNtshxI6qEreOPYs9qQG7gZfloc3JQWPbQ"}

data={"version":"1.0.0","datastreams":[{"id":"01","current_value":"200"}]}

resp=requests.put('http://api.pachube.com/v2/feeds/39985',headers=headers,data=json.dumps(data))


