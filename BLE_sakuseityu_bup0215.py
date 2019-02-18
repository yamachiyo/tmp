#!/usr/bin/env python
# coding: utf-8
#ver1.00-00
#BLE用プログラム
from pybleno import *
import array
import struct
import sys
import signal
import traceback
from builtins import str

class BLE_ctl:
    name = "agbee_vehicle001"	#BLE name
    service_remocon = "ab00"	#service UUID to receive data
    chara_remocon = "ab00"	#characteristic UUID to receive data

    bleno = Bleno()


    def __init__(self):
        pass

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

    def main(self):
        self.bleno.on('stateChange', self.onStateChange)
        self.bleno.on('advertisingStart', self.onAdvertisingStart)

        self.bleno.start()

        #koko ha ros node ka goni sakujo
        print ('Hit <ENTER> to disconnect')
        if (sys.version_info > (3, 0)):
            input()
        else:
            raw_input()

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
          
        self._value = array.array('B', [0] * 0)
        self._updateValueCallback = None
          
    def onReadRequest(self, offset, callback):
        print(self._value)
        callback(Characteristic.RESULT_SUCCESS, self._value)

    def onWriteRequest(self, data, offset, withoutResponse, callback):
        #data jushinji no shori
        self._value = data

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

