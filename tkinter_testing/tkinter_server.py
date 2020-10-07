import socket
import os

# Had to hardcode the image path to make it work properly
image_path = os.path.expanduser("~/Projects/image.png")

# Server IP or Hostname
HOST = '192.168.1.10'

#1000+ recoommended
PORT = 65432

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST,PORT))

while True:
	f = open(image_path, 'rb')
	data = f.read(1024)

	while (data):
		print('Sending Image...')
		sock.send(data)
		data = f.read(1024)
	f.close()
	print('Image sent!')
	sock.close()
	break
sock.close()