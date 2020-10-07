
import wiringpi

wiringpi.wiringPiSetupGpio()  # For GPIO pin numbering
wiringpi.pinMode(2, 1)       # Set pin 2 to 1 ( OUTPUT )
wiringpi.digitalWrite(2, 1)  # Write 1 ( HIGH ) to pin 2
wiringpi.digitalRead(2)      # Read pin 2 