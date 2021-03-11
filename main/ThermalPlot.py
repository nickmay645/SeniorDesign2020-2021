import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib import animation
from numpy import array
import cv2

import LED
import Relay
import logging

class ThermalData:
    def __init__(self,x,y):

        self.thermalx = x + 7
        self.thermaly = y - 15
        

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

                tempvalue = a11[self.thermaly,self.thermalx] + 7

                return tempvalue
           
                

        def animate(self):
            a = getarray()
            if a is not None:
                im.set_data(a)
                return im

        
        
        
        # fig = plt.figure()
        self.data = getarray()
        # im = plt.imshow(self.data,cmap='hot')
        
        # anim = animation.FuncAnimation(fig,animate,interval=100)

        # plt.show()

        
        # a = getarray()
        # cv2.namedWindow("ThermalImage", cv2.WINDOW_AUTOSIZE)
        # cv2.imshow("ThermalImage", a.repeat(1, 0).repeat(1, 1))
        # cv2.waitKey(1)

        

        
        

