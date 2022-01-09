import Pyro4
import random

ns = Pyro4.locateNS()

uri = ns.lookup('obj')

calc = Pyro4.Proxy(uri)

print('SciCalculator is now accessible!')

functs = [ 'add', 'sub', 'mul', 'div', 'pow', 'sqr', 'log', 'sin', 'cos']

print('client making random request!')

for i in range(20):
  funct = random.choice(functs)
  a = random.randint(1,1000)
  b = random.randint(1,10)

  if(funct == 'add'):
    print(f'{a} + {b} = {calc.add([a,b])}')
  elif(funct == 'sub'):
    print(f'{a} - {b} = {calc.sub([a,b])}')
  elif(funct == 'mul'):
    print(f'{a} * {b} = {calc.mul([a,b])}')
  elif(funct == 'div'):
    print(f'{a} / {b} = {calc.div([a,b])}')
  elif(funct == 'pow'):
    print(f'{a} ^ {b} = {calc.pow([a,b])}')
  elif(funct == 'sqr'):
    print(f'sqr({a}) = {calc.sqr(a)}')
  elif(funct == 'log'):
    print(f'log({a}) = {calc.log(a)}')
  elif(funct == 'sin'):
    print(f'sin({a}) = {calc.sin(a)}')
  elif(funct == 'cos'):
    print(f'cos({a}) = {calc.cos(a)}')

print('client done making random requests!')