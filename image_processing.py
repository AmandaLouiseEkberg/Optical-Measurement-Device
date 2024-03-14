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
		histogram = cv2.calcHist([grayImage], [0], None, [256], [0, 256])
		plt.plot(histogram)
		plt.show()
		
	def Average_Gray_Value(self, grayImage):
		avg_gray_value = np.average(grayImage)
		return avg_gray_value
		
		
		

