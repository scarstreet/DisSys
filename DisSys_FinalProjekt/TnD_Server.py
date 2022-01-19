from random import randint
from turtle import update
import rpyc
import system
from objects import Item,Player
from system import Combat, Map
import database as db
import json
import socket
from copy import deepcopy
import hashlib
import datetime

STATE_IS_WRITING = -1
DATABASE = "state.json"


class Game(rpyc.Service): # only can return non custom classes!!
  def on_connect(self, conn):
    pass
  def on_disconnect(self, conn):
    self.getState()
    if(self.exposed_joined):
      self.exposed_leave()
    if(self.exposed_loggedIn):
      self.getState()
      self.STATE["onlinePlayerList"] = [p for p in self.STATE["onlinePlayerList"] if p != self.playerName]
      self.STATE["onlinePlayers"] -= 1
      self.setState(self.STATE, STATE_IS_WRITING, self.playerName)
    if(len(self.STATE['readyToPlayList'])==0 and self.map!=''):
      self.saveMapStatus()
      self.STATE["movementTurn"]=''
      self.STATE['isCombat']=False
      self.STATE['isTrading']=False
      self.setState(self.STATE, STATE_IS_WRITING, self.playerName)
    if(self.exposed_registered):
      self.getState()
      self.savePlayerState()
      self.setState(self.STATE, STATE_IS_WRITING, self.playerName)
#================================================================
# STATE MANAGEMENT 
#================================================================

  STATE = {}
  exposed_state = 0
  
  def getState(self):
    with open(DATABASE) as json_file:
      self.STATE = json.load(json_file)
    self.exposed_state = self.STATE['state']
    
  def setState(self,newSTATE, STATE_IS_WRITING,id):
    while(STATE_IS_WRITING != -1):
      pass
    STATE_IS_WRITING = id
    ##### CRITICAL SECT #####
    self.exposed_state += 1
    newSTATE['state'] += 1
    with open(DATABASE, "w") as outfile:
      json.dump(newSTATE, outfile)
    #########################
    STATE_IS_WRITING = -1
    self.getState()
    
  def savePlayerState(self):
    self.STATE["allPlayerDB"][self.playerName]["role"]=self.player.role
    self.STATE["allPlayerDB"][self.playerName]["baseStatus"] = self.player.baseStatus
    self.STATE["allPlayerDB"][self.playerName]["status"] = self.player.status
    
    if(self.player.equip["weapon"]!=""):
      self.STATE["allPlayerDB"][self.playerName]["equip"]["weapon"] = db.weapons.index(self.player.equip["weapon"])
    if(self.player.equip["armor"]!=""):
      self.STATE["allPlayerDB"][self.playerName]["equip"]["armor"] = db.armors.index(self.player.equip["armor"])
    if(self.player.equip["artifact"]!=""):
      self.STATE["allPlayerDB"][self.playerName]["equip"]["artifact"] = db.artifact.index(self.player.equip["artifact"])
    self.STATE["allPlayerDB"][self.playerName]["inventory"] = {"I":[],"ART":[],"ARM":[],"W":[],"C":[],"gold": 0}
    
    for item in self.player.inventory.items["I"]:
      self.STATE["allPlayerDB"][self.playerName]["inventory"]["I"].append(
        [db.items.index(item[0]),item[1]])
    for item in self.player.inventory.items["ART"]:
      self.STATE["allPlayerDB"][self.playerName]["inventory"]["ART"].append(
        [db.artifact.index(item[0]),item[1]])
    for item in self.player.inventory.items["ARM"]:
      self.STATE["allPlayerDB"][self.playerName]["inventory"]["ARM"].append(
        [db.armors.index(item[0]),item[1]])
    for item in self.player.inventory.items["W"]:
      self.STATE["allPlayerDB"][self.playerName]["inventory"]["W"].append(
        [db.weapons.index(item[0]),item[1]])
    for item in self.player.inventory.items["C"]:
      self.STATE["allPlayerDB"][self.playerName]["inventory"]["C"].append(
        [db.consumables.index(item[0]),item[1]])
    self.STATE["allPlayerDB"][self.playerName]["inventory"]["gold"] = self.player.inventory.gold
    
    self.setState(self.STATE,STATE_IS_WRITING,self.playerName)

  def exposed_waitGet(self): # Literally just waiting while getting state, all the time
    try:
      self.getState()
    except:
      pass
#================================================================
# REGISTRATION MANAGEMENT 
#================================================================
  
  exposed_loggedIn = False
  exposed_registered = False
  
  def exposed_register(self, username, password):
    self.getState()
    if(username in self.STATE["allPlayers"].keys()): # login
      if(password == self.STATE["allPlayers"][username]):
        playerData = self.STATE["allPlayerDB"][username]
        self.playerName = username
        # playerData = playerData.update({"name":username})
        self.player = Player(playerData,{
          "skills":db.skills,
          "I":db.items,
          "C":db.consumables,
          "ART":db.artifact,
          "ARM":db.armors,
          "W":db.weapons
        })
        self.player.setName(username)
        self.login()
        self.exposed_loggedIn = True
        self.exposed_registered = True
      else:
        self.exposed_loggedIn = False
    else: # register
      self.playerName = username
      self.playerPassword = password
      self.login()
      self.exposed_loggedIn = True
    self.setState(self.STATE,STATE_IS_WRITING,username)
  
  def exposed_newPlayer(self,in_role, in_status):
    self.getState()
    self.player = Player(in_role,in_status,db.skills[in_role])
    self.player.setName(self.playerName)
    self.STATE["allPlayerDB"].update({self.playerName:{
      "role": "",
      "skills": [],
      "baseStatus": {"HP": 0,"MP": 0,"ATK": 0,"DEF": 0,"AGI": 0,"LUK": 0,"LVL": 0,"EXP": 0,"EXP_CAP": 0},
      "status": { "HP": 0, "MP": 0, "ATK": 0, "DEF": 0, "AGI": 0, "LUK": 0 },
      "equip": { "weapon": '', "armor": '', "artifact": '' },
      "inventory": {"I": [],"ART": [],"ARM": [],"W": [],"C": [],"gold": 0}
    }})
    self.STATE["allPlayers"].update({self.playerName:self.playerPassword})
    self.exposed_registered = True
    self.savePlayerState()
  
  def exposed_save(self):
    self.savePlayerState()
  
  def login(self):
    self.getState()
    self.STATE["onlinePlayerList"].append(self.playerName)
    self.STATE["onlinePlayers"] += 1
    self.setState(self.STATE,STATE_IS_WRITING,self.playerName)
    self.exposed_roomFull = True if self.STATE["readyToPlay"] == 4 else False

#================================================================
# JOIN / LEAVE MANAGEMENT
#================================================================

  exposed_roomFull = False
  exposed_joined = False
  
  def exposed_ready(self):
    self.getState()
    self.STATE["readyToPlay"] += 1
    self.STATE["readyToPlayList"].append(self.playerName)
    self.setState(self.STATE,STATE_IS_WRITING,self.playerName)
    self.exposed_joined = True
    if(self.STATE["readyToPlay"] == 4):
      self.exposed_roomFull = True
    
  
  def exposed_waitVacant(self):
    try:
      self.getState()
      if(self.STATE["readyToPlay"] < 4):
        self.exposed_roomFull = False
    except:
      pass
    if(not self.exposed_roomFull):
      print(f"{self.playerName} -Able to join.")
  
  def exposed_waitFull(self):
    try:
      self.getState()
      if(self.STATE["readyToPlay"] >= 4):
        self.exposed_roomFull = True
      else:
        self.exposed_roomFull = False
    except:
      pass
    if(self.exposed_roomFull):
      print(f"{self.playerName} - Now playing!")
  
  def exposed_leave(self):
    self.getState()
    self.STATE["readyToPlay"] -= 1
    self.STATE["readyToPlayList"] = [p for p in self.STATE["readyToPlayList"] if p != self.playerName]
    self.setState(self.STATE,STATE_IS_WRITING,self.playerName)
    self.savePlayerState()
    self.exposed_joined = False
    if(self.STATE["readyToPlay"] < 4):
      self.exposed_roomFull = False
    else:
      self.exposed_roomFull = True
    print(f"{self.playerName} - Has left the game.") 

#================================================================
# MAP MOVEMENT MANAGEMENT
#================================================================

  map = '' # Map class
  exposed_movementTurn = ''
  exposed_isCombat = False
  exposed_isTrading = False
  exposed_currentLoc = [0,0]
  exposed_mapVisuals = []
  
  def exposed_initMap(self):
    if(self.STATE['movementTurn']=='' or self.STATE['movementTurn'] not in self.STATE['readyToPlayList']):
      self.exposed_movementTurn = self.STATE['readyToPlayList'][0]
    self.exposed_updateLocalMap()
  
  def  exposed_updateLocalMap(self): # update status of the current map from db visuals too
    self.getState()
    self.map = Map(
      map = db.map, areaList = db.areas, traderList= db.traders,
      currentLoc = self.STATE['currentLocation'],
      progress = self.STATE['mapProgress'],
      cleared = self.STATE['mapCleared'],
      boundaries= self.STATE['mapBoundaries'])
    self.exposed_currentLoc = self.map.currentLoc
    self.exposed_mapVisuals = deepcopy(db.mapVisual)
    newLine = list(self.exposed_mapVisuals[2*self.STATE['currentLocation'][0]])
    newLine[1+4*self.STATE['currentLocation'][1]] = '❖' #Players are here
    newLine = "".join(newLine)
    self.exposed_mapVisuals[2*self.STATE['currentLocation'][0]] = newLine
    for line in self.exposed_mapVisuals:
      for n in range(6):
        string = '-'+str(n)+str(n)+'-'
        if(line.find(string)!=-1): #the progress bar is on this line
          old = line
          index = line.find(string)
          progress = int((self.map.areaList[n].progress/self.map.areaList[n].toClear)*100)
          if progress > 100:
            progress = 100
          progress = str(progress)+'%'
          while(len(progress)<4):
            progress = ' '+progress
          line = list(line)
          line[index] = progress[0]
          line[index+1] = progress[1]
          line[index+2] = progress[2]
          line[index+3] = progress[3]
          line = "".join(line)
          self.exposed_mapVisuals[self.exposed_mapVisuals.index(old)] = line
  
  def saveMapStatus(self): # saving status of the map to db
    self.STATE["currentLocation"] = self.map.currentLoc
    self.STATE["mapBoundaries"] = self.map.boundaries
    self.STATE["mapProgress"] = [a.progress for a in self.map.areaList]
    self.STATE["mapCleared"] = [a.isCleared for a in self.map.areaList]
    self.STATE["movementTurn"] = self.exposed_movementTurn
    self.STATE["isCombat"] = self.exposed_isCombat
    self.STATE["isTrading"] = self.exposed_isTrading
    self.setState(self.STATE, STATE_IS_WRITING, self.playerName)
  
  def exposed_waitForAction(self): # in client, prioritize combat and trading, then movement
      try:
        self.getState()
        self.exposed_movementTurn = self.STATE["movementTurn"]
        if(self.exposed_isCombat == False and self.STATE["isCombat"] == True):
          self.combat = Combat()
          while(self.combat.enemies == []):
            self.exposed_updateCombatState()
        self.exposed_isCombat = self.STATE["isCombat"]
        self.exposed_isTrading = self.STATE["isTrading"]
        self.exposed_updateLocalMap()
      except:
        pass
    
  def exposed_mapMoveTo(self,location):
    # self.initCombat() # TODO - delete this. this is just debug
    # self.exposed_isCombat = True
    self.map.moveParty(location)
    # if(self.map.map[location[0]][location[1]]<0):
    #   self.exposed_isTrading = True
    #   # TODO - trading!!!
    if(randint(1,3)==2):
      self.exposed_isCombat = True
      self.initCombat()
    self.saveMapStatus()
    index = self.STATE["readyToPlayList"].index(self.playerName)
    nextTurn = self.STATE["readyToPlayList"][0] if index + 1 == len(self.STATE["readyToPlayList"]) else self.STATE["readyToPlayList"][index+1]
    self.exposed_movementTurn = self.STATE['movementTurn'] = nextTurn
    self.saveMapStatus()
    self.exposed_updateLocalMap()
  
  def detGameState(self): # TODO - to end the game
    pass

#================================================================
# COMBAT MANAGEMENT
#================================================================
  combat = '' #combat class
  exposed_combatDict = {}
  exposed_players = []
  
  def updatePlayers(self):
    self.exposed_players = []
    for p in self.STATE["readyToPlayList"]:
      self.exposed_players.append(self.STATE['allPlayerDB'][p])
    # self.exposed_saveCombatState()
  
  def initCombat(self):
    self.STATE['combat'] = {
      "turn": "",
      "turnCounter": 0,
      "whichPlayer": "",
      "enemies": [],
      "whichEnemy": 0,
      "result": "",
      "expDrop": 0,
      "goldDrop": 0,
      "itemDrop": {},
      "combatLog": ""
    }
    # self.setState(self.STATE,STATE_IS_WRITING,self.playerName)
    self.combat = Combat(self.map.areaList[self.map.currentArea],self.STATE["readyToPlayList"],self.STATE,{
          "monsters":db.monsters,
          "skills":db.skills,
          "I":db.items,
          "C":db.consumables,
          "ART":db.artifact,
          "ARM":db.armors,
          "W":db.weapons
    })
    print(self.combat.enemies)
    self.exposed_saveCombatState()
    self.exposed_updateCombatState()
    self.updatePlayers()
    
  def exposed_saveCombatState(self):
    print(self.combat.players)
    self.STATE['combat']['turn'] = self.combat.turn
    self.STATE['combat']['turnCounter'] = self.combat.turnCounter
    self.STATE['combat']['whichPlayer'] = self.combat.whichPlayer
    self.STATE['combat']['enemies'] = []
    for enemy in self.combat.enemies:
      enemyStats = {
        "isAlive":enemy.isAlive,
        "effects":[],
        "status":enemy.status,
        "baseStatus":enemy.baseStatus,
      }
      for effect in enemy.effects:
        print(effect)
        enemyEffect = {
            "effect": effect['effect'],
            "turn": effect['turn'],
            "stat": effect['stat']
          }
        enemyStats['effects'].append(enemyEffect)
      self.STATE['combat']['enemies'].append(enemyStats)
    self.STATE['combat']['whichEnemy'] = self.combat.whichEnemy
    self.STATE['combat']['result'] = self.combat.result
    self.STATE['combat']['expDrop'] = self.combat.expDrop
    self.STATE['combat']['goldDrop'] = self.combat.goldDrop
    self.STATE['combat']['itemDrop'] = self.combat.itemDrop
    self.STATE['combat']['combatLog'] = self.combat.combatLog
    categ = self.combat.itemDrop.keys()
    for c in categ:
      categ = c
      break
    if(categ == 'I'):
      self.STATE['combat']['itemDrop'] = {'I':db.items.index(self.combat.itemDrop['I'])}
    elif(categ == 'C'):
      self.STATE['combat']['itemDrop'] = {'C':db.consumables.index(self.combat.itemDrop['C'])}
    elif(categ == 'ART'):
      self.STATE['combat']['itemDrop'] = {'ART':db.artifact.index(self.combat.itemDrop['ART'])}
    elif(categ == 'ARM'):
      self.STATE['combat']['itemDrop'] = {'ARM':db.armors.index(self.combat.itemDrop['ARM'])}
    elif(categ == 'W'):
      self.STATE['combat']['itemDrop'] = {'W':db.weapons.index(self.combat.itemDrop['W'])}
    self.setState(self.STATE,STATE_IS_WRITING,self.playerName)
    self.exposed_updateCombatState()
    print("combat state saved")
  
  def exposed_updateCombatState(self):
    try:
      self.getState()
      self.combat.syncStats(self.STATE,{
            "skills":db.skills,
            "I":db.items,
            "C":db.consumables,
            "ART":db.artifact,
            "ARM":db.armors,
            "W":db.weapons
          })
      self.exposed_combat = self.STATE['combat']
      self.updatePlayers()
      # print("combat state updated")
    except:
      pass
  
  def exposed_endCombat(self):
    self.exposed_isCombat = False
    self.STATE['isCombat'] = False
    self.setState(self.STATE,STATE_IS_WRITING,self.playerName)
#================================================================
# Player Info
#================================================================

  def exposed_getPlayerName(self):
    return self.playerName
  
  playerName = "" 
  playerPassword = ""
  player = "" # Player class



if __name__ == "__main__":
  hostname = socket.gethostname()
  local_ip = socket.gethostbyname(hostname)

  print(local_ip)
  from rpyc.utils.server import ThreadedServer
  t = ThreadedServer(Game, port=18861,protocol_config = {"allow_public_attrs": True, "sync_request_timeout": 3600,"allow_setattr": True,"allow_delattr": True,})
  t.start()
