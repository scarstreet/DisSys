import socket
import time
from random import randrange

def client(id,role):
  name = f'[CLIENT {role} THREAD '+str(id)+'] '
  clientSocket = socket.socket()
  host = socket.gethostbyname(socket.gethostname())
  port = 2004

  READ_REQ = ['>','<','%']

  def writeReq():
    arr = [0]*10
    for i in range(10):
      arr[i] = randrange(30)
    req = 'write '
    for i in arr:
      req += str(i) + ' '
    req = req[:-1]
    return req

  def readReq():
    req = 'read ' + READ_REQ[randrange(3)] + ' ' + str(randrange(1,10))
    return req

  def makeRequest():
    request = ''
    if(role == 'read'):
      request = readReq()
      print(f'{name}- READ request - {request}\n')
    else:
      request = writeReq()
      print(f'{name}- WRITE request - {request}\n')
    return request

  print(f'{name}- Waiting for connection response\n')
  try:
    clientSocket.connect((host, port))
  except socket.error as e:
    print(str(e))

  for i in range(4):
    Input = makeRequest()
    clientSocket.send(str.encode(Input))
    res = clientSocket.recv(1024).decode()
    print(f'{name}- RESponse received - {res}\n')
    time.sleep(1)
  clientSocket.send(str.encode('END'))
  print(f'{name}- CLOSED\n')
