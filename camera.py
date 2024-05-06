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
				
		# ~ print("Camera config first:", self.picam2.camera_configuration())
		
		# Camera configuration: RAW 10-bit image
		self.camera_config = self.picam2.create_still_configuration(raw={'format':'SBGGR10'})
		self.picam2.configure(self.camera_config)
		
		# ~ # Camera controls
		self.setExposure = 50
		self.picam2.set_controls({"ExposureTime": self.setExposure})
		
		# ~ print("Camera modes:", self.picam2.sensor_modes)
		
	# Capture image, save RGB and image
	def capture_image(self):
		self.picam2.start()
		sleep(2)
		
		self.picam2.capture_file("test.jpg")
		self.RGB_array = self.picam2.capture_array("main")
			
		# ~ self.picam2.close()
		# ~ print("Camera config after:", self.picam2.camera_configuration())
	
	#Capture RAW image	
	def capture_RAWimage(self):
		self.picam2.start()
		sleep(2)
		
		#Create raw array and save raw png image
		self.RAWimage = self.picam2.capture_array("raw").view(np.uint16) #RAWimage is used in other parts of the code, use same name if code is changed from 16 bits etc
		# ~ normalized_image = cv2.normalize(self.RAWimage, None, alpha = 0, beta = 255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
		normalized_image = self.RAWimage /  4
		cv2.imwrite("Amanda_blob_test.jpg", normalized_image)
		
		#Save text file of RAW data array for analysis
		# ~ np.savetxt("beamprofile_RAWtext_test.txt", self.RAWimage,  fmt="%d")
		
		#Use only red pixels in image - for homogenioty tests
		# ~ self.img = self.RAWimage[1::2, 1::2] #red channel
		# ~ normalized_img = cv2.normalize(self.img, None, alpha = 0, beta = 255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
		# ~ cv2.imwrite("beamprofile_onlyBlue_test.jpg", normalized_img)
		# ~ self.check = cv2.imread("raw.png", cv2.IMREAD_ANYDEPTH)
		print("capture RAW image funct")
		# ~ self.picam2.close()
		
	def capture_Noiseimage(self):
		
		#TURN OFF LIGHTSOURCE 
		
		self.picam2.start()
		sleep(2)
		
		#Create raw array and save raw png image
		self.NOISEimage = self.picam2.capture_array("raw").view(np.uint16) #RAWimage is used in other parts of the code, use same name if code is changed from 16 bits etc
		# ~ self.NOISEimage = self.NOISEimage[0::2, 0::2] #blue channel
		cv2.imwrite("raw_noise.jpg", self.NOISEimage)
		# ~ self.check = cv2.imread("raw.png", cv2.IMREAD_ANYDEPTH)
		print("capture noise function")
		# ~ self.picam2.close()
		

	
	def change_exposure(self, exposure_time):
		# Camera controls
		self.setExposure = exposure_time
		self.picam2.set_controls({"ExposureTime": self.setExposure})
	
		
