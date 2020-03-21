# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 18:29:54 2020
@author: amann
"""
from __future__ import print_function
import cv2 as cv

def detectAndDisplay(frame):
    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frame_gray = cv.equalizeHist(frame_gray)
    #-- Detect bills
    bills = bill_cascade.detectMultiScale(frame_gray)
    print (bills)
    for (x,y,w,h) in bills:
        center = (x + w//2, y + h//2)
        cv.putText(frame,"Receipt",(x+w//3,y+15),cv.FONT_HERSHEY_PLAIN,1,(0,0,255),1)
        cv.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
        billROI = frame_gray[y:y+h,x:x+w]
        
        #-- In each bill, detect data sections
        '''
        datasec = data_cascade.detectMultiScale(billROI)
        -------------------------------------------------------
        Working on this section yet, data collection is being done to make a classifier for differenct data sections in a receipt.
        This section is open for active contribution. Send your pull request with your data set included if you want to contribute
        to this section.
        -------------------------------------------------------
        '''
        
    cv.imshow('Bill Detector', frame)

bill_cascade_local = 'cascade.xml'
bill_cascade = cv.CascadeClassifier()
#-- 1. Load the cascades
if not bill_cascade.load(bill_cascade_local):
    print('--(!)Error loading bill cascade')
    exit(0)
camera_device = 0
#-- 2. Read the video stream
cap = cv.VideoCapture(camera_device)
if not cap.isOpened:
    print('--(!)Error opening video capture')
    exit(0)
while True:
    ret, frame = cap.read()
    ls = cap.retrieve()
    if frame is None:
        print('--(!) No captured frame -- Break!')
        break
    detectAndDisplay(frame)
    if cv.waitKey(10) == 27:
        break
