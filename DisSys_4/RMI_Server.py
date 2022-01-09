import Pyro4
from math import log,sin,cos,sqrt

@Pyro4.expose
class SciCalculator:
  def add(self,arr):
    return arr[0]+arr[1]
  def sub(self,arr):
    return arr[0]-arr[1]
  def mul(self,arr):
    return arr[0]*arr[1]
  def div(self,arr):
    return arr[0]/arr[1]
  def pow(self,arr):
    return arr[0]**arr[1]
  def sqr(self,a):
    return sqrt(a)
  def log(self,a):
    return log(a)
  def sin(self,a):
    return sin(a)
  def cos(self,a):
    return cos(a)

daemon = Pyro4.Daemon()

uri = daemon.register(SciCalculator)
ns = Pyro4.locateNS()
ns.register('obj', uri)


daemon.requestLoop()
print('Server ready!!')