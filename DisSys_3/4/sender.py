import socket
import struct
import sys

name = '[SENDER]'
multicast_group = ('224.3.29.71', 10000)

TEST = [
  'Never gonna give you up Never gonna let you down'.split(' '),
  'Never gonna run around and desert y o u ~'.split(' '),
  'Never gonna make you cry Never gonna say good bye'.split(' '),
  'Never gonna tell a lie and hurt you ~ <3'.split(' '),
]

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(0.2)
ttl = struct.pack('b', 1)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

try:
  case = 0
  for toSend in TEST:
    print(f'\n\n{name} - testing for Case {case} ===========================================================')
    for send in toSend:
      sent = sock.sendto(send.encode(), multicast_group)
      print(f'\n{name} - sending [{send}]')
      while True:
        print(f'{name} - waiting to receive ack')
        try:
          data, server = sock.recvfrom(16)
        except socket.timeout:
          print(f'{name} - timed out, no more responses')
          break
        else:
          print(f'{name} - received "%s" from %s' % (data.decode(), server))
    case += 1
finally:
  print(f'{name} - closing socket')
  sock.close()