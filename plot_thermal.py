import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from numpy import array

if __name__ == '__main__':

    f = open("text.txt", "r")
    a = f.read()
    a = a.replace("\n","").split(" ")
    for i in range(0, len(a)):
        a[i] = float(a[i])

    n = 160
    newList = [a[i:i + n] for i in range(0, len(a), n)]
    nArray = array(newList)
    print(nArray)

    a11 = nArray.reshape(120, 160)
    plt.imshow(a11, cmap='hot')
    plt.colorbar()
    plt.show()

