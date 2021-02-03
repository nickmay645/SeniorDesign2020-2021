import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib import animation
from numpy import array

import math

from PiCamera import thermalx
from PiCamera import thermaly

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

        print(a11(thermalx,thermaly),end='\r')
        print(thermalx,end='\r')
        print(thermaly,end='\r')

        return a11

def animate(self):
    a = getarray()
    if a is not None:
        im.set_data(a)
        return im


if __name__ == '__main__':
    fig = plt.figure()
    data = getarray()
    im = plt.imshow(data,cmap='hot')
    
    anim = animation.FuncAnimation(fig,animate)

    plt.show()

    
    

