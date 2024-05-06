

class measurementHandler:
	def __init__(self, camera_controller):
		self.camera = camera_controller
		
	def exposure_check(self):
		print("take pic, check exposure to modell, change exposure, check again til ok")

	def take_one_measurement(self, radial_steps, azumuthial_steps, maxGrayPixel_y, maxGrayPixel_x):
		self.camera.capture_RAWimage()
		self.image = self.camera.RAWimage
		return self.image[round(maxGrayPixel_y), round(maxGrayPixel_x)]
