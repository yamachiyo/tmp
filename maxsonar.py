import spidev
import time

class Maxsonar:
    def __init__(self):
        self.spi = spidev.SpiDev()
        self.spi.open(0,0)
        self.spi.max_speed_hz=1000000
        self.spi.bits_per_word=8

    def measure(self, ch):
        dummy = 0xff
        start = 0x47
        sgl = 0x20
        msbf = 0x08
        
        ad = self.spi.xfer2([(start + sgl + ch + msbf), dummy])
        val = ((((ad[0] & 0x03) << 8) + ad[1]) * 3.3) / 1023
        return val


