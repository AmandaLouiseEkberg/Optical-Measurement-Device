from camera import CameraController
from image_processing import Processing
from GUIApplication import GUI_application
from textFile import textFileHandler
import tkinter as tk

def main():
	# Create objects
	camera_controller = CameraController()
	image_processor = Processing()
	
	camera_controller.capture_image()
	
	RGB_array = camera_controller.RGB_array
		
	grayImage = image_processor.RGB_to_Gray(RGB_array)
	
	# ~ image_processor.plotHistogram(grayImage)
	
	avgGray = image_processor.Average_Gray_Value(grayImage)
	
	fileHandler = textFileHandler('data.txt')	
	
	main_window = tk.Tk()
	app = GUI_application(main_window, avgGray, fileHandler) #add more entries here fo interaction with GUI
	main_window.mainloop()

	

if __name__ == "__main__":
	main()
