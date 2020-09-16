# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
from datetime import datetime
from gpiozero import CPUTemperature
import time
import cv2
import pigpio
import os

#constants
verticalvalue = 2300
horizontalvalue = 2000
verticalpin = 25
horizontalpin = 27
horizontalresolution = 640
verticalresolution = 480
setfps = 32

#runs pigpiod
os.system("sudo pigpiod")

#links pigpio to the pi
pi = pigpio.pi()

#sets intial positions of the servos
pi.set_servo_pulsewidth(verticalpin, verticalvalue)
pi.set_servo_pulsewidth(horizontalpin, horizontalvalue) 

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (horizontalresolution, verticalresolution)
camera.framerate = setfps
rawCapture = PiRGBArray(camera, size=(horizontalresolution, verticalresolution))
FaceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# allow the camera to warmup
time.sleep(0.1)
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

    #time at start of frame
    a = datetime.now()

    # grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
    image = frame.array
    # show the frame
    imgGray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    faces = FaceCascade.detectMultiScale(imgGray,1.1,10)
    for (x,y,w,h) in faces:
        # cv2.rectangle(imgGray,(x,y),(x+w,y+h),(255,0.255),2)
        #Based on the position of the bounding box, the camera will move to keep in centered

        #if nothing is detected for 5 seconds reset back to initial position
        # magic code that will work eventually 

        #Have it record the time when a face is registered ->> (when x is printed) and set that to a variable
        #if the current time is more than 10 seconds from the originally set value, issue a reset command to set servos to initial position (make that reset state a function)

        #Horizontal detection
        if x < 220: #min value
            if horizontalvalue <= 2400: #values of servo must be kept between 500 - 2500
                horizontalvalue = horizontalvalue + 100
            pi.set_servo_pulsewidth(horizontalpin, horizontalvalue) #sends command to servo
        elif x >= 420: #max value
            if horizontalvalue >= 100:
                horizontalvalue = horizontalvalue - 100
            pi.set_servo_pulsewidth(horizontalpin, horizontalvalue) 
        #Vertical detection
        if y < 150:
            if verticalvalue >= 100:
                verticalvalue = verticalvalue - 100
            pi.set_servo_pulsewidth(verticalpin, verticalvalue) 
        elif y >= 250:
            if verticalvalue <= 2400:
                verticalvalue = verticalvalue + 100
            pi.set_servo_pulsewidth(verticalpin, verticalvalue)


    #fetches CPU temperature
    cpu = CPUTemperature()

    #time at end of frame
    b = datetime.now()

    #calculates fps
    c = b - a
    seconds = c.total_seconds()
    fps = 1/seconds

    #prints status to terminal
    print("FPS: {:0.0f} Temperature: {:0.2f} C ".format(fps, cpu.temperature),end='\r')

    #displays the viewfinder
    # cv2.imshow("Frame", imgGray)

    key = cv2.waitKey(1) & 0xFF
	# clears the stream in preparation for the next frame
    rawCapture.truncate(0)
	# if the `q` key was pressed, break from the loop
    if key == ord("q"):
	    break