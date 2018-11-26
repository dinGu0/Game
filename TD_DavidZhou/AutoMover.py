from Auto import Auto
from Mover import Mover

class AutoMover(Mover, Auto):

    def __init__(self, x, y):
        super(AutoMover, self).__init__(x, y)

    def update(self):
        super().updateTimer()
        if self.passedInterval:
            self.move()
            self.passedInterval = False

    def move(self):
        super().update()
        self.velocityX = 0
        self.velocityY = 0