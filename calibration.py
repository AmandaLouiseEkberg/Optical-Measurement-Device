import cv2
global blobIntenisty
import numpy as np
global diameter, x_pixel, y_pixel

blobIntenisty = 2

class calibrationHandler:
	def __init__(self, cameraController):
		self.camera = cameraController
	#Move to specific place : specular reflection for calibration	
	
	# Capture image and find blob center
	def blob_detection(self):
		global blobIntenisty
		
		#Take a picture and save as rawNormIm.jpg
		self.camera.capture_RAWimage()
		
		#Read the image and find blob center and size
		im = cv2.imread("exposure_calibration.jpg", cv2.IMREAD_GRAYSCALE) #reading realtime image 
		# ~ im = cv2.imread("homogenitet_bild_test.png", cv2.IMREAD_GRAYSCALE) #reading prepared image
		parameters = cv2.SimpleBlobDetector_Params()
		# ~ parameters.minRepeatability = 1
		parameters.minThreshold = 252
		parameters.maxThreshold = 255
		parameters.filterByConvexity = False
		parameters.filterByInertia = False
		parameters.minRepeatability = 1
		parameters.filterByColor = False
		parameters.filterByArea = True
		parameters.minArea = 8
		parameters.maxArea = 180
		parameters.filterByCircularity = False
		parameters.minCircularity = 0.9
		detector = cv2.SimpleBlobDetector_create(parameters)
		self.keypoints = detector.detect(im)
		
		print("nr of blobs:" , len(self.keypoints))
		for kp in self.keypoints:
			self.y_pixel, self.x_pixel = kp.pt
			self.diameter = kp.size
			print(kp.pt, kp.size)
			
		# Draw red circle around blob
		# ~ blank = np.zeros((1,1))
		# ~ blobs = cv2.drawKeypoints(im, (self.keypoints), blank, (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
		# ~ cv2.imshow("Blobs", blobs)
		# ~ cv2.waitKey(0)
		# ~ cv2.destroyAllWindows()
		
		#return coordinates of blob center and diameter
		return self.y_pixel, self.x_pixel, self.diameter

	def pixels_in_circle(self, image):
		radius = round(self.diameter*1) / 2 #GABRIEL
		
		a = round(self.y_pixel)
		b = round(self.x_pixel)
		pixel_image = image
		
		x = np.arange(pixel_image.shape[1])
		y = np.arange(pixel_image.shape[0])
		
		xx, yy = np.meshgrid(x, y)
		
		circle_mask = ((xx - a)**2 + (yy - b)**2) <= radius**2
		
		return pixel_image[circle_mask]
