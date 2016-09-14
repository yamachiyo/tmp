#!/usr/bin/env python
# coding: utf-8
import time
import RPi.GPIO as GPIO
import random

class Stepmotor_controller:
    GPIO.setmode(GPIO.BOARD)
    pin_Clock = 3                 #RPi pin No.
    pin_CW = 5                 #
    pins = [pin_Clock, pin_CW]
    GPIO.setup(pins, GPIO.OUT)
    s_arg = 0.5                 #ステップ角度
    width = 0.02                #ステップ幅
    coef = 0.3                  #回転角調整用係数
    s_num = 50		#一度に送るステップ数上限
    
    def __init__(self):

        GPIO.output(self.pin_Clock, GPIO.LOW)
        GPIO.output(self.pin_CW, GPIO.LOW)
        self.go_to = -500.0
        self.arg = 0.0
        self.total_step = 0

    def drive_motor(self):
            
	self.arg = self.go_to / 3.1415 * 180        #radian -> degree
	self.arg = self.arg * self.coef             #係数かける
	arg_step = int(self.arg / self.s_arg)       #位置をステップ数に変換
	step_n = arg_step - self.total_step         #現在位置からの必要ステップを計算

        if step_n > self.s_num:			#ステップ数上限を超えるか
        	step_n = self.s_num
        elif step_n < -self.s_num:	#ステップ数上限
        	step_n = -self.s_num

        self.total_step = self.total_step + step_n  #今までの合計ステップ
        

        if step_n > 0:              #正転
            while step_n > 0:
                GPIO.output(self.pin_CW, GPIO.HIGH)

                GPIO.output(self.pin_Clock, GPIO.HIGH)
                time.sleep(self.width)
                GPIO.output(self.pin_Clock, GPIO.LOW)
                time.sleep(self.width)
                GPIO.output(self.pin_Clock, GPIO.HIGH)
                time.sleep(self.width)
                GPIO.output(self.pin_Clock, GPIO.LOW)
                time.sleep(self.width)

                step_n -= 1


        elif step_n < 0:            #逆転
            while step_n < 0:
                GPIO.output(self.pin_CW, GPIO.LOW)
                
                GPIO.output(self.pin_Clock, GPIO.HIGH)
                time.sleep(self.width)
                GPIO.output(self.pin_Clock, GPIO.LOW)
                time.sleep(self.width)
                GPIO.output(self.pin_Clock, GPIO.HIGH)
                time.sleep(self.width)
                GPIO.output(self.pin_Clock, GPIO.LOW)
                time.sleep(self.width)

                step_n += 1



if __name__ == "__main__":
    sm = Stepmotor_controller()
    while True:
        sm.go_to = 1
        sm.drive_motor()
        print sm.arg
        time.sleep(3)
        
        sm.go_to = -1
        sm.drive_motor()
        print sm.arg
        time.sleep(3)

    #GPIO.cleanup()

