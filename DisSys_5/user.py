from email import message
import rpyc
import random

MENU = ['S','R','CI','CS','CU','D']

def showMenu():
  print()
  print('-> Send [S]')
  print('-> Receive [R]')
  print('-> Check Inbox [CI]')
  print('-> Check Sent [CS]')
  print('-> Check Users [CU]')
  if(role == 'OWNER'):
    print('-> Delete Message [D]')
  print()
  print('-> EXIT [E]')
  print()

border = '===================================================================='

board = rpyc.connect("localhost", 18861)

print('Welcome to the message boardom!! Please log in')
name = input('name : ')
role = input('role : [OWNER/USER] ')
while (role != 'OWNER' and role != 'USER'):
  print('Role invalid!! please try again')
  role = input('role : [OWNER/USER] ')
print(board.root.register(name,role))

op = ''

while op!='E':
  print(border)
  showMenu()
  op = input()
  if(op == 'S'):
    receiver = input('Receiver : ')
    message = input('Message (one line only!!): ')
    board.root.sending(receiver,message)
  elif(op == 'R'):
    i = board.root.receiving()
    print(border)
    print('Sender : ',end='')
    print(i['sender'])
    print('Date : ',end='')
    print(i['date'])
    print('Id : ',end='')
    print(i['id'])
    print('Message : ')
    print(i['message'])
    input('press enter to continue ')
  elif(op == 'CI'):
    inbox = board.root.checkRecv()
    for i in inbox:
      print(border)
      print('Sender : ',end='')
      print(i['sender'])
      print('Date : ',end='')
      print(i['date'])
      print('Id : ',end='')
      print(i['id'])
      print('Message : ')
      print(i['message'])
    input('press enter to continue ')
  elif(op == 'CS'):
    inbox = board.root.checkSent()
    for i in inbox:
      print(border)
      print('Receiver : ',end='')
      print(i['receiver'])
      print('Date : ',end='')
      print(i['date'])
      print('Id : ',end='')
      print(i['id'])
      print('Message : ')
      print(i['message'])
    input('press enter to continue ')
  elif(op == 'CU'):
    users = board.root.checkUsers()
    for i in users:
      print(border)
      print('Name : ',end='')
      print(i['name'])
      print('Role : ',end='')
      print(i['role'])
    input('press enter to continue ')
  elif(op == 'D' and role == 'OWNER'):
    print(border)
    toDelete = input('enter ID of message to delete : ')
    board.root.delete(toDelete)
  elif(op == 'E'):
    pass
  else:
    'BAD COMMAND, TRY AGAIN!!'


