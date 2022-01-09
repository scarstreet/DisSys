import socket
from random import choice,randint

def client(number):
  name = f'[CLIENT {number}]'
  clientSocket = socket.socket()
  host = '127.0.0.1'
  port = 2004

  REQ = ['+','-','/','*','%','^']

  print(f'{name} - Waiting for connection response\n')
  try:
    clientSocket.connect((host, port))
  except socket.error as e:
    print(f'{name} - {e}\n')
  for i in range(3):
    req = f'{choice(REQ)} {randint(1,100)} {randint(1,20)}'
    clientSocket.send(str.encode(req))
    print(f'{name} - Made request [{req}]\n')
    res = clientSocket.recv(1024)
    print(f'{name} - Got answer [{res.decode()}] for request [{req}]\n')
  clientSocket.send(str.encode('END'))
  clientSocket.close()