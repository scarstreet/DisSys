import threading
from client import client
from server import server

t = threading.Thread(target=server, )
t.start()
for i in range(3):
  tt = threading.Thread(target=client, args=(i+1, ), )
  tt.start()