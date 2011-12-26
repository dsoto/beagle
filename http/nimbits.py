import requests
import random
import time

while 1:

    # generate random data value
    value = random.random() * 10
    value = 25

    # create dictionary
    data = {"email":"drdrsoto@gmail.com",
            "secret":"01787ade-c6d6-4f9b-8b86-20850af010d9",
            "point":"603_Test_Stream",
            "value":value}

    # use requests library to post to nimbits
    r = requests.post("http://app.nimbits.com/service/currentvalue", data=data)

    # sleep for a minute
    time.sleep(60)