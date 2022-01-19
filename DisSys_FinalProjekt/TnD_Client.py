import rpyc
import random
import os
import math
import time

border = "\n====================================================================================\n"

def clear():
  print()
  input('enter anything to continue')
  os.system('cls' if os.name == 'nt' else 'clear')

def connect():
  connected = False
  while(not connected): # First time connecting
    tryagain = 0
    ip = input('Please insert ip address of server : ')
    if(len(ip)==0):
      ip = '192.168.50.249'
    while(tryagain<15):
      try:
        GAME = rpyc.connect(ip, 18861,config = {"allow_public_attrs": True, "sync_request_timeout": 3600,"allow_setattr": True,"allow_delattr": True,})
        tryagain = 0
        connected = True
        print('Connected!')
        clear()
        return GAME
      except:
        tryagain +=1
    print('Somethings wrong with the connection or IP adress wrong.')
    print('Please try again later')
    input()
  clear()

def newPlayer():
  input("Welcome to TERMINAL QUEST, new blood. Where this quest maybe your last.")
  input("Not everyone were lucky enough to escape this land alive, in fact many have died.")
  input("It's now all up to you and the others to cleanse these lands from evil.")
  print()
  input("Let's get you ready. First of all, what is your class?")
  print("==== MAGE(M) ====")
  print("a master of the arcane arts. Using magic to strike down your enemies.")
  print("==== WARRIOR(W) ====")
  print("a blade wielder. Brute strength is your path to victory.")
  print("==== CLERIC(C) ====")
  print("one of those who chosen by God to heal and protect.")
  print("==== ROGUE(R) ====")
  print("a swift and fighter who lurks in the shadows to wait for their chance.")
  print()
  print(border)
  roleValid = False
  role = ''
  while(not roleValid):
    role = input("So, what is your role? [M/W/C/R]")
    if(role == 'M'):
      role = 'mage'
      roleValid = True
    elif (role == 'W'):
      role = 'warrior'
      roleValid = True
    elif(role == 'C'):
      role = 'cleric'
      roleValid = True
    elif(role == 'R'):
      role = 'rogue'
      roleValid = True
    else:
      print('Inputted role invalid.')
  print(border)
  print()
  input(f"So, a {role}, eh? Very well. Now time to assess your abilities.")
  input(f"In this world, you are given a few attributes")
  print()
  print(f"==== HP ====")
  print(f"Health Points, to determine your life force. The more you have, the more suffering you'll be able to receive.")
  print(f"==== MP ====")
  print(f"Magic Points, to determine your ability to cast spells. The more you have, the more spells you'll be able to cast.")
  print(f"==== ATK ====")
  print(f"The amount of damage that you can deal per attack. A measure of your physical power.")
  print(f"==== AGI ====")
  print(f"A measure of your physical speed. The more you have the faster your attacks become and the better you will be on dodging attacks.")
  print(f"==== DEF ====")
  print(f"How well you are able to defend yourself. The more you have, the less pain would be inflicted to your HP when taking in attacks.")
  print(f"==== LUK ====")
  print(f"How lucky you are. To determine if your attacks would luckily inflict a critical damage toward your enemies")
  print()
  assignedDone = False
  balance = 10
  status = {
    "HP": 15,
    "MP": 15,
    "ATK": 1,
    "DEF": 1,
    "AGI": 1,
    "LUK": 1,
  }
  while(not assignedDone):
    print(border)
    print()
    print("Currently, these are your statuses : ")
    print(f"HP : {status['HP']} || MP : {status['MP']} || ATK : {status['ATK']} || DEF : {status['DEF']} || AGI : {status['AGI']} || LUK : {status['LUK']}")
    print()
    print("To increase or decrease them, name the status and how much you'd like to increase or decrease to it. (eg:[HP + 2])")
    print(f"Your remaining balance is {balance}",end='. ')
    if(balance == 0):
      print('To end assessment, press enter.')
    print()
    change = input("Input status to edit : ")
    if((balance==0 and change != '') or balance>0):
      change = change.split(' ')
      if(len(change)==3):
        change[2] = int(change[2])
        if(change[0] in status.keys()):
          if(change[1]=='-'):
            change[2]*=-1
          if(status[change[0]]+change[2]>0 and balance-change[2]>=0):
            status[change[0]] += change[2]
            balance -=change[2]
          else:
            print("Numerical input bad.")
            continue
      else:
        print("Format bad.")
    if(balance == 0):
      print(border)
      print("Currently, these are your statuses : ")
      print(f"HP : {status['HP']} || MP : {status['MP']} || ATK : {status['ATK']} || DEF : {status['DEF']} || AGI : {status['AGI']} || LUK : {status['LUK']}")
      print()
      doneValid = False
      while(not doneValid):
        done = input("Are you done assigning your statuses?[Y/N]")
        if(done != 'N' and done != 'Y'):
          print("Bad input.")
        else:
          assignedDone = False if done == 'N' else True
          doneValid = True
  print(border)
  GAME.root.newPlayer(role,status)
  print('Your assessment has been recorded')
  print()
  input('enter anything to continue')
  os.system('cls' if os.name == 'nt' else 'clear')
  
def register():
  os.system('cls' if os.name == 'nt' else 'clear')
  registered = False
  while(not registered):
    username = input("Username : ")
    password = input("Password : ")
    GAME.root.register(username,password)
    
    if(not GAME.root.loggedIn):
      print(f'Wrong password for account {username}. Please try again.')
      continue
    if(not GAME.root.registered):
      print(f'Ah, new blood. We welcome you, {username}')
      newPlayer()
    else:
      print(f'We welcome you, {username}')
    registered = True
  clear()

def join():
  print(border)
  if(not GAME.root.roomFull): # check room full or not
    input("Enter anything to join current TERMINAL QUEST party.")
  else:
    print("The current party is full. Please wait until someone leaves the current party.")
    print("Keep the terminal open and we will notify you when you can enter")
    print()
    print()
    print("Waiting...")
    while(GAME.root.roomFull):
      GAME.root.waitVacant()
    print("Now able to join room.")
    input("Enter anything to join current TERMINAL QUEST party.")
  GAME.root.ready()
  print(border)
  if(not GAME.root.roomFull):
    print("Waiting for party to form...")
    while(not GAME.root.roomFull):
      GAME.root.waitFull()
  print("\n\nTERMINAL QUEST shall start now.\n\n")
  print(border)
  clear()

def moveParty(myName,currentLoc,boundary):
  dirGood = False
  while(not dirGood):
    print("Where to? Up[U] / Down [D] / Left [L] / Right [R]")
    dir = input()
    if(dir == 'U'):
      if(currentLoc[0]-1>=0 and currentLoc[0]-1<boundary):
        GAME.root.mapMoveTo([currentLoc[0]-1,currentLoc[1]])
        dirGood = True
      else:
        print("Bad input : Movement out of bounds.")
    elif(dir == 'D'):
      if(currentLoc[0]+1>=0 and currentLoc[0]+1<boundary):
        GAME.root.mapMoveTo([currentLoc[0]+1,currentLoc[1]])
        dirGood = True
      else:
        print("Bad input : Movement out of bounds.")
    elif(dir == 'L'):
      if(currentLoc[1]-1>=0 and currentLoc[1]-1<boundary):
        GAME.root.mapMoveTo([currentLoc[0],currentLoc[1]-1])
        dirGood = True
      else:
        print("Bad input : Movement out of bounds.")
    elif(dir == 'R'):
      if(currentLoc[1]+1>=0 and currentLoc[1]+1<boundary):
        GAME.root.mapMoveTo([currentLoc[0],currentLoc[1]+1])
        dirGood = True
      else:
        print("Bad input : Movement out of bounds.")
    else:
      print("Bad input : Invalid direction indicator.")
  os.system('cls' if os.name == 'nt' else 'clear')

def explore():
  GAME.root.initMap()
  myName = GAME.root.getPlayerName()
  isPlaying = True
  #intro
  print()
  print(f"Welcome {myName}. We've been waiting for you.")
  print()
  while(isPlaying):
    if(GAME.root.isCombat):
      def printEnemies(combat):
        for e in range(len(combat.enemies)):
          print(combat.enemies[e].image.center(20,' '),end="  ")
        print("\n",end='')
        for e in range(len(combat.enemies)):
          print(' '.center(20,' '),end="||")
        print("\n",end='')
        for e in range(len(combat.enemies)):
          print(f"{combat.enemies[e].name} [{e}]".center(20,' '),end="||")
        print("\n",end='')
        for e in range(len(combat.enemies)):
          print(f"HP | {combat.enemies[e].status['HP']}".center(20,' '),end="||")
        print("\n",end='')
        for e in range(len(combat.enemies)):
          print(f"MP | {combat.enemies[e].status['MP']}".center(20,' '),end="||")
        print("\n",end='')
      def printPlayers():
        for p in combat.players:
            print()
            index = combat.players.index(p)
            print(f"{GAME.root.STATE['readyToPlayList'][index]}".center(14," "),end="||")
            print(f"{p.status['HP']}/{p.baseStatus['HP']}",end="")
            if(GAME.root.STATE['readyToPlayList'][index] == combat.whichPlayer):
              print("      Attack[A]   Skill[S]   Defend[D]   Item[I]".center(30," "))
              player = p
            else:
              print()
            print(f"{p.role}".center(14," "),end="||")
            print(f"{p.status['MP']}/{p.baseStatus['MP']}")
            print("====================================================================================")
      def printSkills(player):
        skillInitials = []
        for skill in player.skills: #just printing skills
          # print(player.baseStatus)
          if(skill.unlock <= player.baseStatus['LVL']):
            initial = ''
            for sn in skill.name.split(" "):
              initial += list(sn)[0]
            skillInitials.append(skillInitials)
            print(f"{skill.name} Lvl.{skill.level}[{initial}]")
            print()
            print(f"{skill.desc}")
            turn = f", Turn : {skill.targetEffect['turn']}."
            print(f"MP cost : {skill.MPCost}{ turn if skill.targetEffect['turn']!=0 else ''}")
            if(skill.targetEffect['enable']):
              print(f"{skill.targetEffect['target']} {skill.targetEffect['stat']}",end="")
              if(skill.targetEffect['effect']>0):
                print(f" +{skill.targetEffect['effect']}")
              else:
                print(f" -{skill.targetEffect['effect']}")
            print("====================================================================================")
        return skillInitials
      print("TIME TO FIGHT!!")
      input()
      os.system('cls' if os.name == 'nt' else 'clear')
      # update own combat class
      # Get combat log
      GAME.root.updateCombatState()
      combat = GAME.root.combat
      
      index = 0
      for p in range(len(combat.players)):
        if(combat.players[p].name == combat.whichPlayer):
          index = p
      player = combat.players[index]
      print(combat.combatLog)
      print(border)
      turn = True
      do = ''
      while(turn):
        if(do == ''):
          printEnemies(combat)
          printPlayers()       
        elif(do == 'S'):
          printEnemies(combat)
          skillInitials = printSkills(player)
          
          whichSkill=''
          skillBad = True
          while(skillBad): #choosing the skill
            whichSkill = input(f'Which skill?{str(skillInitials)}')
            if(whichSkill not in skillInitials):
              print("Selected skill unavailable")
            else:
              skillBad = False
          skill = player.skills[skillInitials.index(whichSkill)]
          
          targetBad = True
          target=0
          #choosing target. many options
          if(skill.targetEffect['target'] == '1enemy'):
            while(targetBad):
              for e in range(len(combat.enemies)):
                print(f"{combat.enemies[e].name}[{e}],",end=" ")
              print()
              target = input("who to apply skill?")
              if(target not in range(len(combat.enemies)) or combat.enemies[target].isAlive == False):
                print("Chosen target bad.")
              else:
                targetBad = False
            combat.playerTurn(player,'SKILL',skill.targetEffect['target'],target,skill=skill)
          elif(skill.targetEffect['target'] == '1ally'):
            while(targetBad):
              for e in range(len(combat.players)):
                print(f"{combat.players[e].name}[{e}],",end=" ")
                print()
                target = input("who to apply skill?")
                if(target not in range(len(combat.players)) or combat.players[target].isAlive == False):
                  print("Chosen target bad.")
                else:
                  targetBad = False
            combat.playerTurn(player,'SKILL',skill.targetEffect['target'],target,skill=skill)
          else:
            combat.playerTurn(player,'SKILL',skill.targetEffect['target'],target,skill=skill)
          turn = False
        elif(do == 'I'):
          rows = math.ceil(len(player.inventory.items['C'])/4)
          indexes = []
          for r in range(rows):
            for n in range(4):
              if(r*4+n < len(player.inventory.items['C'])):
                i = player.inventory.items['C'][r*4+n]
                print(f"{i[0].name}({i[1]}),[{r*4+n}]".center(15," "),end="||")
                indexes.append(r*4+n)
            print()
            for n in range(4):
              if(r*4+n < len(player.inventory.items['C'])):
                i = player.inventory.items['C'][r*4+n]
                effect = list(i[0].effect.keys())[0]
                print(f"{effect} + {i[0].effect[effect]}".center(15," "),end="||")
            print()
            print("====================================================================================")
            print()
            whichItem = -1
            indexBad = True
            while(indexBad):
              whichItem = input(f"Which item would you like to use?{indexes}")
              if whichItem not in indexes:
                print("Bad Index.")
              else:
                indexBad = False
            targetBad = True
            target = e
            while(targetBad):
              for e in range(len(combat.players)):
                print(f"{combat.players[e].name}[{e}],",end=" ")
                print()
                target = input("who to apply skill?")
                if(target not in range(len(combat.players)) or combat.players[target].isAlive == False):
                  print("Chosen target bad.")
                else:
                  targetBad = False
            combat.playerTurn(player,'ITEM','',target,skill='',item=player.inventory.items['C'][whichItem][0])
        # wait until turn=================================================================
        if(combat.turn == 'player'):
          if(combat.whichPlayer == myName):
            GAME.root.saveCombatState()
            if(do == ''):
              actionBad = True
              while(actionBad):
                action = input("Now is your turn! Whiat will you do?")
                if(action == 'A'):
                  targetBad = True
                  while(targetBad):
                    target = int(input("Attack which enemy?"))
                    if(target not in range(len(combat.enemies)) or combat.enemies[target].isAlive == False):
                      print("Target bad.")
                    else:
                      GAME.root.combat.playerTurn(
                        player,"ATTACK", "1enemy", target
                      )
                      targetBad = turn = actionBad = False
                elif(action == 'S' or action == 'I'):
                  # do = action
                  # actionBad = False
                  pass
                elif(action == 'D'):
                  GAME.root.combat.playerTurn(
                      player,
                      "DEFEND", "", -1
                    )
                  actionBad = turn = False
                else:
                  print("Selected option unavailable.")
              print("No.. you're still too weak. We will retreat.")
              GAME.root.endCombat()
          else:
            print(f"Now is {combat.whichPlayer}'s turn.")
            whoseTurn = combat.whichPlayer
            while(GAME.root.combat.whichPlayer == whoseTurn):
              GAME.root.updateCombatState()
              combat = GAME.root.combat
            turn = False
        else: # TODO - enemy turn
          print(f"Now is {combat.enemies[combat.whichEnemy].name}'s turn.")
          whoseTurn = combat.whichEnemy
          while(GAME.root.combat.whichEnemy == whoseTurn):
            GAME.root.updateCombatState()
          turn = False
        # keep updating
        # it's my turn
        # attack / defend / skills / item 
        # TODO - client side combat
        GAME.root.saveCombatState()
        continue
      continue
    elif(GAME.root.isTrading):
      print("ARRIVED AT A TOWN.")
    currentLoc = GAME.root.currentLoc
    boundary = 12
    #show map
    print()
    for line in GAME.root.mapVisuals:
      print(line)
    print()
    if(GAME.root.movementTurn == myName): #if my turn, do something
      print("It's now your turn. Select what to do: ")
      # options = inventory, move, check map, check party
      action = input("Inventory[I] / Move[M] / Check Map [CM] / Check Party [CP]\n")
      if(action == 'M'):
        moveParty(myName,currentLoc,boundary)
      else:
        input("Sorry, Action invalid for now.")
        clear()
    else: #else, wait for my turn
      whoseTurn = GAME.root.movementTurn
      print(f"It is currently someone else's turn to make a move. Please wait for your turn")
      while(GAME.root.movementTurn == whoseTurn):
        GAME.root.waitForAction()
      os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
  print("WELCOME TO TERMINAL QUEST")
  GAME = connect()
  register()
  join()
  explore()
  
  while(True):
    GAME.root.waitGet()

# ============== MY TO DO LIST  ======================================
# connected, save own id
# display start screen
# create character
# wait for other players
# waiting complete
# display intro
# display map screen 
#   can choose direction
#   TODO - view other players
#   TODO - open inventory
# wait for other player's decision

# TODO - fight!!
# TODO - wait for turn
# TODO - it's our turn, take action
# TODO - win or lose, get exp or revive (area progess-1)

# TODO - trading!!

# TODO - keep fighting untill all areas cleared

# end game