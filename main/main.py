#Import required modules
# from services import ThermalPlot, PiCam, LED, Relay
import PiCam, ThermalPlot

import os

if __name__ == "__main__":

    # os.chdir("/home/pi/FeverDetection/bin/main")
    # os.system("./main /dev/spidev0.0 /dev/i2c-1")



    


    instance = PiCam.RaspCam()
    instance2 = ThermalPlot.ThermalData(instance.thermalx,instance.thermaly)
    Relay.ToggleRelay(instance2.thermalpoint)
    
    

