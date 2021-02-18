import RPi.GPIO as GPIO
import time



class RelayToggle:
    def __init__(self):

        GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers

        RELAYGPIO = 27

        GPIO.setup(RELAYGPIO, GPIO.OUT) # GPIO Assign mode
        GPIO.output(RELAYGPIO, GPIO.HIGH) # on
        time.sleep(1)
        GPIO.output(RELAYGPIO, GPIO.LOW) # off