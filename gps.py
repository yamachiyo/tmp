# -*- coding: utf-8 -*-
#!/usr/bin/python

import RPi.GPIO as GPIO
import time, serial

port = serial.Serial("/dev/ttyAMA0", 57600)

while True:
    gps_data = port.readline()
    print gps_data
    port.flushInput()
    time.sleep(1)

port.close()
