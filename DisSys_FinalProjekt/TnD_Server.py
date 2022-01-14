import rpyc
from math import log,sin,cos,sqrt

class MyService(rpyc.Service):
    def on_connect(self, conn):
    # code that runs when a connection is created
    # (to init the service, if needed)
        pass

    def on_disconnect(self, conn):
        # code that runs after the connection has already closed
        # (to finalize the service, if needed)
        pass

    def exposed_add(self,arr):
        return arr[0]+arr[1]
    def exposed_sub(self,arr):
        return arr[0]-arr[1]
    def exposed_mul(self,arr):
        return arr[0]*arr[1]
    def exposed_div(self,arr):
        return arr[0]/arr[1]
    def exposed_pow(self,arr):
        return arr[0]**arr[1]
    def exposed_sqr(self,a):
        return sqrt(a)
    def exposed_log(self,a):
        return log(a)
    def exposed_sin(self,a):
        return sin(a)
    def exposed_cos(self,a):
        return cos(a)

if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    t = ThreadedServer(MyService, port=18861)
    t.start()
