from Bullet import Bullet
from Unit import Unit

class Shooter(Unit):
    def __init__(self, x, y):
        super(Shooter, self).__init__(x,y)
        self.target = None

    def update(self):
        super().update()

    def shoot(self, bullets):
        if self.target is not None:
            bullets.append(Bullet(self.centerX, self.centerY, self.target, self.attackPower))
            print(str(self.attackPower))