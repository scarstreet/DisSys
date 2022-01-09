import threading
import socket
import time
import DisSys_GlobalDB as db

def serve():
  name = '[SERVER THREAD] '
  host = socket.gethostbyname(socket.gethostname())
  port = 2004
  ThreadCount = 0
  serverSocket = socket.socket()
  lock = threading.Lock()

  try:
    serverSocket.bind((host, port))
  except socket.error as e:
    print(str(e))
  print(f'{name}-Socket is listening..\n')

  serverSocket.listen(5)

  def busyWait():
    i = 0
    for ii in range(2000000):
      i += 1
  
  def canRead():
    return (not lock.locked() and len(db.Writers) == 0)
  def canWrite(current_client):
    return (current_client == db.Writers[0])

  def handle_request(sock_client):
    print(f'{name}-Server is working...\n')
    data = sock_client.recv(2048).decode().split(' ')
    while data:
      print(f'{name}- REQ GOT - {data}\n')
      response = ''
      if data[0] == 'END':
        break
      elif data[0] == 'read': # if it's read vvvvvvvvvvvvvvvvvvvvvvvvv
        # contention control ---------------------------------------
        execute = canRead()
        while execute == False:
          print(f"want read, db.Writers now {len(db.Writers)}")
          execute = canRead()
        print(f'{name}- WILL NOW READ\n')
        # contention control ---------------------------------------
        busyWait()
        resArr = []
        if(data[1] == '>'):
          resArr = filter(lambda x:x > int(data[2]), db.Array)
        elif(data[1] == '<'):
          resArr = filter(lambda x:x < int(data[2]), db.Array)
        else:
          resArr = filter(lambda x:x % int(data[2]) == 0, db.Array)
        resArr = list(resArr)
        response = ''
        for r in resArr:
          response += str(r) + ' '
        response = response[:-1]
      else: # if it's write vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
        data = data[1:]
        data = list(map(lambda x: int(x),data))
        # contention control ------------------------------------------
        db.Writers.append(sock_client)
        execute = canWrite(sock_client)
        while execute == False:
          execute = canWrite(sock_client)
        with lock: #CRITICAL SECTION STARTS HERE -----------------
          busyWait()
          db.Array = data 
        #CRITICAL SECTION ENDS HERE -------------------
        if len(db.Writers)==1:
          db.Writers = []
        else:
          db.Writers = db.Writers[1:]
        # contention control ------------------------------------------

        for r in db.Array:
          response += str(r) + ' '
        response = response[:-1]
        response = name +'- UPDATED SERVER - ' + response
      sock_client.sendall(str.encode(response))
      # print(f'{name}-SERVER LISTENING FOR NEXT REQ\n')
      data = sock_client.recv(2048).decode().split(' ')
    serverSocket.close()
  try:
    while True:
      client, addr = serverSocket.accept()
      print(f'{name} - Connected to: ' + addr[0] + ':' + str(addr[1])+'\n')
      thrd = threading.Thread(target=handle_request,args=(client, ))
      thrd.start()
      ThreadCount += 1
      print(f'{name} - Thread Number: ' + str(ThreadCount)+'\n')
  except:
    serverSocket.close()
    print(f'{name} - CLOSED\n')

