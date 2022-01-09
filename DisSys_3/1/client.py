import socket

clientSocket = socket.socket()
host = '127.0.0.1'
port = 2004

print('Waiting for connection response')
try:
  clientSocket.connect((host, port))
except socket.error as e:
  print(str(e))
while True:
  Input = input('Message to send: ')
  clientSocket.send(str.encode(Input))
  res = clientSocket.recv(1024)
  print(res.decode('utf-8'))
  if(Input=='END'):
    break
clientSocket.close()