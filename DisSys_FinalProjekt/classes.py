'''
role = knight, mage, cleric, rouge

dbTODO = make 4 skills for each

'''
#=================================================================================

class Player:
  def __init__(self, in_name, in_role, in_status):
    self.name = in_name
    self.role = in_role
    self.status = in_status
  name = 'pleki'
  # VARIABLES
  isAlive = True
  status = {
    # ====================== basic statuses ========================
    'HP':15,
    'MP':15,
    'ATK':1, # base attack
    'DEF':1, # block
    'AGI':1, # evasion
    'LUK':1, # crit
    'INT':1, # magic damage
    # ====================== level statuses ========================
    'LVL':1,
    'EXP':0,
    'EXP_CAP':20,
  }
  role = ''
  skills = {}
  gold = 0
  items = {}
  effects = []

  # FUNCTIONS
  def action(com):
    com = com.split(' ')
    if com[0] == 'story':
      # story 'we goto the woods and blablabla'
      pass
    elif com[0] == 'attack':
      # attack target_enemy
      pass
    elif com[0] == 'skill':
      # skill skillname target
      pass
    elif com[0] == 'item':
      # item itemname target
      pass
    elif com[0] == 'defend':
      # defend
      pass
    else:
      print('bad command!! try again!!')
    
  def story(act):
    pass
  def skill(act):
    pass
  def attack(act):
    pass
  def defend(act):
    pass
  def item(act):
    pass
  '''
  doAction : story, defend, skill, attack, item, flee
  doSkill
  useItem
  '''
#=================================================================================
S_TARGET_SELF, S_TARGET_ENEMY, S_TARGET_ALL_ENEMIES, S_TARGET_ALLY, S_TARGET_ALL_ALLIES = 'self', '1enemy', 'allEnemy', '1ally', 'allAlly'
S_STATS_HP, S_STATS_ATK = 'HP', 'ATK'
class Skill:
  def __init__(self, name, effect, target, tagert_stats, turn, desc, level, active):
    self.name = name
    self.effect = effect
    self.target = target
    self.target_stats = tagert_stats
    self.turn = turn
    self.desc = desc
    self.level = level
    self.active = active
  name = ''
  effect = 0        # negative is damage, positive is healing, 0 is smth else
  target_stats = 'HP'
  target = 'self'   # self or enemy or fren
  active = 'active' # active or passive
  turn = 0
  desc = ''
  level = 1
#=================================================================================

class Monster:
  def __init__(self, name, level, exp_drop, gold_drop, skills):
    self.name = name
    self.level = level
    self.exp_drop = exp_drop
    self.gold_drop = gold_drop
    self.skills = skills

  name = ''
  level = 0
  exp_drop = [5,10]
  gold_drop = [0,10]
  skills = []
  effects = []
#=================================================================================

class DungeonMaster:
  pass
#=================================================================================

class Item:
  pass

