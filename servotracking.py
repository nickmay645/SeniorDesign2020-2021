# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
from datetime import datetime
from gpiozero import CPUTemperature
import time
import cv2
import pigpio
import os

#runs pigpiod
os.system("sudo pigpiod")

#links pigpio to the pi
pi = pigpio.pi()

#initial values
verticalvalue = 2300
horizontalvalue = 2000

#sets intial positions of the servos
pi.set_servo_pulsewidth(17, verticalvalue)
pi.set_servo_pulsewidth(27, horizontalvalue) 

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

    a = datetime.now()

    # grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
    image = frame.array
    # show the frame
    imgGray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    faces = FaceCascade.detectMultiScale(imgGray,1.1,10)
    for (x,y,w,h) in faces:
        #cv2.rectangle(imgGray,(x,y),(x+w,y+h),(255,0.255),2)
        #Based on the position of the bounding box, the camera will move to keep in centered
        #Horizontal detection
        if x < 220: #min value
            if horizontalvalue <= 2400: #values of servo must be kept between 500 - 2500
                horizontalvalue = horizontalvalue + 100
            pi.set_servo_pulsewidth(27, horizontalvalue) #sends command to servo
        elif x >= 420: #max value
            if horizontalvalue >= 100:
                horizontalvalue = horizontalvalue - 100
            pi.set_servo_pulsewidth(27, horizontalvalue) 
        #Vertical detection
        if y < 150:
            if verticalvalue >= 100:
                verticalvalue = verticalvalue - 100
            pi.set_servo_pulsewidth(17, verticalvalue) 
        elif y >= 250:
            if verticalvalue <= 2400:
                verticalvalue = verticalvalue + 100
            pi.set_servo_pulsewidth(17, verticalvalue)

    b = datetime.now()
    #calculates fps
    c = b - a
    seconds = c.total_seconds()
    fps = 1/seconds
    # print("FPS: {:0.2f}".format(fps),end='\r')

    cpu = CPUTemperature()
    # print("\n CPU Temperature: ",cpu.temperature,end='\r')

    print("FPS: {:0.2f}\nTemperature: {}\n".format(fps, cpu.temperature),end='\r')

    #displays the viewfinder
    #cv2.imshow("Frame", imgGray)
    key = cv2.waitKey(1) & 0xFF
	# clears the stream in preparation for the next frame
    rawCapture.truncate(0)
	# if the `q` key was pressed, break from the loop
    if key == ord("q"):
	    break