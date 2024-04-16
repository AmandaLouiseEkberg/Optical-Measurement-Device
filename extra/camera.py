# Camera class
from picamera2 import Picamera2, Preview, SensorFormat
from time import sleep
import numpy as np

class CameraController:
	
	
	# Camera initialization
	def __init__(self):
		# Initialize Picamera2 object
		
		exposure_time = 3000
		self.picam2 = Picamera2()
		
		self.raw_format = SensorFormat(self.picam2.sensor_format)
		self.raw_format.packing = None
		self.raw_format.bit_depth = 10
		
		# Camera configuration: RAW 10-bit image
		# ~ self.camera_config = self.picam2.create_still_configuration(raw={'format':'SRGGB10_CSI2P','unpacked':'SRGGB10','bit_depth':10})
		# ~ self.camera_config = self.picam2.create_still_configuration(raw={'format' : 'SRGGB10', 'size' : self.picam2.sensor_resolution})
		# ~ self.camera_config = self.picam2.create_still_configuration(raw={'size' : self.picam2.sensor_resolution})
		
		self.camera_config = self.picam2.create_still_configuration(raw = {'format' : self.raw_format}, buffer_count = 2)
		self.picam2.configure(self.camera_config)
		
		
		
		# Camera controls
		self.picam2.set_controls({"ExposureTime": exposure_time, "AnalogueGain" : 1.0})
		
		# ~ print("Camera specs:", self.picam2.sensor_modes)
		
	# Capture image and create RGB_array attribute
	def capture_image(self):
		self.picam2.start()
		sleep(2)
		self.raw_data = self.picam2.capture_array("raw").view(np.uint16)
		self.metadata = self.picam2.capture_metadata()		
		print(self.raw_data.shape)
		
		print(self.raw_data)
		print(self.raw_format)
		
		# ~ self.raw_data2 = self.raw_data1.view(np.uint16)
		
		# ~ self.request = self.picam2.capture_request()
		# ~ self.raw_buffer = self.request.make_buffer("raw")
		
		# ~ self.request.release()
		
		self.picam2.close()
		
	
	
	
		
