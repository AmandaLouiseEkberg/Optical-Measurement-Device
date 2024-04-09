import cv2
global blobIntenisty
blobIntenisty = 65000 

class calibrationHandler:
	def __init__(self, cameraController):
		self.camera = cameraController
	#Move to specific place : specular reflection for calibration
	
	#Dark noise calib - no lightsource
	def dark_noise_calib(self):
		print("take pic, save all 'gray values' for the pixels, maybe only chosen middle pixels need to be saved and removed form signal.")
	
	
	# Capture image and find blob center
	def blob_detection(self):
		global blobIntenisty
		self.camera.capture_RAWimage()
		RAWimage = self.camera.RAWimage
		im = cv2.imread("1blob.jpg", cv2.IMREAD_GRAYSCALE) #read raw.png instead
		parameters = cv2.SimpleBlobDetector_Params()
		parameters.blobColor = blobIntenisty
		parameters.filterByArea = False
		detector = cv2.SimpleBlobDetector_create(parameters)
		keypoints = detector.detect(im)
		print("nr of blobs:" , len(keypoints))
		for kp in keypoints:
			y_pixel, x_pixel = kp.pt
			print(kp.pt, kp.size)
		
		return y_pixel, x_pixel, RAWimage[round(y_pixel), round(x_pixel)]
