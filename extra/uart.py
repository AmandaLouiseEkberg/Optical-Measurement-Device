import serial
import time

ser = serial.Serial(
	port = '/dev/ttyS0',
	baudrate = 9600,
	parity = serial.PARITY_NONE,
	stopbits = serial.STOPBITS_ONE,
	bytesize = serial.EIGHTBITS,
	timeout = 1000
)

def send_command(command):
	ser.write(command.encode())

def receive_acknowledgement():
	start_time = time.time()
	while True:
		acknowledgement = ser.readline().decode().strip()
		if acknowledgement:
			print("Received acknowledgement: ", acknowledgement)
			break
		elif time.time() - start_time > 1:
			print("Timeout: no acknowledgement received")
			break

def main():
	forward_command = 'FORWARDS'
	backward_command = 'BACKWARD'
	
	try:
		while True:
			send_command(forward_command)
			receive_acknowledgement()
			time.sleep(2)
			send_command(backward_command)
			receive_acknowledgement()
			time.sleep(2)
		

	except KeyboardInterrupt:
		ser.close()
		print("Serial port closed")


if __name__ == "__main__":
	main()
	
