#Interconnect Diagram:
#S -> GPIO 17 on Pi
#V -> 5V on Pi
#G -> GND on Pi

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers
 
RELAYGPIO = 17
GPIO.setup(RELAYGPIO, GPIO.OUT) # GPIO Assign mode
GPIO.output(RELAYGPIO, GPIO.LOW) # out
time.sleep(5)
GPIO.output(RELAYGPIO, GPIO.HIGH) # on
time.sleep(5)
GPIO.output(RELAYGPIO, GPIO.LOW) # out

