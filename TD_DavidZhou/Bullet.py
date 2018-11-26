import math

import pygame



from Mover import Mover



class Bullet(Mover):
    def __init__(self, x, y, target, attackPower):
        super(Bullet, self).__init__(x,y)
        self.collider.radius = 5
        self.face(target.centerX, target.centerY)
        self.velocityX = int(math.cos(self.angle) * 20)
        self.velocityY = -int(math.sin(self.angle) * 20)
        self.life = 200
        self.attackPower = attackPower

    def draw(self, screen, camera):
        pygame.draw.circle(screen,(50,50,50), (self.centerX - camera.offsetX, self.centerY - camera.offsetY), self.collider.radius, 0)
        super().draw(screen)

    def update(self):
        super().update()
        self.life -= 1
