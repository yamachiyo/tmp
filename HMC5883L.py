# -*- coding: utf-8 -*-
#!/usr/bin/python

import RPi.GPIO as GPIO
import os, smbus, time, math
import matplotlib
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt

# HMC5883L Class
class HMC5883L():
    DevAdr = 0x1E
    myBus = ""
    if GPIO.RPI_INFO['P1_REVISION'] == 1:
        myBus = 0
    else:
        myBus = 1
    b = smbus.SMBus(myBus)

    x = 0
    y = 0
    z = 0

    def __init__(self):
        self.b.write_byte_data(self.DevAdr, 0x00, 0xE0)
#		self.b.write_byte_data(self.DevAdr, 0x00, 0x10)
#		self.b.write_byte_data(self.DevAdr, 0x01, 0x20)
        self.b.write_byte_data(self.DevAdr, 0x02, 0x00)

    def getValueX(self):
        self.x = self.getValue(0x03)

    def getValueY(self):
        self.y = self.getValue(0x07)

    def getValueZ(self):
        self.z = self.getValue(0x05)

    def getValue(self, adr):
        tmp = self.b.read_byte_data(self.DevAdr, adr)
        sign = tmp & 0x80
        tmp = tmp & 0x7F
        tmp = tmp<<8
        tmp = tmp | self.b.read_byte_data(self.DevAdr, adr+1)

        if sign > 0:
            tmp = tmp - 32768

        return tmp

    def offset(self):
        pass
        #base = 250
        #tmp = math.sqrt(self.x**2 + self.y**2)

        self.x = self.x + 100
        self.y = self.y + 150


# MAIN
measure = HMC5883L()

#matplotlib
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.set_xlabel("West <-> East")
ax.set_ylabel("South <-> North")
ax.axhline(2,ls=":")
ax.axvline(2,ls=":")

# LOOP
while True:

    measure.getValueX()
    measure.getValueY()
    measure.getValueZ()
    measure.offset()
    arg = math.atan2(-measure.x, measure.y) #[rad]
    arg = arg/3.14*180  #degree
    
    print "X= " + str(measure.x)
    print "Y= " + str(measure.y)
    print "Z= " + str(measure.z)
    print "arg from North :" + str(arg)
    print("----------")

    ax.plot(-measure.x,measure.y,"bo")
    plt.pause(0.5)
#    time.sleep(0.5)
