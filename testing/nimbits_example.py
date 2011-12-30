import requests
import random
import time

while 1:

    # generate random data value
    value = random.random() * 10

    # create dictionary
    data = {"email":"email@email.com",
            "secret":"1234567890-1234567890",
            "point":"My_Test_Stream",
            "value":value}

    # use requests library to post to nimbits
    r = requests.post("http://app.nimbits.com/service/currentvalue", data=data)

    # sleep for a minute
    time.sleep(60)