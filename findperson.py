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
        self.cascade = cv2.CascadeClassifier("/usr/share/OpenCV/haarcascades/haarcascade_fullbody.xml")
    
    def find(self):		#find person
        person = self.cascade.detectMultiScale(self.image_g, scaleFactor=1.1, minNeighbors=2, minSize=(50,100))
        #print person

        if len(person) > 0:
            for (x,y,w,h) in person:	#make rectangle
                cv2.rectangle(self.image, (x,y), (x+w,y+h), (200,0,0), thickness=2)
                print x+w/2, y+h/2	#center

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

