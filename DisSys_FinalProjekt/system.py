from calendar import c
from objects import T_E, T_AE, T_A, T_AA, Monster
from objects import S_HP, S_ATK, S_DEF, S_MP, S_AGI
from objects import Player
from math import floor
from random import randint
# import database as db

class Combat:
  # one match, lasts until all enemies die or all players die. Holds all enemies.
  # system needs to constantly refer to this object for win lose stats and player stats update
  def __init__(self,area,players,state,db):
      enemyParty = area.monsterParties[randint(0,(len(area.monsterParties)-1))]
      self.enemies = []
      for e in enemyParty.keys():
        for n in range(enemyParty[e]):
          for m in area.monsters:
            if(m['name'] == e):
              self.enemies.append(Monster(m['name'],m,randint(area.levelRange[0],area.levelRange[0]),m['leveling'],db['skills']['monster']))
      for e in self.enemies:
        self.expDrop = randint(area.expDPE[0],area.expDPE[1])
        self.goldDrop = randint(area.goldDPE[0],area.goldDPE[1])
      whichItem = randint(0,area.totalRate-1)
      self.itemDrop = {}
      while(whichItem <= area.totalRate-1 and whichItem > 0):
        for i in area.dropItems:
          whichItem -= i[1]
          if(whichItem >=0):
            categ = i[0].__class__.__name__
            if(categ == 'Item'):
              categ = 'I'
            elif(categ == 'Consumable'):
              categ = 'C'
            else:
              if(i[0].usage == 'weapon'):
                categ = 'W'
              elif(i[0].usage == 'armor'):
                categ = 'ARM'
              elif(i[0].usage == 'artifact'):
                categ = 'ART'
            self.itemDrop={categ:i[0]}
            break
      self.players = players
      playerss = []
      for p in self.players:
        # state['allPlayerDB'][p].update({"name":p})
        playerss.append(Player(state['allPlayerDB'][p],db))
        playerss[-1].setName(p)
      self.players = playerss
      self.whichPlayer = players[0]
      self.combatLog = f"Monsters have appeared!! now is {self.whichPlayer}'s turn!"
    
  def determineResult(self):
    livingPlayers = 0
    for p in self.players:
      if p.isAlive :
        livingPlayers += 1
    if(livingPlayers == 0):
      self.combatLog+=" The party has been defeated."
      self.result = 'lose'
      
    livingEnemies = 0
    for e in self.enemies:
      if e.isAlive:
        livingEnemies += 1
    if(livingEnemies == 0):
      self.combatLog+=f" The party wins! Obtained {self.expDrop} exp, {self.goldDrop} gold."
      if(self.itemDrop != {}):
        self.combatLog += f'also got {self.itemDrop[0].name}'
      self.result = 'win'
    
  def playerTurn(self,player,action,target,target_index=-1,skill='',item=''): # for successful input only
    index = 0
    for p in self.players:
      if(p.name == self.whichPlayer):
        break
      index+=1
    if(index+1 >= len(self.players)):
      self.whichPlayer = self.players[0].name
    else:
      self.whichPlayer = self.players[index+1].name
    
    print(self.whichPlayer)
    print(self.players[0].name)
    
    if self.whichPlayer == self.players[0].name:
      self.turn = 'enemy'
    
    self.combatLog = ""
    
    AGIcompare = player.status['AGI']/self.enemies[target_index].status['AGI']
    LUKcompare = player.status['LUK']/self.enemies[target_index].status['LUK']
    
    if(action == 'ATTACK'):
      self.combatLog += f"{self.players[0].name} attacks {self.enemies[target_index].name}! "
      times = floor(AGIcompare) if AGIcompare>2 else 1
      crit = False if LUKcompare<0 and randint(1,6)>floor(LUKcompare) else True
      if(crit):
        self.combatLog += "It's a critical!! "
      attacks = []
      for t in range(times):
        critMultiplier = 1 if not crit else 2
        chance = randint(1,6) - 3
        damage = (player.status['ATK'] + chance)*critMultiplier
        damage -= self.enemies[target_index].status['DEF']
        self.combatLog += f"Damage dealt is {damage*-1}!"
        dodge = False if floor(AGIcompare) < 1 and randint(1,6)>floor(self.enemies[target_index].status['AGI']/player.status['AGI']) else True
        if(dodge):
          damage = 0
          self.combatLog = f"{self.players[0].name} attacks {self.enemies[target_index].name}! {self.enemies[target_index].name} dodges!!"
        self.enemies[target_index].applyEffect({'turn':0,'stat':S_HP,'effect':-damage})
        attacks.append(damage)
    elif(action == 'SKILL'):
      self.combatLog += f"{self.players[0].name} uses {skill.name} "
      if(skill.selfEffect['enable']):
        self.players[index].applyEffect(skill.selfEffect)
      if(skill.targetEffect['enable']):
        if(skill.targetEffect['target'] == T_E):
          self.combatLog += f"on {self.enemies[target_index].name}!"
          self.enemies[target_index].applyEffect(skill.targetEffect)
        elif(skill.targetEffect['target'] == T_AE):
          self.combatLog += f"on all enemies!"
          for e in self.enemies:
            e.applyEffect(skill.targetEffect)
        elif(skill.targetEffect['target'] == T_A):
          self.combatLog += f"on {self.players[target_index].name}!"
          self.players[target_index].applyEffect(skill.targetEffect)
        elif(skill.targetEffect['target'] == T_AA):
          self.combatLog += f"on all party members!!"
          for p in self.players:
            p.applyEffect(skill.targetEffect)
    elif(action == 'ITEM'):
      stat = item.effect.keys()[0]
      self.combatLog += f"{self.players[index].name} uses {item.name} on {self.players[target].name}."
      self.players[target].applyEffect({
        'enable': True,'turn': 0,
        'effect': item.effect[stat],
        'stat': stat
      })
      self.players[index].inventory.removeItem(item,'C',1)
    elif(action == 'DEFEND'):
      self.combatLog += f"{self.players[0].name} defends!"
      self.players[index].applyEffect({'enable': True,'effect': 3,'turn': 1,'stat': S_DEF})
    self.determineResult()
    
  def enemyTurn(self):
    self.whichEnemy = 0 if self.whichEnemy >= len(self.enemies) else self.whichEnemy+1
    actions = []
    for a in range(len(self.enemies[self.whichEnemy].skills)):
      actions.append('skill')
    for a in range(5):
      actions.append('attack')
    chosenAct = randint(0,len(actions)-1)
    targetValid = False
    chosenTarget = 0
    while(targetValid == False):
      chosenTarget = randint(0,len(self.players)-1)
      if(self.players[chosenTarget].isAlive):
        targetValid = True
        
    if(actions[chosenAct] == 'attack'):
      AGIcompare = floor(self.enemies[self.whichEnemy].status['AGI']/self.players[chosenTarget].status['AGI'])
      LUKcompare = floor(self.enemies[self.whichEnemy].status['LUK']/self.players[chosenTarget].status['LUK'])
      
      times = floor(AGIcompare) if AGIcompare>2 else 1
      crit = False if LUKcompare<0 and randint(1,6)>floor(LUKcompare) else True
      attacks = []
      for t in range(times):
        critMultiplier = 1 if not crit else 2
        chance = randint(1,6) - 3
        damage = (self.enemies[self.whichEnemy].status['ATK'] + chance)*critMultiplier
        damage -= self.players[chosenTarget].status['DEF']
        dodge = False if floor(AGIcompare) < 1 and randint(1,6)>floor(self.players[chosenTarget].status['AGI']/self.enemies[self.whichEnemy].status['AGI']) else True
        self.players[chosenTarget].applyEffect({'turn':0,'stat':S_HP,'effect':-damage})
        attacks.append(damage)
    else: #skill
      skill = self.enemies[self.whichEnemy].skills[chosenAct]
      if(skill.selfEffect['enable']):
        self.enemies[self.whichEnemy].applyEffect(skill.selfEffect)
      if(skill.targetEffect['enable']):
        if(skill.targetEffect['target'] == T_E):
          self.players[chosenTarget].applyEffect(skill.targetEffect)
        elif(skill.targetEffect['target'] == T_AE):
          for e in self.enemies:
            e.applyEffect(skill.targetEffect)
        elif(skill.targetEffect['target'] == T_A):
          allyValid = False
          chosenAlly = 0
          while(allyValid == False):
            chosenAlly = randint(0,len(self.enemies)-1)
            if(self.enemies[chosenAlly].isAlive):
              allyValid = True
          self.enemies[chosenAlly].applyEffect(skill.targetEffect)
        elif(skill.targetEffect['target'] == T_AA):
          for e in self.enemies:
            e.applyEffect(skill.targetEffect)
    self.determineResult()
    self.turnCounter += 1
    if(self.whichEnemy == 0):
      self.turn = 'player'
    
  def syncStats(self,state,db):
    self.turn = state['combat']['turn']
    self.turnCounter = state['combat']['turnCounter']
    self.players = []
    for p in state['readyToPlayList']:
      # state['allPlayerDB'][p].update({"name":p})
      self.players.append(Player(state['allPlayerDB'][p],db))
      self.players[-1].setName(p)
    self.whichPlayer = state['combat']['whichPlayer']
    for e in range(len(state['combat']['enemies'])):
      self.enemies[e].syncStats(state['combat']['enemies'][e])
    self.whichEnemy = state['combat']['whichEnemy']
    self.result = state['combat']['result']
    self.expDrop = state['combat']['expDrop']
    self.goldDrop = state['combat']['goldDrop']
    self.itemDrop = state['combat']['itemDrop']
    categ = ''
    if(len(list(self.itemDrop.keys()))>0):
      categ = list(self.itemDrop.keys())[0]
    self.itemDrop = {}
    if (categ == 'W' or categ == 'C' or categ == 'I' or categ == 'ARM' or categ == 'ART'):
      self.itemDrop[categ] = db[categ][state['combat']['itemDrop'][categ]]
    self.combatLog = state['combat']['combatLog']
    
  turn = 'player' # player / enemy
  turnCounter = 0
  
  players = []
  whichPlayer = ''
  
  enemies = []
  whichEnemy = 0
  
  result = '' # 'win' or 'lose'
  expDrop = 0
  goldDrop = 0
  itemDrop = {'categ':'the item'} # only one item
  combatLog = ''
  
# EXPLORATION ======================================================================

class Map:
  def __init__(self,map,areaList,traderList,currentLoc,progress,cleared,boundaries):
    self.map = map
    self.boundaries = boundaries
    self.areaList = areaList
    self.traderList = traderList
    self.currentLoc = currentLoc
    self.currentArea = map[currentLoc[0]][currentLoc[1]]
    for p in range(len(progress)):
      self.areaList[p].progress = progress[p]
      self.areaList[p].isCleared = cleared[p]
    
  def traderId(index):
    return (index*-1)-1
  
  def moveParty(self,newLocation):
    self.currentLoc = newLocation
    self.currentArea = self.map[newLocation[0]][newLocation[1]]
  
  currentLoc = [0,0] # y , x
  boundaries = []
  currentArea = 0
  map = []
  areaList = [] #each marked in the map itself
  traderList = [] #each marked by a negative number
  
# TRADING ===========================================================================

class Trader:
  def __init__(self, name, items):
    self.name = name
    self.items = items
  name = ''
  items = {
    'C':[],
    'ARM':[],
    'W':[]
    } #items