from Auto import Auto
from Shooter import Shooter

class AutoShooter(Shooter,Auto):

    def __init__(self, x, y):
        super(AutoShooter, self).__init__(x,y)

    def update(self, bullets):
        super().update()
        super().updateTimer()
        if self.passedInterval:
            self.shoot(bullets)
            self.passedInterval = False
