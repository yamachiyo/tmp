# -*- coding: utf-8 -*-
#!/usr/bin/python

import RPi.GPIO as GPIO
import os, smbus, time
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

    def setUp(self):
        self.b.write_byte_data(self.DevAdr, 0x00, 0xE0)
#		self.b.write_byte_data(self.DevAdr, 0x00, 0x10)
#		self.b.write_byte_data(self.DevAdr, 0x01, 0x20)
        self.b.write_byte_data(self.DevAdr, 0x02, 0x00)

    def getValueX(self):
        return self.getValue(0x03)

    def getValueY(self):
        return self.getValue(0x07)

    def getValueZ(self):
        return self.getValue(0x05)

    def getValue(self, adr):
        tmp = self.b.read_byte_data(self.DevAdr, adr)
        sign = tmp & 0x80
        tmp = tmp & 0x7F
        tmp = tmp<<8
        tmp = tmp | self.b.read_byte_data(self.DevAdr, adr+1)

        if sign > 0:
            tmp = tmp - 32768

        return tmp

#	tmp = self.b.read_word_data(self.DevAdr, adr)



# MAIN
myHMC5883L = HMC5883L()
myHMC5883L.setUp()

#matplotlib
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.set_xlabel("West <-> East")
ax.set_ylabel("South <-> North")
ax.axhline(2,ls=":")
ax.axvline(2,ls=":")

# LOOP
for a in range(1000):

    x = myHMC5883L.getValueX()
    y = myHMC5883L.getValueY()
    z = myHMC5883L.getValueZ()
    print("X=", x)
    print("Y=", y)
    print("Z=", z)
    print("----------")

    ax.plot(-x,y,"bo")
    plt.pause(0.5)
#    time.sleep(0.5)
