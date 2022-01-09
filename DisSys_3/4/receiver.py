import socket
import struct
import sys

name='[RECEIVER]'
multicast_group = '224.3.29.71'
server_address = ('', 10000)

# Create the socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to the server address
sock.bind(server_address)

# Tell the operating system to add the socket to the multicast group
# on all interfaces.
group = socket.inet_aton(multicast_group)
mreq = struct.pack('4sl', group, socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

# Receive/respond loop
while True:
  print(f'\n{name} - waiting to receive message')
  data, address = sock.recvfrom(1024)
  print(f'{name} - received [{data.decode()}]')
  print(f'{name} - sending ack to SERVER')
  sock.sendto(('ack').encode(), address)