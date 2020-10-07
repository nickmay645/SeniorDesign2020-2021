
import wiringpi

wiringpi.pinMode(2, 1)       # Set pin 6 to 1 ( OUTPUT )
wiringpi.digitalWrite(2, 1)  # Write 1 ( HIGH ) to pin 6
wiringpi.digitalRead(2)      # Read pin 6