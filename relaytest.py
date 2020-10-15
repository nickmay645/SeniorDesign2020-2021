#Interconnect Diagram:
#S -> GPIO 26 on Pi
#V -> 5V on Pi
#G -> GND on Pi

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers
 
RELAYGPIO = 26
GPIO.setup(RELAYGPIO, GPIO.OUT) # GPIO Assign mode
GPIO.output(RELAYGPIO, GPIO.LOW) # out
GPIO.output(RELAYGPIO, GPIO.HIGH) # on
