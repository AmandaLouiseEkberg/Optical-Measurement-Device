import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import darkdetect
import customtkinter
import numpy as np
from PIL import Image, ImageTk
import cv2

global blobCenter_y, blobCenter_x, radial_steps, azumuthial_steps, NOISEimage, totIncidentLight, maxMeanGray, minMeanGray
radial_steps = 1 #Max steps
azumuthial_steps = 1 #Max steps
blobCenter_y = 300
blobCenter_x = 600
maxMeanGray = 1024
minMeanGray = 980

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")
		

class GUI_application(customtkinter.CTk):
	def __init__(self, fileHandler, camera_controller, image_processor, calibration, measurement): #add more entries here for interactions
		
		self.customtkinter = customtkinter.CTk()
		self.customtkinter.geometry(f"{750}x{580}")
		self.customtkinter.title("Optical Scattering Measurement Device")

        # ~ # configure grid layout (4x4)
		self.customtkinter.grid_columnconfigure(1, weight=1)
		self.customtkinter.grid_columnconfigure((2, 3), weight=0)
		self.customtkinter.grid_rowconfigure((0, 1, 2), weight=1)
		
		self.master = self.customtkinter
		self.fileHandler = fileHandler
		# ~ self.avgGray = avgGray
		self.camera = camera_controller
		self.imageProcessing = image_processor
		self.calibration = calibration
		self.measurement = measurement
		
		#Design of window
		# ~ self.master.geometry("500x500+800+300")
		# ~ self.master.title("Optical Scattering Measurement Device")
		# ~ self.background_image = Image.open("afry.png")
		# ~ self.background_photo = ImageTk.PhotoImage(self.background_image)

		
		self.frames = {}
		self.current_frame = None
		
		for F in (self.FirstPage, self.StartPage, self.TestPage, self.collectingDataPage):
			frame = F()
			self.frames[F.__name__] = frame

		
		self.show_frame(self.FirstPage)
		
	def show_frame(self, F):
		# ~ if self.current_frame:
			# ~ self.current_frame.grid_forget()
			
		frame = self.frames[F.__name__]
		frame.tkraise()
		self.current_frame= frame
		
	def show_frame_str(self, F: str):
		# ~ if self.current_frame:
			# ~ self.current_frame.grid_forget()
			
		frame = self.frames[F]
		frame.tkraise()
		self.current_frame= frame
		
	def button_BRDF(self):
		messagebox.showinfo("Message", "BRDF measurement chosen")
		self.fileHandler.write_text_position(6, "ScatterType  BRDF")
		
	def button_BTDF(self):
		messagebox.showinfo("Message", "BTDF measurement chosen")
		self.fileHandler.write_text_position(6, "ScatterType  BTDF")
		
	def button_sampleRotations_1(self):
		self.fileHandler.write_text_position(7, "SampleRotations")
		self.fileHandler.write_text_position(8, "1")
		
	def button_angleOfIncidence(self):
		messagebox.showinfo("Message", "Choose number of angles of incidence (1 is entered now at 45 degrees)")
		self.fileHandler.write_text_position(9, "AngleOfIncidence 1")
		self.fileHandler.write_text_position(10, "45")
		
	def button_scatterAzimuth_1(self):
		messagebox.showinfo("Message", "Choose number of scatter azumuthial angles (1 is entered now at 0 degrees)")
		self.fileHandler.write_text_position(11, "ScatterAzimuth 1")
		self.fileHandler.write_text_position(12, "0")
		global azumuthial_steps
		azumuthial_steps = 1
		
	def button_scatterAzimuth_2(self):
		messagebox.showinfo("Message", "Choose number of scatter azumuthial angles (2 is entered now at 0  and 90 degrees)")
		self.fileHandler.write_text_position(11, "ScatterAzimuth 2")
		self.fileHandler.write_text_position(12, "0 90")
		global azumuthial_steps
		azumuthial_steps = 2
		
	def button_scatterAzimuth_3(self):
		messagebox.showinfo("Message", "Choose number of scatter azumuthial angles (3 is entered now at 0 , 45, 90 degrees)")
		self.fileHandler.write_text_position(11, "ScatterAzimuth 3")
		self.fileHandler.write_text_position(12, "0 45 90")
		global azumuthial_steps
		azumuthial_steps = 3
		
	def button_scatterRadial_1(self):
		messagebox.showinfo("Message", "Choose number of scatter radial angles (1 is entered now at 0 degrees)")
		self.fileHandler.write_text_position(13, "ScatterRadial 1")
		self.fileHandler.write_text_position(14, "0")
		global radial_steps
		radial_steps = 1
		
	def button_scatterRadial_2(self):
		messagebox.showinfo("Message", "Choose number of scatter radial angles (2 is entered now at 0 and 10 degrees)")
		self.fileHandler.write_text_position(13, "ScatterRadial 2")
		self.fileHandler.write_text_position(14, "0 10")
		global radial_steps
		radial_steps = 2
		
	def button_scatterRadial_3(self):
		messagebox.showinfo("Message", "Choose number of scatter radial angles (3 is entered now at 0, 10, 20 degrees)")
		self.fileHandler.write_text_position(13, "ScatterRadial 2")
		self.fileHandler.write_text_position(14, "0 10 20")
		global radial_steps
		radial_steps = 3
		
	def	button_monochrome(self):
		messagebox.showinfo("Message", "Monochrome measurement confirmed")
		self.fileHandler.write_text_position(15, "Monochrome")
		
	def button_writeInfo(self, entry):
		text = "#" + f"{entry.get()}"
		print("text:", text)
		self.fileHandler.write_text_position(2, text)
		
	def	button_Begin(self):
		global radial_steps, azumuthial_steps, blobCenter_y, blobCenter_x, NOISEimage, totIncidentLight
		messagebox.showinfo("Message", "Data acquisistion started")
		self.fileHandler.write_text_position(16, "DataBegin")
		self.fileHandler.write_text_position(17, "TIS -num-") #CALCULATE AND ADD TIS VALUE
		
		#Create empty array for data storage
		# ~ BSDF_RAW_data[radial_steps, azumuthuial_steps] = []
		BSDF_RAW_data = [[0 for _ in range(radial_steps)]for _ in range(azumuthial_steps)]
		i = 0
		w = 0
		
		#The file is written as ---->
		#						---->
		#						---->
		# the 'blob' of light that is used to get data is retrieved at button_calibrate. It also saves black noise which is removed in this step, before data is saved. 
		while i < azumuthial_steps:
						
			while w < radial_steps:
				self.camera.capture_RAWimage()
				circular_img = self.calibration.pixels_in_circle(self.camera.RAWimage)
				# ~ messagebox.showinfo("Message w", f" Image taken\n\nmean: {round(np.mean(circular_img), 3)}, stddev: {round(np.std(circular_img), 3)}, stddev/mean = {round(np.std(circular_img)/np.mean(circular_img), 3)}")
				print("data without noise and before exposure adjusting : ", round(np.mean(circular_img) - NOISEimage, 4))
				
				#if the mean value is too low/high we need to change exposure in this step and retake image. Then adjust the data with our model y=kx+m, so that the data is comparable to our calibrated 100% data
				while round(np.mean(circular_img) - NOISEimage, 4) > maxMeanGray :
					self.camera.change_exposure(self.camera.setExposure - 50)
					print("lower exposure, new value : ", self.camera.setExposure)
					self.camera.capture_RAWimage()
					circular_img = self.calibration.pixels_in_circle(self.camera.RAWimage)
					print("Decreased exposure ", self.camera.setExposure, " new data value (removed noise) : ", round(np.mean(circular_img) - NOISEimage, 4))
									
				while round(np.mean(circular_img) - NOISEimage, 4) < minMeanGray :
					self.fileHandler.write_text(str(round(np.mean(circular_img) - NOISEimage, 4)))
					self.camera.change_exposure(self.camera.setExposure + 50)
					print("increase exposure, new value : ", self.camera.setExposure)
					self.camera.capture_RAWimage()
					circular_img = self.calibration.pixels_in_circle(self.camera.RAWimage)
					print("Increased exposure ", self.camera.setExposure, " new data value (removed noise) : ", round(np.mean(circular_img) - NOISEimage, 4))
				
				#BRDF = Pr/Pi * Omega_det * cos (theta_det), omdega_det = A/R^2, Pi = totIncidentLight, Pr = round(np.mean(circular_img) - NOISEimage, 4), theta_det = reflection angle from specular
				BSDF_RAW_data[i][w] = round(np.mean(circular_img) - NOISEimage, 4)
				print("saved data : ", BSDF_RAW_data[i][w])
				self.fileHandler.write_text(str(BSDF_RAW_data[i][w]))
				w += 1
			i  += 1
			w = 0
			self.fileHandler.write_text("\n")
			
			
		print("loop ended, size", len(BSDF_RAW_data[0]), "x", len(BSDF_RAW_data))
		self.fileHandler.write_text("DataEnd")
		
		
	def take_picture_avgGray(self):
		global NOISEimage, totIncidentLight
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
		larger_values = NOISEimage > RAWimage 
		NOISEimage[larger_values] = RAWimage[larger_values]
		print(RAWimage - NOISEimage)
		avgNoNoise = self.imageProcessing.Average_Gray_Value(RAWimage - NOISEimage)
		pixelMax = (RAWimage).max()
		messagebox.showinfo("Message", f" Image taken\n\nHistogram will be displayed after this window is closed\n\nAverage Gray value is: {avgRAW}, average without noise is: {avgNoNoise}, max value with noise(is it saturated?) {pixelMax}")
		hist = self.imageProcessing.plotHistogram(RAWimage-NOISEimage)
		np.savetxt("array_exp350mikros_P1,3mikrow.txt", RAWimage-NOISEimage, fmt="%d")
		plt.plot(hist)
		plt.gca().yaxis.set_major_locator(plt.MaxNLocator(integer=True))
		plt.show()
		
	def take_picture_noise(self):
		global NOISEimage
		self.camera.capture_Noiseimage()
		NOISEimage = self.camera.NOISEimage
		
		
	def button_Calibrate(self):
		global blobCenter_y, blobCenter_x, NOISEimage, totIncidentLight

		# ~ hist = self.imageProcessing.plotHistogram(grayImage)
		# ~ global blobCenter_y, blobCenter_x
		# ~ blobCenter_y, blobCenter_x = self.imageProcessing.Max_GrayValue_Pixel(self.imageProcessing, self.camera)
		
		blobCenter_y, blobCenter_x, blobDiameter = self.calibration.blob_detection()
		
		circular_img = self.calibration.pixels_in_circle(self.camera.RAWimage) #alla channels
		# ~ circular_img = self.calibration.pixels_in_circle(self.camera.img) #blue channel
		
		messagebox.showinfo("Message", f"The image is saved as beamprofile_onlyBlue_test.jpg. \n\nPixel Position is: y: {round(blobCenter_y)}, x: {round(blobCenter_x)}, blob diameter: {round(blobDiameter)}, avg with noise: {round(np.mean(circular_img), 3)}, stddev with noise: {round(np.std(circular_img), 3)}, stddev/mean with noise= {round(np.std(circular_img)/np.mean(circular_img), 3)}. Now cover the light source because a noise pic will be taken after you press OK. ")
		
		self.camera.capture_Noiseimage()
		NOISEimage = self.calibration.pixels_in_circle(self.camera.NOISEimage)
		NOISEimage = round(np.mean(NOISEimage), 3) 
		
		totIncidentLight = self.calibration.pixels_in_circle(self.camera.RAWimage)
		totIncidentLight_mean = round(np.mean(totIncidentLight - NOISEimage), 3) 
		totIncidentLight_std =  round(np.std(totIncidentLight - NOISEimage), 3) 
		
		print("circular image shape:", circular_img.shape)
		# ~ messagebox.showinfo("Message", f" noise avg: {NOISEimage}, blob diameter: {round(blobDiameter)}, mean w/o noise: {totIncidentLight_mean}, stddev w/o noise: {totIncidentLight_std}, stddev/mean w/o noise= {round((totIncidentLight_std)/totIncidentLight_mean, 3)}")
		
		
		
	def StartPage(self): #start material properties 
		frame = customtkinter.CTkFrame(self.customtkinter, width=140, corner_radius=0)
		frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
		frame.grid_rowconfigure(4, weight=1)
		# ~ background_label = tk.Label(frame, image=self.background_photo)
		# ~ background_label.place(x=0, y=0, relwidth=1, relheight=1)
		
		# ~ label = tk.Label(frame, text="Start Page")
		# ~ label.pack(pady=10, padx=10)
		
		sidebar_frame = customtkinter.CTkFrame(frame, width=140, corner_radius=0)
		sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
		sidebar_frame.grid_rowconfigure(4, weight=1)
		logo_label = customtkinter.CTkLabel(sidebar_frame, text="Choose option", font=customtkinter.CTkFont(size=20, weight="bold"))
		logo_label.grid(row=0, column=0, padx=20, pady=10)
		sidebar_button_1 = customtkinter.CTkButton(sidebar_frame, text="BRDF", command = self.button_BRDF)
		sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
		sidebar_button_2 = customtkinter.CTkButton(sidebar_frame, text="BTDF", command = self.button_BTDF)
		sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
		sidebar_button_3 = customtkinter.CTkButton(sidebar_frame, text="Calibrate", command = self.button_Calibrate)
		sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
		appearance_mode_label = customtkinter.CTkLabel(sidebar_frame, text="Choose option:", anchor="w")
		appearance_mode_label.grid(row=7, column=0, padx=20, pady=(300, 0))
		appearance_mode_optionemenu = customtkinter.CTkOptionMenu(sidebar_frame, values=["StartPage", "FirstPage", "TestPage",], command = self.show_frame_str)
		appearance_mode_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 10))

		
        # create radiobutton frame
		radiobutton_frame = customtkinter.CTkFrame(frame)
		radiobutton_frame.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
		radio_var = tk.IntVar(value=0)
		label_radio_group = customtkinter.CTkLabel(radiobutton_frame, text="Sample Rotations:")
		label_radio_group.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky="")
		sampleRotations_1 = customtkinter.CTkRadioButton(radiobutton_frame, variable=radio_var, value=0, text="1", command = self.button_sampleRotations_1)
		sampleRotations_1.grid(row=1, column=2, pady=10, padx=20, sticky="n")
		radio_button_2 = customtkinter.CTkRadioButton(radiobutton_frame, variable=radio_var, value=1, state="disabled", text="2")
		radio_button_2.grid(row=2, column=2, pady=10, padx=20, sticky="n")
		radio_button_3 = customtkinter.CTkRadioButton(radiobutton_frame, variable=radio_var, value=2, state="disabled", text="3")
		radio_button_3.grid(row=3, column=2, pady=10, padx=20, sticky="n")

		
		monochrome_frame = customtkinter.CTkFrame(frame)
		monochrome_frame.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
		radio_var = tk.IntVar(value=0)
		label_radio_group = customtkinter.CTkLabel(monochrome_frame, text="Spectral Content:")
		label_radio_group.grid(row=0, column=2, columnspan=1, padx=(10,0), pady=10, sticky="")
		incidenceAngle_1 = customtkinter.CTkRadioButton(monochrome_frame, variable=radio_var, value=0, text="Monochrome", command = self.button_monochrome)
		incidenceAngle_1.grid(row=1, column=2, pady=10, padx=(20,0),  sticky="n")
		radio_button_2 = customtkinter.CTkRadioButton(monochrome_frame, variable=radio_var, value=1, state="disabled", text="Else")
		radio_button_2.grid(row=2, column=2, pady=10, padx=(20, 0), sticky="n")
		
		radiobutton_frame = customtkinter.CTkFrame(frame)
		radiobutton_frame.grid(row=1, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
		radio_var = tk.IntVar(value=0)
		label_radio_group = customtkinter.CTkLabel(radiobutton_frame, text="Angle of incidence:")
		label_radio_group.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky="")
		incidenceAngle_1 = customtkinter.CTkRadioButton(radiobutton_frame, variable=radio_var, value=0, text="1", command = self.button_angleOfIncidence)
		incidenceAngle_1.grid(row=1, column=2, pady=10, padx=20, sticky="n")
		radio_button_2 = customtkinter.CTkRadioButton(radiobutton_frame, variable=radio_var, value=1, state="disabled", text="2")
		radio_button_2.grid(row=2, column=2, pady=10, padx=20, sticky="n")
		radio_button_3 = customtkinter.CTkRadioButton(radiobutton_frame, variable=radio_var, value=2, state="disabled", text="3")
		radio_button_3.grid(row=3, column=2, pady=10, padx=20, sticky="n")

		
		radiobutton_frame = customtkinter.CTkFrame(frame)
		radiobutton_frame.grid(row=0, column=3, padx=(20, 0), pady=(20, 0), sticky="nsew")
		radio_var = tk.IntVar(value=0)
		label_radio_group = customtkinter.CTkLabel(radiobutton_frame, text="Azumuthial angles:")
		label_radio_group.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky="")
		radio_button_1 = customtkinter.CTkRadioButton(radiobutton_frame, variable=radio_var, value=0, text="1", command = self.button_scatterAzimuth_1)
		radio_button_1.grid(row=1, column=2, pady=10, padx=20, sticky="n")
		radio_button_2 = customtkinter.CTkRadioButton(radiobutton_frame, variable=radio_var, value=1, state="disabled", text="2", command = self.button_scatterAzimuth_2)
		radio_button_2.grid(row=2, column=2, pady=10, padx=20, sticky="n")
		radio_button_3 = customtkinter.CTkRadioButton(radiobutton_frame, variable=radio_var, value=2, state="disabled", text="3", command = self.button_scatterAzimuth_3)
		radio_button_3.grid(row=3, column=2, pady=10, padx=20, sticky="n")

		
		radiobutton_frame = customtkinter.CTkFrame(frame)
		radiobutton_frame.grid(row=1, column=3, padx=(20, 0), pady=(20, 0), sticky="nsew")
		radio_var = tk.IntVar(value=0)
		label_radio_group = customtkinter.CTkLabel(radiobutton_frame, text="Radial angles:")
		label_radio_group.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky="")
		radialAngles_1 = customtkinter.CTkRadioButton(radiobutton_frame, variable=radio_var, value=0, text="1", command = self.button_scatterRadial_1)
		radialAngles_1.grid(row=1, column=2, pady=10, padx=20, sticky="n")
		radio_button_2 = customtkinter.CTkRadioButton(radiobutton_frame, variable=radio_var, value=1, text="2", command = self.button_scatterRadial_2)
		radio_button_2.grid(row=2, column=2, pady=10, padx=20, sticky="n")
		radio_button_3 = customtkinter.CTkRadioButton(radiobutton_frame, variable=radio_var, value=2, text="3", command = self.button_scatterRadial_3)
		radio_button_3.grid(row=3, column=2, pady=10, padx=20, sticky="n")
		
		radiobutton_frame = customtkinter.CTkFrame(frame)
		radiobutton_frame.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew", columnspan = 1)
		radio_var = tk.IntVar(value=0)
		self.entry = customtkinter.CTkEntry(radiobutton_frame, placeholder_text="User name")
		self.entry.grid(row=0, column=1, padx=(10, 10), pady=(20, 30), sticky="nsew", rowspan = 2, columnspan = 1)
		save_button = customtkinter.CTkButton(radiobutton_frame, fg_color="transparent", border_width=1, text_color=("gray10", "#DCE4EE"), text="Save", command = lambda: self.button_writeInfo(self.entry))
		save_button.grid(row=2, column=1, padx=(20, 20), pady=(10, 0), sticky="nsew")
		
		main_button_1 = customtkinter.CTkButton(frame, fg_color="transparent", border_width=1, text_color=("gray10", "#DCE4EE"), text="Next", command = lambda: self.show_frame_str("collectingDataPage"))
		main_button_1.grid(row=3, column=3, padx=(10, 0), pady=(10, 0), sticky="nsew")
		
		return frame
		
	def TestPage(self): #test and try the camera for RAW data
		frame = customtkinter.CTkFrame(self.customtkinter,  width=140, corner_radius=0)
		frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
		frame.grid_rowconfigure(4, weight=1)
		# ~ background_label = tk.Label(frame, image=self.background_photo)
		# ~ background_label.place(x=0, y=0, relwidth=1, relheight=1)
		
		# ~ label = tk.Label(frame, text="Test Page")
		# ~ label.pack(pady=10, padx=10)
		
		sidebar_frame = customtkinter.CTkFrame(frame, width=140, corner_radius=0)
		sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
		sidebar_frame.grid_rowconfigure(4, weight=1)
		logo_label = customtkinter.CTkLabel(sidebar_frame, text="Choose option", font=customtkinter.CTkFont(size=20, weight="bold"))
		logo_label.grid(row=0, column=0, padx=20, pady=10)
		buttonTakePic = customtkinter.CTkButton(sidebar_frame, text="2. Take Picture", command= self.take_picture_avgGray)
		buttonTakePic.grid(row=2, column=0, padx=20, pady=10)
		
		buttonNoise = customtkinter.CTkButton(sidebar_frame, text="1. Take Noise Pic", command= self.take_picture_noise)
		buttonNoise.grid(row=1, column=0, padx=20, pady=10)
		
		appearance_mode_label = customtkinter.CTkLabel(sidebar_frame, text="Choose option:", anchor="w")
		appearance_mode_label.grid(row=4, column=0, padx=20, pady=(350, 0))
		appearance_mode_optionemenu = customtkinter.CTkOptionMenu(sidebar_frame, values=["TestPage", "StartPage", "FirstPage"], command = self.show_frame_str)
		appearance_mode_optionemenu.grid(row=5, column=0, padx=20, pady=(10, 10))
		
		return frame
		
	def collectingDataPage(self):
		frame = customtkinter.CTkFrame(self.customtkinter, width = 140, corner_radius=0)
		frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
		frame.grid_rowconfigure(4, weight=1)
	
		#create sidebar frame with widgets
		sidebar_frame = customtkinter.CTkFrame(frame, width=140, corner_radius=0)
		sidebar_frame.configure(height = 580)
		sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
		sidebar_frame.grid_rowconfigure(4, weight=1)
		logo_label = customtkinter.CTkLabel(sidebar_frame, text="Data Acquisition", font=customtkinter.CTkFont(size=20, weight="bold"))
		logo_label.grid(row=0, column=0, padx=20, pady=(20, 0))

		appearance_mode_label = customtkinter.CTkLabel(sidebar_frame, text="Choose option:", anchor="w")
		appearance_mode_label.grid(row=7, column=0, padx=20, pady=(450, 0))
		appearance_mode_optionemenu = customtkinter.CTkOptionMenu(sidebar_frame, values=["collectingDataPage", "StartPage"], command = self.show_frame_str)
		appearance_mode_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 0))
		
		button_Begin = customtkinter.CTkButton(frame, text="Begin", command = self.button_Begin)
		button_Begin.grid(row=1, column=0, padx=20, pady=10)		
		
		return frame
		
	def FirstPage(self): #Button for Test and Start
		frame = customtkinter.CTkFrame(self.customtkinter, width=140, corner_radius=0)
		frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
		frame.grid_rowconfigure(4, weight=1)
		
		#create sidebar frame with widgets
		sidebar_frame = customtkinter.CTkFrame(frame, width=140, corner_radius=0)
		sidebar_frame.configure(height = 580)
		sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
		sidebar_frame.grid_rowconfigure(4, weight=1)
		logo_label = customtkinter.CTkLabel(sidebar_frame, text="Welcome!", font=customtkinter.CTkFont(size=20, weight="bold"))
		logo_label.grid(row=1, column=0, padx=10, pady=(20, 20))

		appearance_mode_label = customtkinter.CTkLabel(sidebar_frame, text="Choose option:", anchor="w")
		appearance_mode_label.grid(row=7, column=0, padx=20, pady=(420, 0))
		appearance_mode_optionemenu = customtkinter.CTkOptionMenu(sidebar_frame, values=["FirstPage", "TestPage", "StartPage"], command = self.show_frame_str)
		appearance_mode_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 0))
		
		# create textbox
		textbox = customtkinter.CTkTextbox(frame, width=250)
		textbox.grid(row=1, column=3, padx=(100, 10), pady=20, sticky="nsew")
		textbox.insert("0.0", "Welcome to the optical scattering measurement device developed by Amanda Gåhlin, Ida Grunwald, Jonathan Eriksson, Gabriel Yousef and Amanda Ekberg as part of their master thesis spring 2024")
		
		# ~ img = Image.open("teamet.png")
		# ~ img = img.resize((640, 360), Image.ANTIALIAS)
		# ~ newImg = customtkinter.CTkImage(img)
		# ~ imgTeam = customtkinter.CTkLabel(frame, text=" ", image = newImg, width = 360, height = 640)
		# ~ imgTeam.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
		
		return frame
		
	def run(self):
		self.master.mainloop()
		
	

		
		
