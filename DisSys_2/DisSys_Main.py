import threading
from DisSys_Server import serve
from DisSys_Client import client

t = threading.Thread(target=serve)
t.start()
for i in range(5):
  t = threading.Thread(target=client, args=(i,'read'))
  t.start()
for i in range(1):
  t = threading.Thread(target=client, args=(i,'write'))
  t.start()
