
# Parametrs
Time = 0.1  # in seconds
M = 8
P = 4
N = 8
Q = (N // P)
########################################################################

import threading
import queue
import time



class Bench(threading.Thread):

    def __init__(self, M, P, N, Q=(N // P), Time=60):
        threading.Thread.__init__(self)
        self.Time = Time
        self.M = M
        self.P = P
        self.N = N
        self.Q = Q
        self.dataQueue = queue.Queue()
        self.now_eats = [None]
        self.mutex = threading.Lock()
        self.sparrows = []

    def run(self):
        now_eats = None
        thread = Grandmother(self.Q, self.dataQueue, self.N, self.Time)
        thread.start()
        
        lol = threading.active_count()
        for i in range(self.M):
            thread = Sparrow(
                self.P,
                self.mutex,
                i,
                self.dataQueue,
                self.now_eats)
            thread.start()

        while True:
            time.sleep(self.Time)
            #print('@@@',self.now_eats,threading.active_count()-lol)
            thread = Sparrow(
                self.P,
                self.mutex,
                self.M,
                self.dataQueue,
                self.now_eats)
            thread.start()
            self.M += 1


class Grandmother(threading.Thread):

    def __init__(self, period, dataQueue, N, Time):
        threading.Thread.__init__(self)
        self.period = period
        self.dataQueue = dataQueue
        self.Time = Time
        self.N = N

    def run(self):
        while True:
            time.sleep(self.period * (self.Time))
            for i in range(self.N):
                self.dataQueue.put('breadcrumb')


class Sparrow(threading.Thread):

    def __init__(obj, P, mutex, Id, dataQueue, now_eats):
        threading.Thread.__init__(obj)
        obj.number_of_breadcrumbs = 0
        obj.P = P
        obj.status = 0
        obj.status = 1
        obj.Id = Id
        obj.dataQueue = dataQueue
        obj.mutex = mutex
        obj.now_eats = now_eats
        obj.Status = [
            'arrived',
            'waiting for distribution',
            'fighting for breadcrumb',
            'flew off to the side and eat',
            'fly away']

    def __str__(obj):
        return 'Sparrow Id: %s. Number of breadcrumbs: %s. Sparrow status: %s' % (
            obj.Id, obj.number_of_breadcrumbs, obj.Status[obj.status])

    def run(obj):

        while True:
            try:
                data = obj.dataQueue.get(block=False)
                #print(obj.Id,'       ',data,obj.now_eats,obj.dataQueue.qsize(),obj.number_of_breadcrumbs)
                if obj.now_eats  is not obj.Id:
                    with obj.mutex:
                        obj.number_of_breadcrumbs += 1
                        obj.status = 3
                        #print(obj.Id,'       ',data,obj.now_eats,obj.dataQueue.qsize(),obj.number_of_breadcrumbs)
                        obj.now_eats[0] = obj.Id
                        # print(obj)
                if obj.number_of_breadcrumbs == obj.P:
                    obj.flew_away()
                    # print(obj)
                    break
            except queue.Empty:
                pass

    def flew_away(obj):
        obj.status = 4

    def is_back(obj):
        obj.status = 1

    def status(obj):
        return obj.status

    def fight(obj):
        obj.status = 2

thread = Bench(M, P, N, Time=Time, Q=Q)
thread.start()
