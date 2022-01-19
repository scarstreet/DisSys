
class Item:
  def __init__(self,name,desc,price):
    self.name = name
    self.price = price
    self.desc = desc
  name = ''
  price = 0
  desc=''
  
#=================================================================================

class Equipment(Item):
  def __init__(self, name,desc, price,status,usage,role,unlock):
    super().__init__(name, price, desc)
    self.status = status
    self.usage = usage
    self.unlock = unlock
    self.role = role
  unlock = 0
  usage = ''
  role = ''
  equiped = False
  status = {
    'HP':0,
    'MP':0,
    'ATK':0,
    'DEF':0,
    'AGI':0,
    'LUK':0,
  }

#=================================================================================

class Consumable(Item):
  def __init__(self, name, price, desc, effect):
    super().__init__(name, price, desc)
    self.effect = effect
  effect = {
    'HP':0,
    'MP':0,
    'ATK':0,
    'DEF':0,
    'AGI':0,
    'LUK':0,
  }
  
#=================================================================================

class Inventory:
  def __init__(self,*args):
    if(len(args)!=0):
      inventory,db = args[0],args[1]
      #__init__(self,inventory,db):
      for categ in inventory:
        if(categ!='gold'):
          for item in inventory[categ]:
            self.items[categ].append([db[categ][item[0]],item[1]])
      self.gold = inventory['gold']
    
  def removeItem(self,item,type,amount):
    for i in self.items[type]:
      if i[0] == item:
        i[1] -= amount
        if i[1] <= 0:
          self.items[type] = [s for s in self.items[type] if s[0] != item]
        break
      
  def addItem(self,item,type,amount):
    if item not in self.items[type]:
      self.items[type].append([item,0])
    else:
      for i in self.items[type]:
        if(i[0] == item):
          i[1] += amount
          
  items = {
    'I':[],'ART':[],'ARM':[],'W':[],'C':[]
  }
  gold = 0

#=================================================================================

class Player:
  def __init__(self, *args):
    
    if(len(args) == 3):
      in_role,in_status,skills = args[0],args[1],args[2]
      # __init__(self, in_role, in_status, skills):
      self.role = in_role
      self.skills = skills
      self.baseStatus = {
          'HP':in_status['HP'],
          'MP':in_status['MP'],
          'ATK':in_status['ATK'], # base attack
          'DEF':in_status['DEF'], # block
          'AGI':in_status['AGI'], # evasion
          'LUK':in_status['LUK'], # crit
          'LVL':1,
          'EXP':0,
          'EXP_CAP':20,
        }
      self.status = in_status
      self.inventory = Inventory()
      self.resetStatus()
    else:
      playerData,db = args[0],args[1]
      # __init__(self,playerData,db):
      self.role = playerData['role']
      # self.name = playerData['name']
      self.skills = db['skills'][self.role]
      self.baseStatus = playerData['baseStatus']
      self.status = playerData['status']
      if(playerData['equip']['weapon']!=''):
        self.equip['weapon'] = db['W'][playerData['equip']['weapon']]
      if(playerData['equip']['armor']!=''):
        self.equip['armor'] = db['ARM'][playerData['equip']['armor']]
      if(playerData['equip']['artifact']!=''):
        self.equip['artifact'] = db['ART'][playerData['equip']['artifact']]
      self.calcStatus()
      self.inventory = Inventory(playerData['inventory'],db)
    
  def levelUp(self, newStatus, skillToLevel): # triggered when leveling up
    for s in newStatus.keys(): # leveling up base stats
      self.baseStatus[s] = newStatus[s]
    self.baseStatus['EXP_CAP'] = 20*self.baseStatus['LVL']
    self.resetStatus()
    self.status['HP'] = self.equipStatus['HP'] # reset HP
    self.status['MP'] = self.equipStatus['MP'] # reset MP
    
    for s in skillToLevel: #leveling up skills
      for ss in self.skills:
        if ss == s:
          ss.levelUp(1)
    
  def resetStatus(self): # trigerred to reset all status except HP and MP. For exiting battle
    if (self.isAlive != True):
      self.revive()
    self.calcStatus()
    self.effects = []
    self.status['ATK'] = self.equipStatus['ATK']
    self.status['DEF'] = self.equipStatus['DEF']
    self.status['LUK'] = self.equipStatus['LUK']
    self.status['AGI'] = self.equipStatus['AGI']
    
  def removeEffect(self):
    for e in self.effects:
      if(e['turn'] == 0):
        if(e['stat'] != DB_TAUNT):
          self.status[e['stat']] -= e['effect']
    self.effects = [e for e in self.effects if e['turn'] != 0]
  
  def applyEffect(self, effect):
    self.effects.append(effect)
    self.status[effect['stat']] = self.status[effect['stat']]+effect['effect']
    if self.status[effect['stat']]<0:
      self.status[effect['stat']] = 0
      if(self.status['HP']<0):
        self.isAlive = False
    elif self.status[effect['stat']]>self.equipStatus[effect['stat']]:
      self.status[effect['stat']]=self.equipStatus[effect['stat']]
  
  def calcStatus(self): # triggered only to calculate base+equipment
    self.equipStatus = {
      'HP':self.baseStatus['HP'],
      'MP':self.baseStatus['MP'],
      'ATK':self.baseStatus['ATK'],
      'DEF':self.baseStatus['DEF'],
      'AGI':self.baseStatus['AGI'],
      'LUK':self.baseStatus['LUK'],
    }
    
    for e in self.equip:
      if(self.equip[e]!=''):
        for stats in self.equip[e].status.keys():
          self.equipStatus[stats] += self.equip[e].status[stats]
  
  def revive(self):
    self.status['HP'] = 1
    
  def useConsumable(self,item):
    for e in item.effect.keys():
      if (e == 'HP' or e == 'MP'):
        self.status[e] = self.status[e]+item.effect[e] if self.status[e]+item.effect[e]<self.equipStatus[e] else self.equipStatus[e]
      else:
        self.baseStatus[e] += item.effect[e]
      self.calcStatus()
  
  def useEquipment(self,item):
    self.equip[item.usage] = item
    self.calcStatus()
  
  def setName(self,name):
    self.name = name
  
  # VARIABLES
  name = ''
  isAlive = True
  baseStatus = { # Base character status without equipment
    # ====================== basic statuses ========================
    'HP':15,
    'MP':15,
    'ATK':1, # base attack
    'DEF':1, # block
    'AGI':1, # evasion
    'LUK':1, # crit
    # ====================== level statuses ========================
    'LVL':1,
    'EXP':0,
    'EXP_CAP':20,
  }
  equipStatus = { # Character status with equipment. upper threshold
    'HP':15,
    'MP':15,
    'ATK':1,
    'DEF':1,
    'AGI':1,
    'LUK':1,
  }
  status = { # Current character status. During playtime
    'HP':15,
    'MP':15,
    'ATK':1,
    'DEF':1,
    'AGI':1,
    'LUK':1,
  }
  role = ''
  skills = []
  effects = []
  equip = { # The actual item
    'weapon': '',
    'armor': '',
    'artifact': '',
  }
  inventory = [] # should be an inventory class

#=================================================================================

T_E, T_AE, T_A, T_AA = '1enemy', 'allEnemy', '1ally', 'allAlly'
S_HP, S_ATK, S_DEF, S_MP, S_AGI = 'HP', 'ATK', 'DEF', 'MP', 'AGI'
DB_TAUNT = 'taunt'

class Skill:
  def __init__(self,name,MPCost,level,unlock,selfEffect,targetEffect,leveling,desc):
    self.name = name
    self.MPCost = MPCost
    self.level = 1
    self.unlock = unlock
    self.selfEffect = selfEffect
    self.targetEffect = targetEffect
    self.leveling = leveling
    self.desc = desc
    self.levelUp(level)
  name = ''
  MPCost = 0
  level = 0
  unlock = 0
  selfEffect = {
    'enable': False,
    'effect': 0,
    'turn': 0,
    'stat': '',
  }
  targetEffect = {
    'enable': False,
    'target': '',
    'effect': 0,
    'turn': 0,
    'stat': '',
  }
  leveling = {
    'modulus': 1,
    'self': {
      'effect': 0,
      'turn': 0,
    },
    'target': {
      'effect': 0,
      'turn': 0,
    },
  }
  desc = ''

  def levelUp(self,level):
    self.level += level
    while(level > 0):
      if(self.leveling['modulus'] == 1):
        self.targetEffect['turn'] += self.leveling['target']['turn']
        self.targetEffect['effect'] += self.leveling['target']['effect']
        self.selfEffect['turn'] += self.leveling['self']['turn']
        self.selfEffect['effect'] += self.leveling['self']['effect']
      else:
        mod = level%self.leveling['modulus']
        toUpgrade = list(self.leveling['target'].keys())[mod]
        self.targetEffect[toUpgrade] += self.leveling['target'][toUpgrade]
        self.selfEffect[toUpgrade] += self.leveling['self'][toUpgrade]
      level -= 1

#=================================================================================

class Monster:
  def __init__(self,name,type,level,leveling,skills):
    self.name = name
    self.image = type['image']
    self.level = level
    multiplier = int(level/leveling['div']) if level/leveling['div'] > 0 else 1
    for s in type['status'].keys():
      self.status[s] = type['status'][s] + multiplier*leveling['status'][s]
    self.baseStatus = self.status
    for s in type['skills']:
      self.skills.append(skills[s])
    for s in self.skills:
      s.levelUp(level)
      
  def removeEffect(self):
    for e in self.effects:
      if(e['turn'] == 0):
        if(e['stat'] != DB_TAUNT):
          self.status[e['stat']] -= e['effect']
    self.effects = [e for e in self.effects if e['turn'] != 0]
  
  def applyEffect(self, effect):
    self.effects.append(effect)
    self.status[effect['stat']] = self.status[effect['stat']]+effect['effect']
    if self.status[effect['stat']]<0:
      self.status[effect['stat']] = 0
      if(self.status['HP']<0):
        self.isAlive = False
    elif self.status[effect['stat']]>self.baseStatus[effect['stat']]:
      self.status[effect['stat']]=self.baseStatus[effect['stat']]
  
  def syncStats(self,state):
    self.isAlive = state['isAlive']
    self.level = state['level']
    self.status = state['status']
    self.baseStatus = state['baseStatus']
    self.effects = state['effects']
  
  name = ''
  level = 0
  isAlive = True
  skills = []
  effects = []
  baseStatus = {
    
  }
  status = {
    'HP':1,
    'MP':1,
    'ATK':1, # base attack
    'DEF':1, # block
    'AGI':1, # evasion
    'LUK':1, # crit
  }
  image = ''

#=================================================================================