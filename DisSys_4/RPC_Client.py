import rpyc
import random

calc = rpyc.connect("localhost", 18861)

functs = [ 'add', 'sub', 'mul', 'div', 'pow', 'sqr', 'log', 'sin', 'cos']

print('client making random request!')

for i in range(20):
  funct = random.choice(functs)
  a = random.randint(1,1000)
  b = random.randint(1,10)

  if(funct == 'add'):
    print(f'{a} + {b} = {calc.root.add([a,b])}')
  elif(funct == 'sub'):
    print(f'{a} - {b} = {calc.root.sub([a,b])}')
  elif(funct == 'mul'):
    print(f'{a} * {b} = {calc.root.mul([a,b])}')
  elif(funct == 'div'):
    print(f'{a} / {b} = {calc.root.div([a,b])}')
  elif(funct == 'pow'):
    print(f'{a} ^ {b} = {calc.root.pow([a,b])}')
  elif(funct == 'sqr'):
    print(f'sqr({a}) = {calc.root.sqr(a)}')
  elif(funct == 'log'):
    print(f'log({a}) = {calc.root.log(a)}')
  elif(funct == 'sin'):
    print(f'sin({a}) = {calc.root.sin(a)}')
  elif(funct == 'cos'):
    print(f'cos({a}) = {calc.root.cos(a)}')

print('client done making random requests!')