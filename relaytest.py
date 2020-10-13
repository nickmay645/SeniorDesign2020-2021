import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers
 
RELAYGPIO = 25
GPIO.setup(RELAYGPIO, GPIO.OUT) # GPIO Assign mode
GPIO.output(RELAYGPIO, GPIO.LOW) # out
GPIO.output(RELAYGPIO, GPIO.HIGH) # on
