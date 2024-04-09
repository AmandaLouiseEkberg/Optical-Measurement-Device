from camera import CameraController
import cv2
import numpy as np
import matplotlib.pyplot as plt


class Processing:
	def __init__(self):
		pass
		
	def RGB_to_Gray(self, image):
		grayImage = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
		return grayImage
		
	def plotHistogram(self, grayImage):
		histogram = cv2.calcHist([grayImage], [0], None, [65536], [0, 65536])
		# ~ plt.plot(histogram)
		# ~ plt.show()
		return histogram
		
	def Average_Gray_Value(self, grayImage):
		avg_gray_value = np.average(grayImage)
		return round(avg_gray_value, 3)
		
		#Calculate Total integrated scatter, return to file at row 16 "TIS 0.134506"
		
	# ~ def Max_GrayValue_Pixel(self, image_processing, camera_controller): #FIX if the exposure needs to increase as well. 
		# ~ exposure_time = 3000
		# ~ #take image and retrieve gray values
		# ~ camera_controller.capture_image()
		# ~ RGB_array = camera_controller.RGB_array
		# ~ grayImage = image_processing.RGB_to_Gray(RGB_array)
		# ~ calibrationComplete = False
		
		# ~ hist = image_processing.plotHistogram(grayImage)
		
		# ~ while (calibrationComplete == False):
		
			# ~ #retrieve max gray values and positions, we want brightest_pixels == 2 
			# ~ max_grayValue = grayImage.max()
			# ~ brightest_pixels = hist[max_grayValue]
				
			# ~ print("nr of pixels", brightest_pixels)
			# ~ print("max gray value:", max_grayValue)
			
			# ~ #check if there is more than 1 pixel with same max gray value, we want gray value 255, one pixel, at repeat of 3 times, position at these locations. 
			# ~ while not(brightest_pixels == 1) :
				# ~ exposure_time = exposure_time - 10
				# ~ camera_controller.change_exposure(exposure_time)
				# ~ #take image and retrieve gray values
				# ~ camera_controller.capture_image()
				# ~ RGB_array = camera_controller.RGB_array
				# ~ grayImage = image_processing.RGB_to_Gray(RGB_array)
				# ~ hist = image_processing.plotHistogram(grayImage)
				# ~ #retrieve max gray values and positions, we want brightest_pixels == 2 
				# ~ max_grayValue = grayImage.max()
				# ~ brightest_pixels = hist[max_grayValue]
				# ~ print("exposure time:", exposure_time)
				# ~ print("nr of pixels:", brightest_pixels)
				# ~ print("max gray value:", max_grayValue)
				
				# ~ if (max_grayValue < 900):
					# ~ exposure_time = exposure_time + 100
					# ~ brightest_pixels = 100
				# ~ else: 
					# ~ calibrationComplete = True
			
			
				
			# ~ flattened_image = grayImage.flatten()
			# ~ max_grayValue_pixel = np.argmax(flattened_image)
			# ~ pixel_y, pixel_x = np.unravel_index(max_grayValue_pixel, grayImage.shape)
			
			
			
			
