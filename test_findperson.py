#!/usr/bin/env python
# coding: utf-8

import time, cv2
import numpy as np

class FindPerson:
    def __init__(self):

        self.capture = cv2.VideoCapture(0)

    def get_image(self):	#get camera image
        o, self.image = self.capture.read()
        #cv2.imshow("Original", self.image)

    def gray_image(self):	#change color gray
        self.image_g = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)
        #cv2.imshow("Gray", self.image_g)

    def read_class(self):	#read classifier file
        self.hog = cv2.HOGDescriptor()

    
    def find(self):		#find person
        #self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        self.hog.setSVMDetector(cv2.HOGDescriptor_getPeopleDetector48x96())
        hogParams = {'winStride': (8, 8), 'padding': (32, 32), 'scale': 1.05}
        human, r = self.hog.detectMultiScale(self.image_g, **hogParams)

        for (x, y, w, h) in human:
            cv2.rectangle(self.image, (x, y),(x+w, y+h),(200,0,0), 3)
            print x+w/2

        cv2.imshow("Result", self.image)
        cv2.waitKey(1)


if __name__ == "__main__":
    fp = FindPerson()

    fp.read_class()
    while True:
        fp.get_image()
        fp.gray_image()
        fp.find()

        time.sleep(0.01)

