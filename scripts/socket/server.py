import socket

# Server IP or Hostname
HOST = ''

# Make sure it's 1000+
PORT = 65432

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

s.bind((HOST, PORT))
s.listen()

print('Waiting for messages')
(conn, addr) = s.accept()
print('Got connection from', addr)

while True:
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

conn.close() # Close connections