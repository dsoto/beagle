import beaglebone as bb
import time
import datetime as dt

tag = 'kitchen'
ip = '108.166.92.185'

while (1):
    data_value = bb.read_ain2()
    time_stamp = dt.datetime.now().isoformat()

    bb.post_custom_server_http(ip, tag, data_value, time_stamp)

    time.sleep(60 * 5)