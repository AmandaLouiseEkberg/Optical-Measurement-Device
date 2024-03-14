import tkinter as tk
from tkinter import messagebox
from image_processing import Processing

class GUI_application:
	def __init__(self, main_window, avgGray, fileHandler): #add more entries here for interactions
		self.master = main_window
		self.fileHandler = fileHandler
		self.avgGray = avgGray
		
		#Design of window
		self.master.geometry("500x500")
		self.master.title("Optical Scattering Measurement Device")
		self.create_widgets()
		
		
	def create_widgets(self):
		self.label = tk.Label(self.master, text="Welcome")
		self.label.pack()
		
		self.button_BRDF = tk.Button(self.master, text="BRDF", command = self.button_BRDF, bg="blue", fg="white", font=("Helvetica", 12), bd=2, relief=tk.RAISED)
		self.button_BRDF.place(x=200, y=200)
		
		self.button_BTDF = tk.Button(self.master, text="BTDF", command = self.button_BTDF, bg="blue", fg="white", font=("Helvetica", 12), bd=2, relief=tk.RAISED)
		self.button_BTDF.place(x=300, y=200)
		
		self.button_sampleRotations = tk.Button(self.master, text="Sample Rotations", command = self.button_sampleRotations, bg="blue", fg="white", font=("Helvetica", 12), bd=2, relief=tk.RAISED)
		self.button_sampleRotations.place(x=250, y=400)
		
		self.button_angleOfIncidence = tk.Button(self.master, text="Angle of Incidences", command = self.button_angleOfIncidence, bg="blue", fg="white", font=("Helvetica", 12), bd=2, relief=tk.RAISED)
		self.button_angleOfIncidence.place(x=250, y=500)
		
		self.button_scatterRadial = tk.Button(self.master, text="Scatter Radial", command = self.button_scatterRadial, bg="blue", fg="white", font=("Helvetica", 12), bd=2, relief=tk.RAISED)
		self.button_scatterRadial.place(x=250, y=600)
		
	def button_BRDF(self):
		messagebox.showinfo("Message", "BRDF measurement chosen")
		self.fileHandler.write_text("ScatterType  BRDF\n")
		
	def button_BTDF(self):
		messagebox.showinfo("Message", "BTDF measurement chosen")
		self.fileHandler.write_text("ScatterType  BTDF\n")
		
	def button_sampleRotations(self):
		messagebox.showinfo("Message", "Choose number of sample rotations (1 is entered now at 0 degrees)")
		self.fileHandler.write_text("SampleRotation 1\n0\n")
		
	def button_angleOfIncidence(self):
		messagebox.showinfo("Message", "Choose number of angles of incidence (1 is entered now at 0 degrees)")
		self.fileHandler.write_text("AngleOfIncidence 1\n0\n")
		
	def button_scatterRadial(self):
		messagebox.showinfo("Message", "Choose number of scatter radials (1 is entered now at 0 degrees)")
		self.fileHandler.write_text("AngleOfIncidence 1\n0\n")
		
