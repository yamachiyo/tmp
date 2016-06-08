#coding :utf-8
import spidev, serial, time
import blescan
import bluetooth._bluetooth as bluez
import iBeacon_receiver_sub_2
import maxsonar

set_uptake_number_of_once = 15
set_terget_of_beacon_major = 0
set_terget_of_beacon_minor = 1

ser = serial.Serial('/dev/ttyAMA0', 115200)

sonar = maxsonar.Maxsonar()
spi = spidev.SpiDev()

ch0 = 0x00
ch1 = 0x10

f = open('test.txt' ,'w')

while True:
    """tenma = iBeacon_receiver_sub_2.Beacon_receiver()
    tenma.all_receive(set_uptake_number_of_once)    
    tenma.select(set_terget_of_beacon_major,set_terget_of_beacon_minor)
    tenma.matrix()
    get_dataA = tenma.average()"""
    get_dataA = [-50]
    
    m0 = round(sonar.measure(ch0),2) +0.001
    m1 = round(sonar.measure(ch1),2) +0.001

    mes_ch0 = round(m0,3)
    mes_ch1 = round(m1,3)

    get_dataA.append(mes_ch0)
    get_dataA.append(mes_ch1)
    print get_dataA
    
    send_val = str(get_dataA)
    ser.write(send_val)
#    ser.write(send_val+"\n")
    time.sleep(0.02)

    f.write(send_val)
    f.write('\n')

spi.close()
ser.close()
f.close()
