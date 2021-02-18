import subprocess
import logging

class startthermal:
    def __init__(self):
        logging.info("Thermal Camera starting...")
        subprocess.call("cd /home/pi/Senior_Design/SeniorDesign2020-2021/bin/main && ./main /dev/spidev0.0 /dev/i2c-1",shell=True)