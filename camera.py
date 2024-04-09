# Camera class
from picamera2 import Picamera2, Preview
from time import sleep
import numpy as np
import cv2

class CameraController:
	# Camera initialization
	def __init__(self):
		# Initialize Picamera2 object
		self.picam2 = Picamera2()
				
		print("Camera config first:", self.picam2.sensor_modes)
		
		# Camera configuration: RAW 10-bit image
		self.camera_config = self.picam2.create_preview_configuration(raw={'unpacked':'SRGGB10','bit_depth':10})
		self.picam2.configure(self.camera_config)
		
		# ~ # Camera controls
		self.picam2.set_controls({"ExposureTime": 3000})
		
		print("Camera modes:", self.picam2.sensor_modes)
		
	# Capture image, save RGB and image
	def capture_image(self):
		self.picam2.start()
		sleep(2)
		
		self.picam2.capture_file("test.jpg")
		self.RGB_array = self.picam2.capture_array("main")
			
		# ~ self.picam2.close()
		print("Camera config after:", self.picam2.sensor_modes)
	
	#Capture RAW image	
	def capture_RAWimage(self):
		self.picam2.start()
		sleep(2)
		
		#Create raw array and save raw png image
		self.RAWimage = self.picam2.capture_array("raw").view(np.uint16) #RAWimage is used in other parts of the code, use same name if code is changed from 16 bits etc
		cv2.imwrite("raw.png", self.RAWimage)
		self.check = cv2.imread("raw.png", cv2.IMREAD_ANYDEPTH)
		# ~ self.picam2.close()

	
	def change_exposure(self, exposure_time):
		# Camera controls
		self.picam2.set_controls({"ExposureTime": exposure_time})
	
		

	
		
