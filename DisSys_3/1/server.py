import threading
import socket
import sys

host = '127.0.0.1'
port = 2004
ThreadCount = 0
serverSocket = socket.socket()

try:
  serverSocket.bind((host, port))
except socket.error as e:
  print(str(e))
print('Socket is listening..')
serverSocket.listen(5)

def handle_request(sock_client):
  print('Server is working...')
  data = sock_client.recv(2048)
  while data:
    response = 'Server message: ' + data.decode('utf-8')
    sock_client.sendall(str.encode(response)) # echo
    data = sock_client.recv(2048)
    if(data.decode()=='END'):
      break
  sock_client.close()
  sys.exit()

try:
  while True:
    client, addr = serverSocket.accept()
    print('Connected to: ' + addr[0] + ':' + str(addr[1]))
    thrd = threading.Thread(target=handle_request,
    args=(client, ))
    thrd.start()
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))
finally:
  serverSocket.close()
