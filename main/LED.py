import RPi.GPIO as GPIO
import time



class LEDToggle:
    def __init__(self,toggle):

        GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers

        if toggle == 0:
            RELAYGPIO = 16
        else:
            RELAYGPIO = 20
        
        GPIO.setup(RELAYGPIO, GPIO.OUT) # GPIO Assign mode
        GPIO.output(RELAYGPIO, GPIO.HIGH) # on
        time.sleep(1)
        GPIO.output(RELAYGPIO, GPIO.LOW) # off
    