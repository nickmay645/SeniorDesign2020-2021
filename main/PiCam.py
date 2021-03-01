# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import sys
import math

import ThermalPlot
import LED

class RaspCam:

    def __init__(self):

        self.thermalx = 0
        self.thermaly = 0
        toggle = False

        count = 0

        # initialize the camera and grab a reference to the raw camera capture
        camera = PiCamera()
        camera.resolution = (640, 480)
        camera.framerate = 32
        rawCapture = PiRGBArray(camera, size=(640, 480))
        FaceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

        # allow the camera to warmup
        time.sleep(0.1)
        # capture frames from the camera
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            # grab the raw NumPy array representing the image, then initialize the timestamp
            # and occupied/unoccupied text
            image = frame.array
            # show the frame
            imgGray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
            faces = FaceCascade.detectMultiScale(imgGray,1.1,10)

            for (x,y,w,h) in faces:
                self.thermalx = math.floor((x + (w/2))/4)
                self.thermaly = math.floor((y + (h/4))/4)
                cv2.rectangle(imgGray,(self.thermalx*4,self.thermaly*4),(self.thermalx*4+1,self.thermaly*4+1),(255,0.255),2)
                ThermalPlot.ThermalData(self.thermalx,self.thermaly)
               
                #code for verifying that its actually a face,
                #creates a buffer to avoid and accidental face detections
                # if x != 0 and count == 15:
                #     count = 0
                #     print(ThermalPlot.ThermalData(self.thermalx,self.thermaly))
                # else:
                #     count = count + 1
            
            cv2.imshow("Frame", imgGray)
            key = cv2.waitKey(1) & 0xFF
            # clear the stream in preparation for the next frame
            rawCapture.truncate(0)
            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                break