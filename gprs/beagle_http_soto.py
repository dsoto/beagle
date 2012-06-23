import beaglebone as bb
import time
import datetime as dt

tag = 'kitchen'
ip = '108.166.92.185'

start_temp = bb.read_ain2()
high = start_temp
low = start_temp

while (1):
    data_value = bb.read_ain2(verbose=False)

    time_stamp = dt.datetime.now().isoformat()

    if data_value > high:
        high = data_value
        print 'all time high', high, time_stamp
    if data_value < low:
        low = data_value
        print 'all time low', low, time_stamp

    # am i doing anything with timestamp?
    bb.post_custom_server_http(ip, tag, data_value, time_stamp)

    time.sleep(60 * 5)
    #time.sleep(30)
