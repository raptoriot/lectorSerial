# !/usr/bin/python
import serial
import time


serie = serial.Serial('/dev/ttyUSB0', baudrate=9600, timeout=3.0)
cadena = ''

while True:
    print(serie.read())
