from objects import T_E, T_AE, T_A, T_AA
from objects import S_HP, S_ATK, S_DEF, S_MP, S_AGI
from objects import DB_TAUNT

state_list = ['battle','narative']
from objects import Skill
SKILL_POISON, SKILL_WARCRY, SKILL_HEAL, SKILL_FIREBALL = 0, 1, 2, 3
skills = {
  # MAGE (1,3,4,7)==================================================
  'mage' : [
    Skill(
      name = 'Mana Hail', MPCost= 3, level= 1, unlock= 1,
      selfEffect= {'enable': False,'effect': 0,'turn': 0,'stat': '',},
      targetEffect= {'enable': True,'target': T_AE,'effect': -3,'turn': 0,'stat': S_HP},
      leveling = {'modulus':1,'self':{'effect':0,'turn':0},'target':{'effect':-1,'turn':0}},
      desc= 'Rain damaging mana from above all your enemies.'
    ),
    Skill(
      name = 'Mana Missile', MPCost= 4, level= 1, unlock= 3,
      selfEffect= {'enable': False,'effect': 0,'turn': 0,'stat': '',},
      targetEffect= {'enable': True,'target': T_E,'effect': -2,'turn': 0,'stat': S_HP},
      leveling = {'modulus':1,'self':{'effect':0,'turn':0},'target':{'effect':-1,'turn':0}},
      desc= 'Fire concentrated mana to pierce one enemy.'
    ),
    Skill(
      name = 'Enhancement', MPCost= 2, level= 1, unlock= 4,
      selfEffect= {'enable': False,'effect': 0,'turn': 0,'stat': ''},
      targetEffect= {'enable': True,'target': T_A,'effect': 2,'turn': 3,'stat': S_ATK},
      leveling = {'modulus':2,'self':{'effect':0,'turn':0},'target':{'effect':1,'turn':1}},
      desc= 'Focus your magic to increase the ATK of one of your ally.'
    ),
    Skill(
      name = 'Soul Conversion', MPCost= 1, level= 1, unlock= 7,
      selfEffect= {'enable': True,'effect': 5,'turn': 1,'stat': S_MP},
      targetEffect= {'enable': True,'target': T_E,'effect': -1,'turn': 0,'stat': S_HP},
      leveling = {'modulus':1,'self':{'effect':0,'turn':0},'target':{'effect':-1,'turn':0}},
      desc= "Steal a small amount of damage to one enemy's soul and use it to replenish your own mana."
    ),
  ],
  # CLERIC (1,3,4,8)================================================
  'cleric': [
    Skill(
      name = 'Heal', MPCost= 3, level= 1, unlock= 1,
      selfEffect= {'enable': False,'effect': 0,'turn': 0,'stat': '',},
      targetEffect= {'enable': True,'target': T_A,'effect': 5,'turn': 0,'stat': S_HP},
      leveling = {'modulus':1,'self':{'effect':0,'turn':0},'target':{'effect':1,'turn':0}},
      desc='Use magic to heal one ally.'
    ),
    Skill(
      name = 'Replenishing Mist', MPCost= 4, level= 1, unlock= 3,
      selfEffect= {'enable': False,'effect': 0,'turn': 0,'stat': '',},
      targetEffect= {'enable': True,'target': T_AA,'effect': 3,'turn': 0,'stat': S_HP},
      leveling = {'modulus':1,'self':{'effect':0,'turn':0},'target':{'effect':1,'turn':0}},
      desc='Heal all allies using a mist that covers the battlefield.'
    ),
    Skill(
      name = 'Holy Shield', MPCost= 4, level= 1, unlock= 4,
      selfEffect= {'enable': False,'effect': 0,'turn': 0,'stat': '',},
      targetEffect= {'enable': True,'target': T_AA,'effect': 2,'turn': 3,'stat': S_DEF},
      leveling = {'modulus':2,'self':{'effect':0,'turn':0},'target':{'effect':1,'turn':1}},
      desc='Pray to summon holy shield to increase defense of all allies.'
    ),
    Skill(
      name = 'Divine Protection', MPCost= 5, level= 1, unlock= 8,
      selfEffect= {'enable': False,'effect': 0,'turn': 0,'stat': '',},
      targetEffect= {'enable': True,'target': T_A,'effect': 4,'turn': 1,'stat': S_DEF},
      leveling = {'modulus':1,'self':{'effect':0,'turn':0},'target':{'effect':1,'turn':0}},
      desc='Pray to protect one ally by increasing their defense by a significant amount for one turn.'
    ),
  ],
  # WARRIOR (2,4,6,9)===============================================
  'warrior':[
    Skill(
      name = 'WarCry', MPCost= 0, level= 1, unlock= 2,
      selfEffect= {'enable': True,'effect': 2,'turn': 3,'stat': S_ATK,},
      targetEffect= {'enable': False,'target': '','effect': 0,'turn': 0,'stat': ''},
      leveling = {'modulus':2,'self':{'effect':1,'turn':1},'target':{'effect':0,'turn':0}},
      desc='Let out a warcry to boost your own ATK'
    ),
    Skill(
      name = 'Strike', MPCost= 3, level= 1, unlock= 4,
      selfEffect= {'enable': False,'effect': 0,'turn': 0,'stat': '',},
      targetEffect= {'enable': True,'target': T_E,'effect': -3,'turn': 0,'stat': S_HP},
      leveling = {'modulus':1,'self':{'effect':0,'turn':0},'target':{'effect':-1,'turn':0}},
      desc='Swiftly strike one enemy with a tactical strike.'
    ),
    Skill(
      name = 'Break Armor', MPCost= 6, level= 1, unlock= 6,
      selfEffect= {'enable': False,'effect': 0,'turn': 0,'stat': '',},
      targetEffect= {'enable': True,'target': T_E,'effect': -5,'turn': 5,'stat': S_DEF},
      leveling = {'modulus':2,'self':{'effect':0,'turn':0},'target':{'effect':-1,'turn':1}},
      desc='Destroy the DEF of an enemy by a huge amount.'
    ),
    Skill(
      name = 'Intimidate', MPCost= 4, level= 1, unlock= 9,
      selfEffect= {'enable': False,'effect': 0,'turn': 0,'stat': '',},
      targetEffect= {'enable': True,'target': T_AE,'effect': -2,'turn': 3,'stat': S_ATK},
      leveling = {'modulus':1,'self':{'effect':0,'turn':0},'target':{'effect':-1,'turn':1}},
      desc='Let out an intimidating cry to lower enemy morale, weakening their ATK.'
    ),
  ],
  # ROGUE (2,3,5,7)=================================================
  'rogue': [
    Skill(
      name = 'Focus', MPCost= 2, level= 1, unlock= 2,
      selfEffect= {'enable': True,'effect': 2,'turn': 3,'stat': S_AGI,},
      targetEffect= {'enable': False,'target': '','effect': 0,'turn': 0,'stat': ''},
      leveling = {'modulus':2,'self':{'effect':1,'turn':1},'target':{'effect':0,'turn':0}},
      desc='Observe the enemy movements to increase your own agility.'
    ),
    Skill(
      name = 'Taunt', MPCost= 1, level= 1, unlock= 3,
      selfEffect= {'enable': True,'effect': 0,'turn': 2,'stat': DB_TAUNT,},
      targetEffect= {'enable': True,'target': T_AE,'effect': 0,'turn': 2,'stat': DB_TAUNT},
      leveling = {'modulus':1,'self':{'effect':1,'turn':1},'target':{'effect':1,'turn':1}},
      desc='Taunt all enemies to attack you.'
    ),
    Skill(
      name = 'Cherry Bombs', MPCost= 4, level= 1, unlock= 5,
      selfEffect= {'enable': False,'effect': 0,'turn': 0,'stat': '',},
      targetEffect= {'enable': True,'target': T_AE,'effect': -2,'turn': 0,'stat': S_HP},
      leveling = {'modulus':1,'self':{'effect':0,'turn':0},'target':{'effect':-1,'turn':0}},
      desc='Throw bombs to all enemies dealing damage to all of them.'
    ),
    Skill(
      name = 'Poison', MPCost= 3, level= 1, unlock= 7,
      selfEffect= {'enable': False,'effect': 0,'turn': 0,'stat': '',},
      targetEffect= {'enable': True,'target': T_E,'effect': -1,'turn': 3,'stat': S_HP},
      leveling = {'modulus':2,'self':{'effect':0,'turn':0},'target':{'effect':-1,'turn':1}},
      desc='Poison an enemy, inflicting damage to them for a few turns.'
    ),
  ],
  # MONSTER ========================================================
  'monster': [
    Skill(
      name = 'Poison', MPCost= 3, level= 1, unlock= 9,
      selfEffect= {'enable': False,'effect': 0,'turn': 0,'stat': '',},
      targetEffect= {'enable': True,'target': T_E,'effect': -1,'turn': 3,'stat': S_HP},
      leveling = {'modulus':2,'self':{'effect':0,'turn':0},'target':{'effect':-1,'turn':1}},
      desc='Poison an enemy, inflicting damage to them for a few turns.'
    ),
    Skill(
      name = 'WarCry', MPCost= 0, level= 1, unlock= 2,
      selfEffect= {'enable': True,'effect': 2,'turn': 3,'stat': S_ATK,},
      targetEffect= {'enable': False,'target': '','effect': 0,'turn': 0,'stat': ''},
      leveling = {'modulus':2,'self':{'effect':1,'turn':1},'target':{'effect':0,'turn':0}},
      desc='Let out a warcry to boost your own ATK'
    ),
    Skill(
      name = 'Heal', MPCost= 3, level= 1, unlock= 5,
      selfEffect= {'enable': False,'effect': 0,'turn': 0,'stat': '',},
      targetEffect= {'enable': True,'target': T_A,'effect': 5,'turn': 0,'stat': S_HP},
      leveling = {'modulus':1,'self':{'effect':0,'turn':0},'target':{'effect':1,'turn':0}},
      desc='Use magic to heal one ally.'
    ),
    Skill(
      name = 'Fireball', MPCost= 4, level= 1, unlock= 5,
      selfEffect= {'enable': False,'effect': 0,'turn': 0,'stat': '',},
      targetEffect= {'enable': True,'target': T_E,'effect': -2,'turn': 0,'stat': S_HP},
      leveling = {'modulus':1,'self':{'effect':0,'turn':0},'target':{'effect':-1,'turn':0}},
      desc= 'Fire concentrated mana to pierce one enemy.'
    ),
  ]
}
map = [ # negative numbers are traders
    [ 0,  0,  0,  1,  1,  1,  1,  1,  1,  5,  5,  5],
    [ 0,  0, -1,  1,  1,  1,  1,  1,  1,  5,  5,  5],
    [ 0,  0,  1,  1,  1,  1,  3,  1,  1,  5,  5,  5],
    [ 0,  0,  1,  1,  1,  3,  3,  3, -3,  5,  5,  5],
    [ 0,  0,  0,  1,  1,  3,  3,  3,  4,  4,  5,  4],
    [ 0,  0,  0,  1,  3,  3,  3,  3,  4,  4,  5,  4],
    [ 0,  0,  2,  2,  3,  3,  3,  3,  3,  4,  4,  4],
    [ 2,  2,  2,  2,  2,  2,  3,  3,  3,  4,  4,  4],
    [ 2,  2,  2,  2,  2, -2,  3,  3,  3,  4,  4,  4],
    [ 2,  2,  2,  2,  2,  2,  2,  2,  4,  4,  4,  4],
    [ 2,  2,  2,  2,  2,  2,  2,  4,  4,  4,  4,  4],
    [ 2,  2,  2,  2,  2,  2,  2,  4,  4,  4,  4,  4],
  ]

mapVisual = [
"           |                       |           ",
"        ___| Zombified Village     |   Mount   ",
"       | D |                       |           ",
"       |___|  -11-      ___        | Grimfate  ",
"       |               |   |       |           ",
"       |            ___|   |_______|  -55-     ",
"       |           |           | H |           ",
"  -00- |___        |           |___|___     ___",
"           |       |           |       |   |   ",
"Begining's |    ___|  -33-     |       |   |   ",
"           |   |               |       |   |   ",
"Plains  ___|___| Dusted Caverns|___    |___|   ",
"       |       |                   |           ",
"_______|       |_______            |           ",
"                       |           |           ",
"  Rotting Forest    ___|           |           ",
"                   | P |           |           ",
"  -22-             |___|___________|  -44-     ",
"                               |               ",
"                            ___| Warlock's Bog ",
"                           |                   ",
"                           |                   ",
"                           |                   ",
]

from objects import Item
I_SR,I_SA,I_GR,I_GA,I_JR,I_JA = 0,1,2,3,4,5
items = [
  Item(name='Silver Ring',desc='Treasure. Not useful for you.',price=20),
  Item(name='Silver Amulet',desc='Treasure. Not useful for you.',price=35),
  Item(name='Golden Ring',desc='Treasure. Not useful for you.',price=35),
  Item(name='Golden Amulet',desc='Treasure. Not useful for you.',price=40),
  Item(name='Jeweled Ring',desc='Treasure. Not useful for you.',price=60),
  Item(name='Jeweled Amulet',desc='Treasure. Not useful for you.',price=80),
]

from objects import Equipment
ART_HP1,ART_HP2,ART_MP1,ART_MP2,ART_ATK1,ART_ATK2,ART_DEF1,ART_DEF2,ART_AGI1,ART_AGI2,ART_LUK1,ART_LUK2 = 0,1,2,3,4,5,6,7,8,9,10,11
artifact = [
  Equipment(name="Garnet Amulet",price=200,usage='artifact',role='',
          status={'HP':5}, unlock = 0,
          desc=''),
  Equipment(name="Ruby Amulet",price=800,usage='artifact',role='',
          status={'HP':10}, unlock = 7,
          desc=''),
  
  Equipment(name="Lapis Lazuli Amulet",price=200,usage='artifact',role='',
          status={'MP':5}, unlock = 0,
          desc=''),
  Equipment(name="Sapphire Amulet",price=800,usage='artifact',role='',
          status={'MP':10}, unlock = 7,
          desc=''),
  
  Equipment(name="Imp's Tooth",price=200,usage='artifact',role='',
          status={'ATK':2}, unlock = 0,
          desc=''),
  Equipment(name="Demon's Horn",price=800,usage='artifact',role='',
          status={'ATK':4}, unlock = 7,
          desc=''),
  
  Equipment(name="Blessed Token",price=200,usage='artifact',role='',
          status={'DEF':2}, unlock = 0,
          desc=''),
  Equipment(name="Sacred Token",price=800,usage='artifact',role='',
          status={'DEF':4}, unlock = 7,
          desc=''),
  
  Equipment(name="Crow's feather",price=200,usage='artifact',role='',
          status={'AGI':2}, unlock = 0,
          desc=''),
  Equipment(name="Harpy's feather",price=800,usage='artifact',role='',
          status={'AGI':4}, unlock = 7,
          desc=''),
  
  Equipment(name="Three Leaf Clover",price=200,usage='artifact',role='',
          status={'LUK':2}, unlock = 0,
          desc=''),
  Equipment(name="Six Leaf Clover",price=800,usage='artifact',role='',
          status={'LUK':4}, unlock = 7,
          desc=''),
]

ARM_M1,ARM_M2,ARM_M3,ARM_C1,ARM_C2,ARM_C3,ARM_W1,ARM_W2,ARM_W3,ARM_R1,ARM_R2,ARM_R3 = 0,1,2,3,4,5,6,7,8,9,10,11
armors = [
  Equipment(name='Scholar Cloak',price=300,usage='armor',role='mage',
            status={'DEF':1,'MP':4}, unlock =3,
            desc=''),
  Equipment(name='Infused Cloak',price=1000,usage='armor',role='mage',
            status={'DEF':2,'MP':8}, unlock =7,
            desc=''),
  Equipment(name='Manacule Cloak',price=2200,usage='armor',role='mage',
            status={'DEF':3,'MP':10}, unlock =15,
            desc=''),
  
  Equipment(name='Pilgrimage Robes',price=300,usage='armor',role='cleric',
            status={'DEF':2,'MP':2}, unlock =3,
            desc='Robes used during pilgrimages. Light and helps focus on meditation and prayers.'),
  Equipment(name='Blessed Robes',price=1000,usage='armor',role='cleric',
            status={'DEF':4,'MP':4}, unlock =7,
            desc='Robes blessed by the gods. Only given to those who are worthy.'),
  Equipment(name='Sacred Robes',price=2200,usage='armor',role='cleric',
            status={'DEF':5,'MP':6}, unlock =15,
            desc='Robes only worn by those who are chosen by the gods. Grants the user greater protection.'),
  
  Equipment(name='Copper Armor',price=300,usage='armor',role='warrior',
            status={'DEF':3,'HP':5}, unlock =3,
            desc='Armor made from copper. Not the best metal used for armor but it does the job well enough.'),
  Equipment(name='Steel Armor',price=1000,usage='armor',role='warrior',
            status={'DEF':6,'HP':8}, unlock =7,
            desc='Armor made of steel. A standard material used for infantry to go to war.'),
  Equipment(name='Titanium Armor',price=2200,usage='armor',role='warrior',
            status={'DEF':8,'HP':10}, unlock =15,
            desc='Armor that is light, durable and strong. The best material that can be used for heavy armor.'),
  
  Equipment(name='Leather Plates',price=300,usage='armor',role='rogue',
            status={'DEF':3,'AGI':2}, unlock =3,
            desc='Cured and hardened leather that is used for armor.'),
  Equipment(name='Aluminum Plates',price=1000,usage='armor',role='rogue',
            status={'DEF':4,'AGI':3}, unlock =7,
            desc='Plates made from aluminum that is used for armor.'),
  Equipment(name='Fiber Plates',price=2200,usage='armor',role='rogue',
            status={'DEF':5,'AGI':5}, unlock =15,
            desc='Extremely light but strong plates used for light armor.'),
]

W_M1,W_M2,W_M3,W_C1,W_C2,W_C3,W_W1,W_W2,W_W3,W_R1,W_R2,W_R3 = 0,1,2,3,4,5,6,7,8,9,10,11
weapons = [
  Equipment(name='Magic Book',price=200,usage='weapon',role='mage',
            status={'ATK':2}, unlock = 3,
            desc='A beginner spell book for mages. Contains instruction for basic spells.'),
  Equipment(name='Magic Tome',price=800,usage='weapon',role='mage',
            status={'ATK':4}, unlock = 8,
            desc='A collection of adept spells for a mage. Used by skilled mages.'),
  Equipment(name='Magic Opus',price=2000,usage='weapon',role='mage',
            status={'ATK':7}, unlock = 13,
            desc='A beginner spell book for mages. Contains instruction for basic spells.'),
  
  Equipment(name='Wooden Staff',price=200,usage='weapon',role='cleric',
            status={'ATK':1}, unlock = 3,
            desc='A basic weapon only for self defense, most commonly used by clerics'),
  Equipment(name='Iron Staff',price=800,usage='weapon',role='cleric',
            status={'ATK':3, 'DEF':1}, unlock = 8,
            desc='An iron staff used by combat clerics to deal extra damage.'),
  Equipment(name='Silver Staff',price=2000,usage='weapon',role='cleric',
            status={'ATK':5, 'DEF':2}, unlock = 13,
            desc='A staff made from holy metal, silver. Is used for exorcism.'),
  
  Equipment(name='Training Sword',price=200,usage='weapon',role='warrior',
            status={'ATK':2}, unlock = 3,
            desc='A sword used by swordsmen during training. Deals sufficient damage.'),
  Equipment(name='Infantry Sword',price=800,usage='weapon',role='warrior',
            status={'ATK':5}, unlock = 8,
            desc='The type of sword used by the royal infantry when going to war.'),
  Equipment(name='Seasoned Sword',price=2000,usage='weapon',role='warrior',
            status={'ATK':9}, unlock = 13,
            desc='A sword that was crafted to strike monsters down. Made only by the best blacksmith.'),
  
  Equipment(name='Shiv',price=200,usage='weapon',role='rogue',
            status={'ATK':2}, unlock = 3,
            desc='A basic hidden dagger that is commonly used by theives.'),
  Equipment(name='Iron Dagger',price=800,usage='weapon',role='rogue',
            status={'ATK':4}, unlock = 8,
            desc='A well crafted dagger that can be used for many purposes. Long enough for utility, short enough to be hidden'),
  Equipment(name='Hidden Blade',price=2000,usage='weapon',role='rogue',
            status={'ATK':7}, unlock = 13,
            desc='A blade designed for only the best assassins out there. Well hidden under the arm of the user to strike down foes.'),
]

from objects import Consumable
C_HP_S,C_HP_M,C_HP_L,C_MP_S,C_MP_M,C_MP_L,C_ATK,C_DEF,C_AGI,C_LUK = 0,1,2,3,4,5,6,7,8,9
consumables = [
  Consumable(name='Small HP Potion',price=25,effect={'HP':10},
            desc='A small vial of potion to heal targeted ally'),
  Consumable(name='Medium HP Potion',price=75,effect={'HP':25},
            desc='A vial of potion to heal targeted ally'),
  Consumable(name='Big HP Potion',price=150,effect={'HP':50},
            desc='A small vial of potion to heal targeted ally'),
  
  Consumable(name='Small MP Potion',price=25,effect={'MP':10},
            desc='A small vial of potion to restore MP of targeted ally'),
  Consumable(name='Medium MP Potion',price=75,effect={'MP':25},
            desc='A vial of potion to restore MP of targeted ally'),
  Consumable(name='Big MP Potion',price=150,effect={'MP':50},
            desc='A small vial of potion to restore MP of targeted ally'),
  
  Consumable(name='ATK Candy',price=500,effect={'ATK':1},
            desc='A piece of candy that can add and ATK of targeted ally by 1'),
  Consumable(name='DEF Candy',price=500,effect={'DEF':1},
            desc='A piece of candy that can add and DEF of targeted ally by 1'),
  Consumable(name='AGI Candy',price=500,effect={'AGI':1},
            desc='A piece of candy that can add and AGI of targeted ally by 1'),
  Consumable(name='LUK Candy',price=500,effect={'LUK':1},
            desc='A piece of candy that can add and LUK of targeted ally by 1'),
]

monsterParty = [
  {'Imp':1},{'Imp':2},{'Imp':3},
  {'Imp':1,'Rat':2},

  {'Zombie':1},{'Zombie':2},{'Zombie':3},

  {'Rat':2},{'Rat':3},

  {'Warlock':1},{'Warlock':1,'Imp':2},{'Warlock':1,'Zombie':2},{'Warlock':1,'Zombie':1},{'Warlock':1,'Skeleton':1},

  {'Serpent':1},{'Serpent':2},

  {'Skeleton':1},{'Skeleton':2},{'Skeleton':3},
  {'Skeleton':1, 'Zombie':2},
  {'Skeleton':2, 'Zombie':1},

  {'Ghost':1},{'Ghost':2},{'Ghost':3},
]

M_IMP, M_ZOMBIE, M_WARLOCK, M_SKELETON, M_SERPENT, M_GHOST, M_RAT = 0,1,2,3,4,5,6
monsters = [
  {'name':'Imp','skills':[SKILL_FIREBALL],
  'status':{'HP':10,'MP':6,'ATK':3,'DEF':1,'AGI':3,'LUK':2},
  'leveling':{'div':3,'status':{'HP':1,'MP':1,'ATK':2,'DEF':0,'AGI':2,'LUK':2}},
  'image':'(◣‿◢)ψ'},

  {'name':'Zombie','skills':[SKILL_WARCRY],
  'status':{'HP':10,'MP':0,'ATK':2,'DEF':0,'AGI':1,'LUK':0},
  'leveling':{'div':2,'status':{'HP':1,'MP':1,'ATK':2,'DEF':1,'AGI':2,'LUK':1}},
  'image':'~(。□°)~'},

  {'name':'Warlock','skills':[SKILL_FIREBALL,SKILL_POISON,SKILL_HEAL],
  'status':{'HP':8,'MP':10,'ATK':4,'DEF':0,'AGI':1,'LUK':1},
  'leveling':{'div':2,'status':{'HP':2,'MP':2,'ATK':2,'DEF':1,'AGI':1,'LUK':1}},
  'image':'(◣__◢)⊃━ﾟ.*･｡ﾟ'},
  
  {'name':'Skeleton','skills':[SKILL_WARCRY],
  'status':{'HP':10,'MP':6,'ATK':4,'DEF':2,'AGI':0,'LUK':0},
  'leveling':{'div':3,'status':{'HP':2,'MP':1,'ATK':1,'DEF':2,'AGI':1,'LUK':1}},
  'image':'┌(۞ 皿 ۞)┐'},
  
  {'name':'Serpent','skills':[SKILL_POISON],
  'status':{'HP':7,'MP':10,'ATK':3,'DEF':0,'AGI':2,'LUK':3},
  'leveling':{'div':2,'status':{'HP':1,'MP':1,'ATK':1,'DEF':0,'AGI':2,'LUK':2}},
  'image':'<XXXXXXXXX:>~'},
  
  {'name':'Ghost','skills':[],
  'status':{'HP':6,'MP':0,'ATK':2,'DEF':0,'AGI':4,'LUK':5},
  'leveling':{'div':3,'status':{'HP':1,'MP':1,'ATK':2,'DEF':0,'AGI':2,'LUK':1}},
  'image':'<  ⊃╥﹏╥)⊃'},
  
  {'name':'Rat','skills':[SKILL_POISON],
  'status':{'HP':5,'MP':0,'ATK':2,'DEF':0,'AGI':3,'LUK':2},
  'leveling':{'div':3,'status':{'HP':1,'MP':1,'ATK':1,'DEF':0,'AGI':2,'LUK':2}},
  'image':'ᘛ⁐̤ᕐᐷ'},
  
  # 'name':{'skills':[],
  # 'status':{'HP':0,'MP':0,'ATK':0,'DEF':0,'AGI':0,'LUK':0},
  # 'leveling':{'div':3,'status':{'HP':1,'MP':1,'ATK':1,'DEF':1,'AGI':1,'LUK':1}},
  # 'image':''},
]
class Area:
  def __init__(self,name,toClear,clearReward,monsters,levelRange,dropItems,expDPE,goldDPE,MDB,MPDB,IDB,ARTDB,ARMDB,WDB,CDB):
    # print("=========================================================")
    self.name = name
    self.toClear = toClear
    self.clearReward = clearReward
    self.monsters = []
    monsterNames = []
    for m in monsters:
      self.monsters.append(MDB[m])
      monsterNames.append(MDB[m]['name'])
    self.monsterParties = []
    for mn in monsterNames:
      for m in MPDB:
        # print(str(self.monsterParties)+","+str(m.keys())+","+mn)
        if(mn in m.keys() and m not in self.monsterParties):
          self.monsterParties.append(m)
    self.levelRange = levelRange
    # drop items categ = I,ART,ARM,W,C
    # items = [index,chance]
    for items in dropItems['I']:
      self.dropItems.append([IDB[items[0]],items[1]])
    for items in dropItems['ART']:
      self.dropItems.append([ARTDB[items[0]],items[1]])
    for items in dropItems['ARM']:
      self.dropItems.append([ARMDB[items[0]],items[1]])
    for items in dropItems['W']:
      self.dropItems.append([WDB[items[0]],items[1]])
    for items in dropItems['C']:
      self.dropItems.append([CDB[items[0]],items[1]])
    for i in self.dropItems:
      self.totalRate += i[1]
    self.totalRate += 20 # there's a good chance you won't get anything either, hehe 
    self.expDPE = expDPE
    self.goldDPE = goldDPE
  name = ''
  progress = 0
  toClear = 30
  isCleared = False
  clearReward = []
  
  monsters = []
  monsterParties = []
  levelRange = []
  dropItems = []
  totalRate = 0
  # DPE = drop per enemy (range)
  expDPE = []
  goldDPE = []
  
A_0,A_1,A_2,A_3,A_4,A_5 = 0,1,2,3,4,5
areas = [
  Area(name="Begining's Plains",toClear=20,
      clearReward={
        'gold':800,
        'exp':120,
      },
      monsters=[M_SERPENT,M_RAT,M_IMP],
      dropItems={
        'I':[[I_SR,9],[I_SA,7],[I_GR,2]],
        'ART':[[ART_MP1,2],[ART_DEF1,2]],
        'ARM':[[ARM_C1,1],[ARM_W1,1]],
        'W':[[W_M1,1],[W_W1,1]],
        'C':[[C_MP_S,10],[C_HP_S,10],[C_DEF,3],[C_AGI,3]]
      },
      expDPE=[2,5],goldDPE=[3,12],levelRange=[1,8],
      MDB=monsters,MPDB=monsterParty,IDB=items,ARTDB=artifact,ARMDB=armors,WDB=weapons,CDB=consumables
      ),
  Area(name="Zombified Village",toClear=30,
      clearReward={
        'gold':1500,
        'exp':200,
      },
      monsters=[M_WARLOCK,M_ZOMBIE,M_SKELETON],
      dropItems={
        'I':[[I_SR,10],[I_SA,9],[I_GR,6],[I_GA,5]],
        'ART':[[ART_HP1,2],[ART_LUK1,2]],
        'ARM':[[ARM_M1,1],[ARM_R1,1]],
        'W':[[W_C1,1],[W_R1,1]],
        'C':[[C_MP_S,10],[C_HP_S,10],[C_ATK,3],[C_LUK,3]]
      },
      expDPE=[4,9],goldDPE=[7,16],levelRange=[6,15],
      MDB=monsters,MPDB=monsterParty,IDB=items,ARTDB=artifact,ARMDB=armors,WDB=weapons,CDB=consumables
      ),
  Area(name="Rotting Forest",toClear=40,
      clearReward={
        'gold':2300,
        'exp':340,
      },
      monsters=[M_GHOST,M_RAT,M_IMP],
      dropItems={
        'I':[[I_SR,3],[I_SA,2],[I_GR,10],[I_GA,8],[I_JR,2]],
        'ART':[[ART_AGI1,2],[ART_ATK1,2]],
        'ARM':[[ARM_C2,1],[ARM_W2,1]],
        'W':[[W_M2,1],[W_R2,1]],
        'C':[[C_MP_S,11],[C_HP_S,11],[C_AGI,3],[C_DEF,3],[C_MP_M,5],[C_HP_M,5]]
      },
      expDPE=[5,14],goldDPE=[12,24],levelRange=[14,21],
      MDB=monsters,MPDB=monsterParty,IDB=items,ARTDB=artifact,ARMDB=armors,WDB=weapons,CDB=consumables
      ),
  Area(name="Dusted Caverns",toClear=30,
      clearReward={
        'gold':3200,
        'exp':520,
      },
      monsters=[M_ZOMBIE,M_SKELETON,M_RAT],
      dropItems={
        'I':[[I_GR,8],[I_GA,11],[I_JR,4],[I_JA,4]],
        'ART':[[ART_HP2,2],[ART_DEF2,2]],
        'ARM':[[ARM_R2,1],[ARM_M2,1]],
        'W':[[W_C2,1],[W_W2,1]],
        'C':[[C_MP_S,5],[C_HP_S,5],[C_ATK,3],[C_LUK,3],[C_MP_M,9],[C_HP_M,9]]
      },
      expDPE=[7,19],goldDPE=[17,30],levelRange=[19,26],
      MDB=monsters,MPDB=monsterParty,IDB=items,ARTDB=artifact,ARMDB=armors,WDB=weapons,CDB=consumables
      ),
  Area(name="Warlock's Bog",toClear=30,
      clearReward={
        'gold':4500,
        'exp':700,
      },
      monsters=[M_WARLOCK,M_GHOST,M_SERPENT],
      dropItems={
        'I':[[I_GR,7],[I_GA,9],[I_JR,8],[I_JA,7]],
        'ART':[[ART_AGI2,2],[ART_MP2,2]],
        'ARM':[[ARM_R3,1],[ARM_W3,1]],
        'W':[[W_C3,1],[W_M3,1]],
        'C':[[C_MP_L,5],[C_HP_L,5],[C_DEF,3],[C_LUK,3],[C_MP_M,6],[C_HP_M,6]]
      },
      expDPE=[14,30],goldDPE=[24,41],levelRange=[25,33],
      MDB=monsters,MPDB=monsterParty,IDB=items,ARTDB=artifact,ARMDB=armors,WDB=weapons,CDB=consumables
      ),
  Area(name="Mount Grimfate",toClear=25,
      clearReward={
        'gold':6600,
        'exp':900,
      },
      monsters=[M_IMP,M_WARLOCK,M_SKELETON],
      dropItems={
        'I':[[I_GR,3],[I_GA,4],[I_JR,9],[I_JA,8]],
        'ART':[[ART_LUK2,2],[ART_ATK2,2]],
        'ARM':[[ARM_C3,1],[ARM_M3,1]],
        'W':[[W_R3,1],[W_W3,1]],
        'C':[[C_MP_L,3],[C_HP_L,3],[C_DEF,3],[C_LUK,3],[C_MP_M,7],[C_HP_M,7]]
      },
      expDPE=[21,37],goldDPE=[33,55],levelRange=[31,40],
      MDB=monsters,MPDB=monsterParty,IDB=items,ARTDB=artifact,ARMDB=armors,WDB=weapons,CDB=consumables
      ),
]


from system import Trader

T_1,T_2,T_3 = 0,1,2
traders = [
  Trader('Dawn County',{
    'C':[C_HP_S,C_HP_M,C_MP_S,C_MP_M],
    'W':[W_C1,W_M1,W_R1,W_W1],
    'ARM':[ARM_C1,ARM_M1,ARM_W1,ARM_R1]
  }),
  Trader('Promise Township',{
    'C':[C_HP_S,C_HP_M,C_MP_S,C_MP_M,C_HP_L,C_MP_L],
    'W':[W_C2,W_M2,W_R2,W_W2],
    'ARM':[ARM_C2,ARM_M2,ARM_W2,ARM_R2]
  }),
  Trader('Hope Fortress',{
    'C':[C_HP_S,C_HP_M,C_MP_S,C_MP_M,C_HP_L,C_MP_L],
    'W':[W_C3,W_M3,W_R3,W_W3],
    'ARM':[ARM_C3,ARM_M3,ARM_W3,ARM_R3]
  }),
]