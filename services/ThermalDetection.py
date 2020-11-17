from datetime import datetime
from picamera.array import PiRGBArray
from picamera import PiCamera
from datetime import datetime
from gpiozero import CPUTemperature
import time
import cv2
import pigpio
import os

"""
Main functionality:

Grab image from vis camera
check for faces
adjust position if needed


"""


class ThermalDetection:

    def __init__(self):
        """ Runs at the creation of the class object. """

        os.system("sudo pigpiod")

        # Define class variables
        self.start_time = datetime.now()
        self.pi = pigpio.pi()
        self.vis_camera = PiCamera()
        self.servo_vertical_value = 2300
        self.servo_horizontal_value = 1000
        self.servo_vertical_pin = 25
        self.servo_horizontal_pin = 27
        self.vis_horizontal_resolution = 640
        self.vis_vertical_resolution = 480
        self.vis_fps = 32
        self.vis_capture = None
        self.vis_frame = None

    def initializeCamera(self):
        """ Initializes the Pi Camera """

        self.vis_camera.resolution = (self.vis_horizontal_resolution, self.vis_vertical_resolution)
        self.vis_camera.frame_rate = self.vis_fps
        self.vis_capture = PiRGBArray(self.vis_camera,
                                      size=(self.vis_horizontal_resolution, self.vis_vertical_resolution))

    def initializeServos(self):
        """ Initializes the Tracking Servos """

        self.pi.set_servo_pulsewidth(self.servo_vertical_pin, self.servo_vertical_value)
        self.pi.set_servo_pulsewidth(self.servo_horizontal_pin, self.servo_horizontal_value)

    def captureVisFrame(self):
        """ Captures a frame from the visual camera """

        return self.vis_camera.capture(self.vis_capture, format="bgr", use_video_port=True)



    def run(self):
        """ Runs each step of system continuously """

        pass
