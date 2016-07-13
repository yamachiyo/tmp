#!/usr/bin/env python
import numpy as np
import rospy
from nkc_program.msg import Ints32
from std_msgs.msg import Int8

class CheckMove:
    ng_list = Ints32()
    target = Int8()

    def __init__(self):
        self.p = 0
        self.pub1 = rospy.Publisher('position_jr', Int8 ,queue_size=3)

    def subscribe(self):
        sub1 = rospy.Subscriber('ng_position', Ints32, self.callback1)
        sub2 = rospy.Subscriber('position_j', Int8, self.callback2)

    def callback1(self, msg):
        self.ng_list = msg.data

    def callback2(self, msg):
        self.target = msg.data
 
    def calc(self):
        self.go_to = -1
        if not self.target in self.ng_list:
            self.go_to = self.target

    def publish(self):
        self.pub1.publish(self.data_nga)       


if __name__ == "__main__":
    rospy.init_node('check_move')

    CM = CheckMove()
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        CM.subscribe()           
        CM.calc() 
        if not CM.go_to == -1:
            CM.publish()

        rate.sleep()

