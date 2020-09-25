import socket

HOST = '192.168.1.5' # Server IP or Hostname
PORT = 65432 #1000+ recoommended
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST,PORT))

while True:
	command = input('Enter your command: ')

	sock.send(bytes(command, "utf-8"))

	reply = sock.recv(1024)
	reply = reply.decode("utf-8")

	if reply == 'Quitting...':
		print("Quitting...")
		break
	elif reply == 'Send the Image':
		f = open('file.png', 'rb')
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