from PyQt5.QtCore import Qt
from PyQt5.QtCore import QTimer, QPoint, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QLabel
from PyQt5.QtWidgets import QWidget, QAction, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QFont, QPainter, QImage, QTextCursor
import ThermalPlot,Relay,LED
import sys, time, threading, cv2
import queue as Queue
import startcam
import math

VERSION = "Automated COVID-19 Temperature Sensor"

IMG_SIZE    = 640,480          # 640,480 or 1280,720 or 1920,1080
IMG_FORMAT  = QImage.Format_RGB888
DISP_SCALE  = 1                # Scaling factor for display image
DISP_MSEC   = 50                # Delay between display cycles
CAP_API     = cv2.CAP_ANY       # API: CAP_ANY or CAP_DSHOW etc...
EXPOSURE    = 0                 # Zero for automatic exposure
TEXT_FONT   = QFont("Courier", 18)

camera_num  = 1                 # Default camera (first in list)
image_queue = Queue.Queue()     # Queue to hold images
capturing   = True              # Flag to indicate capturing
FaceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')



# Grab images from the camera (separate thread)
def grab_images(cam_num, queue,input):
    if input == 0:
        cap = cv2.VideoCapture(cam_num-1 + CAP_API)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, IMG_SIZE[0])
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, IMG_SIZE[1])
        
        while capturing:
            if cap.grab():
                retval, image = cap.retrieve(0)
                if image is not None and queue.qsize() < 2:
                    queue.put(image)
                else:
                    time.sleep(DISP_MSEC / 1000.0)
            else:
                print("Error: can't grab camera image")
                break
        cap.release()
    elif input == 1:
        startcam.startthermal()

# Image widget
class ImageWidget(QWidget):
    def __init__(self, parent=None):
        super(ImageWidget, self).__init__(parent)
        self.image = None
        self.toggle = False

    def setImage(self, image):
        self.image = image
        self.setMinimumSize(image.size())
        self.update()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        if self.image:
            qp.drawImage(QPoint(0, 0), self.image)
        qp.end()

# Main window
class MyWindow(QMainWindow):
    text_update = pyqtSignal(str)

    # Create main window
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.central = QWidget(self)
        self.toggle = False

        sys.stdout = self

        self.vlayout = QVBoxLayout()        # Window layout
        self.displays = QHBoxLayout()
        self.disp = ImageWidget(self)    
        self.displays.addWidget(self.disp)
        self.vlayout.addLayout(self.displays)
        self.label1 = QLabel("Forehead Temperature",self)
        self.label2 = QLabel("N/A",self)
        self.label3 = QLabel("Door Status",self)
        self.label4 = QLabel("N/A",self)

        self.vlayout.addWidget(self.label1)
        self.vlayout.addWidget(self.label2)
        self.vlayout.addWidget(self.label3)
        self.vlayout.addWidget(self.label4)
        
        self.central.setLayout(self.vlayout)
        self.setCentralWidget(self.central)

        self.mainMenu = self.menuBar()      # Menu bar
        exitAction = QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(self.close)
        self.fileMenu = self.mainMenu.addMenu('&File')
        self.fileMenu.addAction(exitAction)

    # Start image capture & display
    def start(self):
        
        self.timer1 = QTimer(self)           # Timer to trigger display.
        self.timer1.timeout.connect(lambda: 
                    self.show_image(image_queue, self.disp, DISP_SCALE))
        self.timer1.start(DISP_MSEC)
        for index in range(2):    
            self.capture_thread = threading.Thread(target=grab_images, 
                        args=(camera_num, image_queue, index))
            self.capture_thread.start()         
        

    # Fetch camera image from queue, and display it
    def show_image(self, imageq, display, scale):
        if not imageq.empty():
            image = imageq.get()
            if image is not None and len(image) > 0:
                img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                faces = FaceCascade.detectMultiScale(img,1.1,10)
                for (x,y,w,h) in faces:
                    self.toggle = True
                    self.thermalx = math.floor((x + (w/2))/4)
                    self.thermaly = math.floor((y + (h/4))/4)
                    cv2.rectangle(img,(self.thermalx*4,self.thermaly*4),(self.thermalx*4+1,self.thermaly*4+1),(255,0.255),2)
                    instance = ThermalPlot.ThermalData(self.thermalx,self.thermaly)
                    if instance.data != None:
                        self.label2.setText(str(instance.data)+"°F")
                        if instance.data > 70.0:
                            self.label4.setText("Unlocked")
                            Relay.RelayToggle()
                            self.label4.setText("Locked")
                self.label2.setText("N/A")
                            
                self.display_image(img, display, scale)

    # Display an image, reduce size if required
    def display_image(self, img, display, scale=1):
        disp_size = img.shape[1]//scale, img.shape[0]//scale
        disp_bpl = disp_size[0] * 3
        if scale > 1:
            img = cv2.resize(img, disp_size, 
                             interpolation=cv2.INTER_CUBIC)
        qimg = QImage(img.data, disp_size[0], disp_size[1], 
                      disp_bpl, IMG_FORMAT)
        display.setImage(qimg)

    # Window is closing: stop video capture
    def closeEvent(self, event):
        global capturing
        capturing = False
        self.capture_thread.join()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        try:
            camera_num = int(sys.argv[1])
        except:
            camera_num = 0
    if camera_num < 1:
        print("Invalid camera number '%s'" % sys.argv[1])
    else:
        app = QApplication(sys.argv)
        win = MyWindow()
        win.show()
        win.setWindowTitle(VERSION)
        win.start()
        sys.exit(app.exec_())





    
    
    
    

