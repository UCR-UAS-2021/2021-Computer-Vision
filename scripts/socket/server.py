import socket

HOST = '' # Server IP or Hostname
PORT = 65432 # Make sure it's 1000+

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

s.bind((HOST, PORT))
s.listen()

print('Waiting for messages')
(conn, addr) = s.accept()
print('Got connection from', addr)

while True:
	print('Waiting for a command...')

	command = conn.recv(1024)
	command = command.decode("utf-8")

	print('Received: ' + command)

	if command == 'quit':
		conn.send(b'Quitting...')
		conn.close()
		break
	elif command == 'image':
		f = open('image.png', 'wb')
		conn.send(b'Send the Image')

		data = conn.recv(1024)
		while (data):
			print('Downloading file...')
			f.write(data)
			data = conn.recv(1024)
		f.close()
		print('Finished')
		conn.close()
		break
	else:
		conn.send(b'Unknown command')
		continue

conn.close() # Close connections