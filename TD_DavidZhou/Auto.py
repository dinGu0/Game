import random

from Unit import Unit

class Auto(Unit):

    def __init__(self, x, y):
        super(Auto, self).__init__(x,y)
        self.timerMax = random.randrange(20,50)
        self.timer = self.timerMax
        self.passedInterval = False

    def updateTimer(self):
        if not self.passedInterval:
            self.timer -= 1
            if self.timer <= 0:
                self.timer = self. timerMax
                self.passedInterval = True