import threading
import socket
import sys

def server():
  name = '[SERVER]'
  host = '127.0.0.1'
  port = 2004
  serverSocket = socket.socket()

  try:
    serverSocket.bind((host, port))
  except socket.error as e:
    print(f'{name} - {e}\n')
  print(f'{name} - listening..\n')
  serverSocket.listen(5)

  def handle_request(sock_client,addr):
    print(f'{name} - working...\n')
    data = sock_client.recv(2048)
    print(f'{name} - received request [{data.decode()}] from [{addr}]\n')
    while data:
      data = data.decode().split(' ')
      reply = ''
      if(len(data)!=1):
        data[1] = int(data[1])
        data[2] = int(data[2])
      if(data[0]=='+'):
        reply=f'{data[1]+data[2]}'
      elif(data[0]=='-'):
        reply=f'{data[1]-data[2]}'
      elif(data[0]=='/'):
        reply=f'{data[1]/data[2]}'
      elif(data[0]=='*'):
        reply=f'{data[1]*data[2]}'
      elif(data[0]=='%'):
        reply=f'{data[1]%data[2]}'
      elif(data[0]=='^'):
        reply=f'{data[1]**data[2]}'
      elif(data[0]=='END'):
        sock_client.close()
        print(f'{name} - Service for [{addr}] closed\n')
        sys.exit()
      else:
        reply = 'BAD REQUEST!!!'
      sock_client.sendall(str.encode(reply))
      print(f'{name} - sent answer [{reply}] to [{addr}]\n')
      print(f'{name} - Waiting for next request...\n')
      data = sock_client.recv(2048)

  try:
    while True:
      client, addr = serverSocket.accept()
      print(f'{name} - Connected to: ' + addr[0] + ':' + str(addr[1])+'\n')
      thrd = threading.Thread(target=handle_request, args=(client, addr, ))
      thrd.start()
  finally:
    serverSocket.close()
