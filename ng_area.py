#!/usr/bin/env python
import numpy as np
import rospy
from std_msgs.msg import Int8
from sensor_msgs.msg import LaserScan

class NGArea:
    u_angle = 0.25	#unit angle of LRF[degree]
    short_d = 0.3	#distance to make detour[m]
    short_n = 10	#number of points to detour
    c_angle = 40.0	#angle of center position[degree]
    a_angle = 180.0	#all angle to use[degree]
    lrf_data = LaserScan()
    data_nga = Int8()

    def __init__(self):
        self.p = 0
        self.pub1 = rospy.Publisher('position_jr', Int8 ,queue_size=3)

    def subscribe(self):
        sub1 = rospy.Subscriber('/scan', LaserScan, self.callback1)

    def callback1(self, msg):
        self.lrf_data = msg
 
    def sort_data(self):	#get all LRF data
        data_r = 0.
        self.data_list = []
        self.n = len(self.lrf_data.ranges)
        for i in range(0,self.n-1):
            data_a = [i * self.u_angle]		#angle
            data_r = list(self.lrf_data.ranges[i:i+1])
            self.data_list.append(data_a + data_r)
        #print(self.data_list)

    def find_short(self):	#get short distance data
        self.short_list = []
        #n = len(self.data_list)
        for i in range(0,self.n-1):
            if self.data_list[i][1] < self.short_d :
                self.short_list.append(self.data_list[i])
        #print(self.short_list)

    def decide_ng(self):	#decide NG area
        data_nga = []
        p1 = 0		#number of points in position1
        p2 = 0		#number of points in position2
        p3 = 0		#number of points in position3
        n = len(self.short_list)
        c_angle_b = self.n/2*self.u_angle - self.c_angle/2
        c_angle_e = self.n/2*self.u_angle + self.c_angle/2
        a_angle_b = self.n/2*self.u_angle - self.a_angle/2
        a_angle_e = self.n/2*self.u_angle + self.a_angle/2
        for i in range(0,n-1):
            if c_angle_b < self.short_list[i][0] < c_angle_e :
                p2 += 1
            elif a_angle_b < self.short_list[i][0] < c_angle_b :
                p1 += 1
            elif c_angle_e < self.short_list[i][0] < a_angle_e :
                p3 += 1
        if p1 >= self.short_n :
            data_nga.append(1)
        if p2 >= self.short_n :
            data_nga.append(2)
        if p3 >= self.short_n :
            data_nga.append(3)

        print(data_nga)

    def publish(self):
        self.pub1.publish(self.data_nga)       


if __name__ == "__main__":
    rospy.init_node('ng_area')

    NG = NGArea()
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        NG.subscribe()           
        NG.sort_data() 
        NG.find_short() 
        NG.decide_ng() 
        NG.publish()

        rate.sleep()

