from datetime import datetime
from picamera.array import PiRGBArray
from picamera import PiCamera
from datetime import datetime
from gpiozero import CPUTemperature
import time
import cv2
import pigpio
import os
import sys
from os import path
from numpy import array

"""
Main functionality:

Grab image from vis camera
check for faces
adjust position if needed


"""


class ThermalDetection(object):

    def __init__(self):
        """ Runs at the creation of the class object. """

        resp = os.system("sudo pigpiod")
        print("`sudo pigpiod` ran with exit code %d" % resp)

        # Define Class Variables
        self.start_time = datetime.now()
        self.pi = pigpio.pi()
        self.vis_camera = PiCamera()

        # Servo Variables
        self.servo_vertical_value = 2300
        self.servo_horizontal_value = 1000
        self.servo_vertical_pin = 25
        self.servo_horizontal_pin = 27

        # Vis Camera Variables
        self.vis_horizontal_resolution = 640
        self.vis_vertical_resolution = 480
        self.vis_fps = 32
        self.vis_capture = None
        self.vis_frame = None
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

        # Thermal Variables
        # self.fever_count = 0
        # self.non_fever_count = 0
        # self.get_data_flag = True
        # self.count_threshold = 5
        # self.temp_threshold = 100.00

    def initialize_vis_camera(self):
        """ Initializes the Pi Camera """

        self.vis_camera.resolution = (self.vis_horizontal_resolution, self.vis_vertical_resolution)
        self.vis_camera.frame_rate = self.vis_fps
        self.vis_capture = PiRGBArray(self.vis_camera,
                                      size=(self.vis_horizontal_resolution, self.vis_vertical_resolution))

    @staticmethod
    def initialize_thermal_camera():

        file_path = "ThermalRead/leptonic/bin/examples"
        resp = os.system("cd %s" % file_path)
        print("`cd %s` ran with exit code %d" % (file_path, resp))

        run_command = "./telemetry /dev/spidev0.0 /dev/i2c-1"
        resp = os.system(run_command)
        print("`%s` ran with exit code %d" % (run_command, resp))

    def initialize_servos(self):
        """ Initializes the Tracking Servos """

        self.pi.set_servo_pulsewidth(self.servo_vertical_pin, self.servo_vertical_value)
        self.pi.set_servo_pulsewidth(self.servo_horizontal_pin, self.servo_horizontal_value)

    def capture_vis_frame(self):
        """ Captures a frame from the visual camera """

        return self.vis_camera.capture(self.vis_capture, format="bgr", use_video_port=True)

    def capture_thermal_frame(self):
        """ Gets the thermal data from the IR camera """
        # TODO Define Text Path Variable at class init
        file = open("text.txt", "r")
        raw_data = file.read()
        list_data = raw_data.replace("\n", "").split(" ")
        for i in range(0, len(list_data)):
            if list_data[i] != "" or list_data[i] != " ":
                list_data[i] = float(list_data[i])

        size = 160
        new_list_data = [list_data[i:i + size] for i in range(0, len(list_data), size)]
        array_data = array(new_list_data)
        print(array)
        reshaped_array = array_data.reshape(120, 160)
        file.close()
        return reshaped_array

    def check_for_faces(self, frame):
        """ """
        image = frame.array
        img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(img_gray, 1.1, 10)
        pass

    def run(self):
        """ Runs each step of system continuously

        1 Clock Cycle
            Step 1. Capture frame from visual camera
            Step 2. Capture frame from thermal camera
            Step 3. Check for face
            Step 4. Get thermal data from face location
            Step 5. Check Thermal to update led, speaker, and door
            Step 6. Check if servos need to be adjusted.

        """

        vis_frame = self.capture_vis_frame()
        thermal_frame = self.capture_thermal_frame()
        self.check_for_faces(vis_frame)

        pass
