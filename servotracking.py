# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import RPi.GPIO as GPIO




import pigpio

pi = pigpio.pi()

# #Declaration of GPIO pins for servos
# servoPIN0 = 17
# servoPIN1 = 27

# #Mode set for servos
# GPIO.setmode(GPIO.BCM)

# GPIO.setup(servoPIN0, GPIO.OUT)
# GPIO.setup(servoPIN1, GPIO.OUT)

# vertical = GPIO.PWM(servoPIN0, 50) # GPIO 17 for PWM with 50Hz
# horizontal = GPIO.PWM(servoPIN1, 50) # GPIO 27 for PWM with 50Hz

# # Initialization
# horizontal.start(10) 
# vertical.start(10)

pi.set_servo_pulsewidth(17, 2500) # vertical
pi.set_servo_pulsewidth(27, 2000) # horizontal

horizontalvalue = 1500
verticalvalue = 1500

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
        cv2.rectangle(imgGray,(x,y),(x+w,y+h),(255,0.255),2)
        if x < 320:
            if horizontalvalue >= 0:
                horizontalvalue = horizontalvalue - 100
            pi.set_servo_pulsewidth(27, horizontalvalue) # position anti-clockwise
        elif x >= 320:
            if horizontalvalue <= 2000:
                horizontalvalue = horizontalvalue + 100
            pi.set_servo_pulsewidth(27, horizontalvalue) # position anti-clockwise
        
        if y < 200:
            if verticalvalue >= 0:
                verticalvalue = verticalvalue - 100
            pi.set_servo_pulsewidth(17, verticalvalue) # position anti-clockwise
        elif y >= 200:
            if verticalvalue <= 2000:
                verticalvalue = verticalvalue + 100
            pi.set_servo_pulsewidth(17, verticalvalue) # position anti-clockwise


    cv2.imshow("Frame", imgGray)
    key = cv2.waitKey(1) & 0xFF
	# clear the stream in preparation for the next frame
    rawCapture.truncate(0)
	# if the `q` key was pressed, break from the loop
    if key == ord("q"):
	    break