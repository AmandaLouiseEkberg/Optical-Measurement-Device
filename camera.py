# Camera class
from picamera2 import Picamera2, Preview
from time import sleep

class CameraController:
	# Camera initialization
	def __init__(self):
		# Initialize Picamera2 object
		self.picam2 = Picamera2()
		
		# Configurate to preview and RGB888
		camera_config = self.picam2.create_preview_configuration({'format' : 'RGB888'})
		self.picam2.configure(camera_config)
		
		# Camera controls
		self.picam2.set_controls({"ExposureTime": 3000})
		
	# Capture image and create RGB_array attribute
	def capture_image(self):
		self.picam2.start()
		sleep(2)
		self.RGB_array = self.picam2.capture_array("main")
		self.picam2.close()
	
	
		
