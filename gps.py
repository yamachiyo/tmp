# -*- coding: utf-8 -*-
#!/usr/bin/python

import RPi.GPIO as GPIO
import time, serial
import matplotlib
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt

port = serial.Serial("/dev/ttyAMA0", 57600)

#matplotlib
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.set_xlabel("longitude")
ax.set_ylabel("latitude")

while True:
    gps_data = port.readline()
    port.flushInput()
    #gps_data = "0 1.0 2.0 3.0 4.0 5 6 7.0 8.0 9.0 10.0 11.0 12.0 13.0 14.0" #test
    datalist = gps_data.split()
    if len(datalist) == 15:
        lat = float(datalist[2])
        lon = float(datalist[3])
        print gps_data
        print datalist
        print lat,lon
        ax.plot(lat,lon,"bo")
    plt.pause(1.0)
    #time.sleep(1)

port.close()
