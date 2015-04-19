import _thread as thread
import threading
import queue
import time
# constant
Time = 0.1
M = 2
P = 2
N = 6
Q = (N // P)
########################

dataQueue = queue.Queue()

now_eats = None


def Grandmother(period):
    while True:
        time.sleep(period * (Time))
        for i in range(N):
            dataQueue.put('breadcrumb')


class Sparrow(threading.Thread):

    def __init__(self, P, mutex, Id):
        threading.Thread.__init__(self)
        self.number_of_breadcrumbs = 0
        self.P = P
        self.status = 0  
        self.status = 1
        self.Id = Id
        self.mutex = mutex

    def __str__(self):
        status = [
            'arrived',
            'waiting for distribution',
            'fighting for breadcrumb',
            'flew off to the side and eat',
            'fly away']
        return 'Sparrow Id: [%s] number of breadcrumbs [%s] sparrow status [%s]' % (
            self.Id, self.number_of_breadcrumbs, status[self.status])

    def run(self):
        global now_eats
        while True:
            # time.sleep(Time)
            try:
                data = dataQueue.get(block=False)
                if now_eats != self.Id:
                    with mutex:
                        self.number_of_breadcrumbs += 1
                        self.status = 3
                        now_eats = self.Id
                        print(
                            'Sparrow Id: [%s] number of breadcrumbs [%s]' %
                            (self.Id, self.number_of_breadcrumbs))
                if self.number_of_breadcrumbs == self.P:
                    self.flew_away()
                    break
            except queue.Empty:
                pass

    def flew_away(self):
        self.status = 4

    def is_back(self):
        self.status = 1

    def status(self):
        return self.status

    def fight(self):
        self.status = 2

thread.start_new_thread(Grandmother, (Q,))
mutex = threading.Lock()
sparrows = set()
slep = None
for i in range(M):
    thread = Sparrow(P, mutex, i)
    thread.start()


while True:
    time.sleep(Time)
    thread = Sparrow(P, mutex, M)
    thread.start()
    M += 1
    rez = 0
    # print(dataQueue.qsize())