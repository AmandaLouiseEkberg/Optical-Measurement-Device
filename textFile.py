from datetime import datetime

class textFileHandler:
	def __init__(self, filename):
		self.filename = filename
		
		#Automatically save date and time
		now = datetime.now()
		timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
		with open(self.filename, 'w') as file:
			file.write(f"#Data Generated by Afry's BSDF imaging solution\n#{timestamp} \nSource Measured\nSymmetry PlaneSymmetrical \nSpectralContent Monochrome\n")
		
	def write_text(self, text):
		with open(self.filename, 'a') as file:
			file.write(text + '\n')
			
			
