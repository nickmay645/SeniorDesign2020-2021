import time
import os
import RPi.GPIO as GPIO
import eeml
GPIO.setmode(GPIO.BCM)
DEBUG = 1
LOGGER = 1

GPIO.setup(2, GPIO.IN)
input = GPIO.input(0)

print(input)