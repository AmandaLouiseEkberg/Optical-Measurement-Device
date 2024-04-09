import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from PIL import Image, ImageTk

global maxGrayPixel_y, maxGrayPixel_x, radial_steps, azumuthial_steps, maxValue
radial_steps = 5 #Max steps
azumuthial_steps = 5 #Max steps

class GUI_application:
	def __init__(self, main_window, fileHandler, camera_controller, image_processor, calibration, measurement): #add more entries here for interactions
		self.master = main_window
		self.fileHandler = fileHandler
		# ~ self.avgGray = avgGray
		self.camera = camera_controller
		self.imageProcessing = image_processor
		self.calibration = calibration
		self.measurement = measurement
		
		#Design of window
		self.master.geometry("500x500+800+300")
		self.master.title("Optical Scattering Measurement Device")
		self.background_image = Image.open("afry.png")
		self.background_photo = ImageTk.PhotoImage(self.background_image)
		
		self.frames = {}
		self.current_frame = None
		
		for F in (self.FirstPage, self.StartPage, self.TestPage, self.collectingDataPage):
			frame = F()
			self.frames[F.__name__] = frame

		self.show_frame(self.FirstPage)
		
	def show_frame(self, F):
		if self.current_frame:
			self.current_frame.pack_forget()
			
		frame = self.frames[F.__name__]
		frame.pack(fill="both", expand=True)
		self.current_frame= frame
		
	def button_BRDF(self):
		messagebox.showinfo("Message", "BRDF measurement chosen")
		self.fileHandler.write_text_position(5, "ScatterType  BRDF\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
		
	def button_BTDF(self):
		messagebox.showinfo("Message", "BTDF measurement chosen")
		self.fileHandler.write_text_position(5, "ScatterType  BTDF\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
		
	def button_sampleRotations(self):
		messagebox.showinfo("Message", "Choose number of sample rotations (1 is entered now at 0 degrees)")
		self.fileHandler.write_text_position(6, "SampleRotation 1")
		self.fileHandler.write_text_position(7, "0")
		
	def button_angleOfIncidence(self):
		messagebox.showinfo("Message", "Choose number of angles of incidence (1 is entered now at 0 degrees)")
		self.fileHandler.write_text_position(8, "AngleOfIncidence 1")
		self.fileHandler.write_text_position(9, "0")
		
	def button_scatterAzimuth_1(self):
		messagebox.showinfo("Message", "Choose number of scatter azumuthial angles (1 is entered now at 0 degrees)")
		self.fileHandler.write_text_position(10, "ScatterAzimuth 1")
		self.fileHandler.write_text_position(11, "0")
		global azumuthial_steps
		azumuthial_steps = 1
		
	def button_scatterAzimuth_2(self):
		messagebox.showinfo("Message", "Choose number of scatter azumuthial angles (2 is entered now at 0  and 10 degrees)")
		self.fileHandler.write_text_position(10, "ScatterAzimuth 2")
		self.fileHandler.write_text_position(11, "0 10")
		global azumuthial_steps
		azumuthial_steps = 2
		
	def button_scatterRadial_1(self):
		messagebox.showinfo("Message", "Choose number of scatter radial angles (1 is entered now at 0 degrees)")
		self.fileHandler.write_text_position(12, "ScatterRadial 1")
		self.fileHandler.write_text_position(13, "0")
		global radial_steps
		radial_steps = 1
		
	def button_scatterRadial_2(self):
		messagebox.showinfo("Message", "Choose number of scatter radial angles (2 is entered now at 0 and 10 degrees)")
		self.fileHandler.write_text_position(12, "ScatterRadial 2")
		self.fileHandler.write_text_position(13, "0 10")
		global radial_steps
		radial_steps = 2
		
	def	button_monochrome(self):
		messagebox.showinfo("Message", "Monochrome measurement confirmed")
		self.fileHandler.write_text_position(14, "Monochrome")
		
	def	button_Begin(self):
		global radial_steps, azumuthial_steps, maxGrayPixel_y, maxGrayPixel_x
		messagebox.showinfo("Message", "Data acquisistion started")
		self.fileHandler.write_text_position(15, "DataBegin")
		# ~ BSDF_RAW_data[radial_steps, azumuthuial_steps] = []
		BSDF_RAW_data = [[0 for _ in range(radial_steps)]for _ in range(azumuthial_steps)]
		i = 0
		
		while i < radial_steps:
			# ~ self.camera.capture_image()
			# ~ RGB_array = self.camera.RGB_array
			# ~ grayImage = self.imageProcessing.RGB_to_Gray(RGB_array)
			# ~ grayValue = grayImage[maxGrayPixel_y, maxGrayPixel_x] #insert coordinates of calibrated pixel position
			BSDF_RAW_data[i][1] = (self.measurement.take_one_measurement(radial_steps, azumuthial_steps, maxGrayPixel_y, maxGrayPixel_x))
			print(BSDF_RAW_data[i][1])
			i  += 1
			
		print("loop ended")
		
		
	def take_picture_avgGray(self):
		# ~ self.camera.capture_image()
		# ~ grayImage = self.camera.RGB_array
		# ~ grayImage = self.imageProcessing.RGB_to_Gray(RGB_array)
		# ~ avgGray = self.imageProcessing.Average_Gray_Value(grayImage)
		# ~ print(grayImage.max())
		
		self.camera.capture_RAWimage()
		RAWimage = self.camera.RAWimage
		# ~ check = self.camera.check
		# ~ RAWimage = self.imageProcessing.RGB_to_Gray(RAW_array)
		avgRAW = self.imageProcessing.Average_Gray_Value(RAWimage)
		messagebox.showinfo("Message", f" Image taken\n\nHistogram will be displayed after this window is closed\n\nAverage Gray value is: {avgRAW}")
		hist = self.imageProcessing.plotHistogram(RAWimage)
		plt.plot(hist)
		plt.gca().yaxis.set_major_locator(plt.MaxNLocator(integer=True))
		plt.show()
		
		
	def button_Calibrate(self):
		global maxGrayPixel_y, maxGrayPixel_x, maxValue
		cameraController = self.camera
		# ~ RGB_array = self.camera.RGB_array
		# ~ grayImage = self.imageProcessing.RGB_to_Gray(RGB_array)
		# ~ hist = self.imageProcessing.plotHistogram(grayImage)
		# ~ global maxGrayPixel_y, maxGrayPixel_x
		# ~ maxGrayPixel_y, maxGrayPixel_x = self.imageProcessing.Max_GrayValue_Pixel(self.imageProcessing, self.camera)
		
		maxGrayPixel_y, maxGrayPixel_x, maxValue = self.calibration.blob_detection()
		messagebox.showinfo("Message", f" Image taken\n\nPixel Position is: y: {maxGrayPixel_y}, x: {maxGrayPixel_x}, max value is: {maxValue}")
		
	def FirstPage(self): #Button for Test and Start
		frame = tk.Frame(self.master, width = 300, height = 200)
		background_label = tk.Label(frame, image=self.background_photo)
		background_label.place(x=0, y=0, relwidth=1, relheight=1)
		
		label = tk.Label(frame, text="First Page")
		label.pack(pady=10, padx=10)
		
		buttonStart = tk.Button(frame, text="START", command=lambda: self.show_frame(self.StartPage), fg="white", font=("Helvetica", 12), bd=2, relief=tk.RAISED)	
		buttonStart.pack()
		
		buttonTest = tk.Button(frame, text="Camera TEST", command=lambda: self.show_frame(self.TestPage), fg="white", font=("Helvetica", 12), bd=2, relief=tk.RAISED)
		buttonTest.pack()
		
		button_Calibrate = tk.Button(frame, text="Calibrating", command = self.button_Calibrate, fg="white", font=("Helvetica", 12), bd=2, relief=tk.RAISED)
		button_Calibrate.pack(side='top')
		
		return frame
		
	def StartPage(self): #start material properties 
		frame = tk.Frame(self.master, width = 300, height = 200)
		background_label = tk.Label(frame, image=self.background_photo)
		background_label.place(x=0, y=0, relwidth=1, relheight=1)
		
		label = tk.Label(frame, text="Start Page")
		label.pack(pady=10, padx=10)
		
		# ~ self.create_widgets()	

		button_BRDF = tk.Button(frame, text="BRDF", command = self.button_BRDF, fg="white", font=("Helvetica", 12), bd=2, relief=tk.RAISED)
		button_BRDF.pack(side='top')
		
		button_BTDF = tk.Button(frame, text="BTDF", command = self.button_BTDF, fg="white", font=("Helvetica", 12), bd=2, relief=tk.RAISED)
		button_BTDF.pack(side='top')
		
		button_sampleRotations = tk.Button(frame, text="Sample Rotations", command = self.button_sampleRotations, fg="white", font=("Helvetica", 12), bd=2, relief=tk.RAISED)
		button_sampleRotations.pack(side='top')
		
		button_angleOfIncidence = tk.Button(frame, text="Angle of Incidences", command = self.button_angleOfIncidence, fg="white", font=("Helvetica", 12), bd=2, relief=tk.RAISED)
		button_angleOfIncidence.pack(side='top')
		
		button_scatterAzimuth1 = tk.Button(frame, text="Scatter Azimuth = 1", command = self.button_scatterAzimuth_1, fg="white", font=("Helvetica", 12), bd=2, relief=tk.RAISED)
		button_scatterAzimuth1.pack(side='top')
		
		button_scatterAzimuth2 = tk.Button(frame, text="Scatter Azimuth = 2", command = self.button_scatterAzimuth_1, fg="white", font=("Helvetica", 12), bd=2, relief=tk.RAISED)
		button_scatterAzimuth2.pack(side='top')
		
		button_scatterRadial1 = tk.Button(frame, text="Scatter Radial = 1", command = self.button_scatterRadial_1, fg="white", font=("Helvetica", 12), bd=2, relief=tk.RAISED)
		button_scatterRadial1.pack(side='top')
		
		button_scatterRadial2 = tk.Button(frame, text="Scatter Radial = 2", command = self.button_scatterRadial_2, fg="white", font=("Helvetica", 12), bd=2, relief=tk.RAISED)
		button_scatterRadial2.pack(side='top')
		
		button_monochrome = tk.Button(frame, text="confirm monochrome measurement", command = self.button_monochrome, fg="white", font=("Helvetica", 12), bd=2, relief=tk.RAISED)
		button_monochrome.pack(side='top')
		
		button_Begin = tk.Button(frame, text="Begin", command =lambda: self.show_frame(self.collectingDataPage), fg="white", font=("Helvetica", 12), bd=2, relief=tk.RAISED)
		button_Begin.pack(side='top')		
		
		buttonBack = tk.Button(frame, text="Back", command=lambda: self.show_frame(self.FirstPage), fg="white", font=("Helvetica", 12), bd=2, relief=tk.RAISED)
		buttonBack.pack(side='bottom')
		
		return frame
		
	def TestPage(self): #test and try the camera for RAW data
		frame = tk.Frame(self.master, width = 300, height = 200)
		background_label = tk.Label(frame, image=self.background_photo)
		background_label.place(x=0, y=0, relwidth=1, relheight=1)
		
		label = tk.Label(frame, text="Test Page")
		label.pack(pady=10, padx=10)
		
		buttonTakePic = tk.Button(frame, text="Take Picture", command= self.take_picture_avgGray, fg="white", font=("Helvetica", 12), bd=2, relief=tk.RAISED)
		buttonTakePic.pack()
		
		buttonBack = tk.Button(frame, text="Back", command=lambda: self.show_frame(self.FirstPage), fg="white", font=("Helvetica", 12), bd=2, relief=tk.RAISED)
		buttonBack.pack(side='bottom')
		
		return frame
		
	def collectingDataPage(self):
		frame = tk.Frame(self.master, width = 300, height = 200)
		background_label = tk.Label(frame, image=self.background_photo)
		background_label.place(x=0, y=0, relwidth=1, relheight=1)		
		
		label = tk.Label(frame, text="Data acquisistion")
		label.pack(pady=10, padx=10)	
		
		button_Begin = tk.Button(frame, text="Begin", command = self.button_Begin, fg="white", font=("Helvetica", 12), bd=2, relief=tk.RAISED)
		button_Begin.pack()		
		
		
		#Display graph of measurment data as it is collected
		#STOP button 
		buttonSTOP = tk.Button(frame, text="STOP", command=lambda: self.show_frame(self.TestPage), fg="white", font=("Helvetica", 12), bd=2, relief=tk.RAISED)
		buttonSTOP.pack(side='bottom') #Make correct stop command!
		
		return frame
		
	def run(self):
		self.master.mainloop()
		
	

		
		

