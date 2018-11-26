import math
import random

import pygame

from AutoShooter import AutoShooter



class Turret(AutoShooter):
    def __init__(self, x,y):
        self.image = pygame.image.load("images/units/turret.png")
        super(Turret,self).__init__(x,y)
        self.target = None
        self.angle = 0
        self.attackPower = 100
        self.timerMax = 10
        self.health = 10000



    def draw(self, screen, enemies, camera):
        super().draw(screen)
        self.getNearestTarget(enemies)
        if self.target is not None:
                self.pointAtEnemy(screen, camera)
        else:
            rotimage = pygame.transform.rotate(self.image, math.degrees(self.angle))
            rect = rotimage.get_rect(center=(self.centerX - camera.offsetX, self.centerY - camera.offsetY))
            screen.blit(rotimage, rect)

    def getNearestTarget(self, enemies):
        if enemies.__len__() > 0:
            ni = 0
            for i in range(enemies.__len__()):
                if ni != i:
                    if abs(self.centerX - enemies[i].centerX) < abs(self.centerX - enemies[ni].centerX) and abs(self.centerY - enemies[i].centerY) < abs(self.centerY - enemies[ni].centerY):
                        ni = i
            self.target = enemies[ni]

    def pointAtEnemy(self, screen, camera):
        self.face(self.target.centerX, self.target.centerY)
        rotimage = pygame.transform.rotate(self.image, math.degrees(self.angle))
        rect = rotimage.get_rect(center = (self.centerX - camera.offsetX, self.centerY - camera.offsetY))
        screen.blit(rotimage, rect)

    def update(self, bullets):
        super().update(bullets)