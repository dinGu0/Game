import math

from Circle import Circle

class Unit:
    def __init__(self, x, y):
        self.centerX = x
        self.centerY = y
        self.angle = 0
        self.active = True
        self.health = 100
        self.attackPower = 1
        self.collider = Circle(self.centerX, self.centerY, 25)

    def draw(self, screen):
        self.centerX = int(self.centerX)
        self.centerY = int(self.centerY)
        self.collider.centerX = self.centerX
        self.collider.centerY = self.centerY
        # self.collider.draw(screen)

    def face(self, x, y):
        dx = x - self.centerX
        dy = y - self.centerY
        self.angle = math.atan2(-dy, dx)
        self.angle %= 2 * math.pi

    def update(self):
        if self.health <= 0:
            self.active = False
    def attack(self, unit):
        unit.health -= self.attackPower
