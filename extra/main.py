from camera import CameraController
from image_processing import Processing
import numpy as np

def main():
	# Create objects
	camera_controller = CameraController()
	image_processor = Processing()
	
	camera_controller.capture_image()
	
	raw_data = camera_controller.raw_data
	
	# ~ print(raw_data[0])
	
	# ~ print(raw_data.shape)
	# ~ print(raw_data)
	
	# ~ grayImage = image_processor.RGB_to_Gray(raw_data)
	
	# ~ image_processor.plotHistogram(grayImage)
	
	# ~ avgGray = image_processor.Average_Gray_Value(grayImage)
	
	
	

	

if __name__ == "__main__":
	main()
