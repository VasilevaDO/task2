# constant
M = 30
P = 2
N = 6
Q = N // P


class Sparrow:

    def __init__(self, P):
        self.number_of_breadcrumbs = 0
        self.P = P
        self.status = 0  # 0 -прилетел, 1 - ждет, 2 -дерется, 3 - ест, 4 улетел
        self.status = 1

    def __str__(self):
        status = [
            'Прилетел',
            'Ждет раздачи',
            'Дерется за крошку',
            'Отлетел в сторону и ест',
            'Улетел']
        return status[self.status] + ' ' + str(self.number_of_breadcrumbs)

    def eat(self):
        if self.status == 3:
            print('уже ест')
        else:

            self.number_of_breadcrumbs += 1
            self.status = 3
        if self.number_of_breadcrumbs == self.P:
            self.flew_away()

    def flew_away(self):
        self.status = 4

    def is_back(self):
        self.status = 1

    def status(self):
        return self.status

    def fight(self):
        self.status = 2

sparrows = set()
slep = None
for i in range(M):
    sparrows.add(Sparrow(P))

for i in range(2000):
    sparrows.add(Sparrow(P))
    if i % Q == 0:
        for Y in range(N):
            try:
                #print(i,Y, len(sparrows))
                x = sparrows.pop()
                # print(x)
                if slep is not None:
                    slep.is_back()
                    sparrows.add(slep)

                x.fight()
                x.eat()
                if x.status == 3:
                    slep = x
                else:
                    slep = None
            except KeyError:
                print('все улетели (((')
        if slep is not None:
            sparrows.add(slep)

# print(sparrows.pop())