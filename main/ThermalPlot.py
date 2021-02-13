import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib import animation
from numpy import array

import LED

class ThermalData:
    def __init__(self,x,y):
        
        self.thermalx = x
        self.thermaly = y

        def getarray():
            
            f = open("output.txt", "r")
            a = f.read()
            a = a.replace("\n","").split(" ")
            if len(a) == 19201 and a is not None:
                for i in range(0, len(a)-1):
                    a[i] = float(a[i])
                n = 160
                newList = [a[i:i + n] for i in range(0, len(a)-1, n)]
                nArray = array(newList,dtype='float')
                a11 = nArray.reshape(120, 160)
                
                thermalvalue = a11[self.thermalx,self.thermaly]
                print(thermalvalue)
                if thermalvalue > 70.00: #temp value (replace when position is callibrated)
                    LED.LEDToggle(1) #toggles green LED
                else:
                    LED.LEDToggle(0) #toggles red LED

        
                return a11

        def animate(self):
            a = getarray()
            if a is not None:
                im.set_data(a)
                return im


        
        fig = plt.figure()
        data = getarray()
        # im = plt.imshow(data,cmap='inferno')
        
        # anim = animation.FuncAnimation(fig,animate)

        # plt.show()

        

        
        

