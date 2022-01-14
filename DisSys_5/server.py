from calendar import c
import rpyc
import json
import hashlib
import datetime
# json.dumps(a dictionary) || making a string
# 
# with open('board.json', 'w') as outfile:
#  json.dump('', outfile)

JSON_IS_WRITING = ''

class MyService(rpyc.Service):
    
    role = 'USER' # can be either OWNER or USER
    name = ''
    currentJSON = {}

    def on_connect(self, conn):
      pass
    def on_disconnect(self, conn):
      pass

    def jsonRead(self):
      with open('board.json') as json_file:
        self.currentJSON = json.load(json_file)

    def jsonWrite(self, JSON_IS_WRITING, content, action):
      while(JSON_IS_WRITING != ''):
        pass
      JSON_IS_WRITING = self.name
      self.jsonRead()
      ##### CRITICAL SECT #####
      if(action == 'delete'):
        self.currentJSON['messages'] = [msg for msg in self.currentJSON['messages'] if msg['id'] != content]
      elif(action == 'send'):
        self.currentJSON['messages'].append(content)
      elif(action == 'register'):
        self.currentJSON['users'].append(content)
      else:
        return -1
      with open('board.json', 'w') as outfile:
        json.dump(self.currentJSON, outfile)
      #########################
      JSON_IS_WRITING = ''
      return 1 #

    def exposed_register(self, name, role):
      self.jsonRead()
      self.role = role
      self.name = name
      for user in self.currentJSON['users']:
        # print(user)
        if(user['name'] == name):
          return f'user exists. Welcome {name}!'
      self.jsonWrite(JSON_IS_WRITING, content={'role':self.role,'name':self.name}, action='register')
      return f'user registered. Welcome {name}!'

    def exposed_sending(self, receiver, message):
      date = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
      hash = hashlib.sha1(date.encode("UTF-8")).hexdigest()
      hash = hash[:6]
      self.jsonWrite(JSON_IS_WRITING, content={'receiver':receiver,'sender':self.name,'message':message, 'id':hash, 'date':date}, action='send')
    
    def exposed_receiving(self):
      self.jsonRead()
      inbox = [msg for msg in self.currentJSON['messages'] if msg['receiver'] == self.name]
      inbox = sorted(inbox, key=lambda i:i['date'], reverse=True)
      return inbox[0]

    def exposed_delete(self, delID):
      if(self.role == 'OWNER'):
        self.jsonWrite(JSON_IS_WRITING, content = delID, action='delete')
        return 1
      return -1

    def exposed_checkRecv(self):
      self.jsonRead()
      inbox = [msg for msg in self.currentJSON['messages'] if msg['receiver'] == self.name]
      inbox = sorted(inbox, key=lambda i:i['date'], reverse=True)
      return inbox

    def exposed_checkSent(self):
      self.jsonRead()
      inbox = [msg for msg in self.currentJSON['messages'] if msg['sender'] == self.name]
      inbox = sorted(inbox, key=lambda i:i['date'], reverse=True)
      return inbox

    def exposed_checkUsers(self):
      self.jsonRead()
      return self.currentJSON['users']

if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    t = ThreadedServer(MyService, port=18861)
    t.start()
