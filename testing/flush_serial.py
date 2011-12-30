import serial
import time

s=serial.Serial('/dev/ttyUSB0',baudrate=115200,timeout=2)
response = s.readlines()
print response

s.write('AT\r\n')
response=s.readlines()
print response
