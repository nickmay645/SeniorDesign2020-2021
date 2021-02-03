import RPi.GPIO as GPIO
import time



class ToggleRelay:
    def __init__(self,data):
        self.value = data
        # GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers
        # RELAYGPIO = 17
        # GPIO.setup(RELAYGPIO, GPIO.OUT) # GPIO Assign mode
        # GPIO.output(RELAYGPIO, GPIO.LOW) # out
        print("Relay Not Toggled")

        if self.value <= 98.99:
            # GPIO.output(RELAYGPIO, GPIO.HIGH) # on
            # time.sleep(5)
            # GPIO.output(RELAYGPIO, GPIO.LOW) # out
            print("Relay Toggled")
        