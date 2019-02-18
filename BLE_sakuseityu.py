#!/usr/bin/env python
# coding: utf-8
#ver0.01-00
#BLE用プログラム
#BLE remokon data wo string de manual_drive.py he okuru
from pybleno import *
import array
import struct
import sys
import signal
import traceback
from builtins import str
import rospy
from std_msgs.msg import String


class BLE_ctl:
    name = "agbee_vehicle001"	#BLE name
    service_remocon = "ab00"	#service UUID to receive data
    chara_remocon = "ab00"	#characteristic UUID to receive data

    bleno = Bleno()


    def __init__(self):
        self.RCdata = String()
        self.pub1 = rospy.Publisher('BLE_RCdata', String,queue_size=1)


    #kokokara kakusyu data tuushinkaishi
    def onStateChange(self,state):
       print('on -> stateChange: ' + state);

       if (state == 'poweredOn'):
         self.bleno.startAdvertising(self.name, [self.service_remocon])
       else:
         self.bleno.stopAdvertising();

    def onAdvertisingStart(self,error):	#start put out advertising packet
        print('on -> advertisingStart: ' + ('error ' + error if error else 'success'));

        if not error:
            self.bleno.setServices([
                BlenoPrimaryService({
                    'uuid': self.service_remocon,
                    'characteristics': [ 
                        EchoCharacteristic(self.chara_remocon)
                    ]
                })
            ])

    def publish(self):
        self.pub1.publish(self.RCdata)       

    def receive(self):
        self.RCdata = EchoCharacteristic.receive_data

    def main(self):
        rospy.init_node('BLE_ctl')
        rate = rospy.Rate(20)

        self.bleno.on('stateChange', self.onStateChange)
        self.bleno.on('advertisingStart', self.onAdvertisingStart)

        self.bleno.start()

        while not rospy.is_shutdown():
            self.receive()
            self.publish()

            rate.sleep()

        self.bleno.stopAdvertising()
        self.bleno.disconnect()

        print ('terminated.')
        sys.exit(1)



class EchoCharacteristic(Characteristic):	#data soujushinji no shori
    
    def __init__(self, uuid):
        Characteristic.__init__(self, {
            'uuid': uuid,
            'properties': ['read', 'write', 'notify'],
            'value': None
          })
          
        self.receive_data = ""
        self._value = array.array('B', [0] * 0)
        self._updateValueCallback = None
          
    def onReadRequest(self, offset, callback):
        print(self._value)
        callback(Characteristic.RESULT_SUCCESS, self._value)

    def onWriteRequest(self, data, offset, withoutResponse, callback):
        #data jushinji no shori
        self._value = data

        self.receive_data = self._value
        print(self._value)

        if self._updateValueCallback:
            print('EchoCharacteristic - onWriteRequest: notifying');
            
            self._updateValueCallback(self._value)
        
        callback(Characteristic.RESULT_SUCCESS)
        
    def onSubscribe(self, maxValueSize, updateValueCallback):
        print('EchoCharacteristic - onSubscribe')
        
        self._updateValueCallback = updateValueCallback

    def onUnsubscribe(self):
        print('EchoCharacteristic - onUnsubscribe');
        
        self._updateValueCallback = None





if __name__ == "__main__":
    BLE = BLE_ctl()
    BLE.main()

