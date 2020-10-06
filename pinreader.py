

import RPi.GPIO as GPIO           # Allows us to call our GPIO pins and names it just GPIO
 
GPIO.setmode(GPIO.BCM)           # Set's GPIO pins to BCM GPIO numbering
INPUT_PIN = 9           #Video Over SPI Slave Data Out
GPIO.setup(INPUT_PIN, GPIO.IN)           # Set our input pin to be an input

counter = 0

# Start a loop that never ends
while True: 
    print(GPIO.input(INPUT_PIN),end='')
    counter = counter + 1
    if counter == 16:
        counter = 0
        print("/n")
