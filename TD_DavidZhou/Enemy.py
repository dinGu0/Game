import math
import random

import pygame

from AutoMover import AutoMover



enemyStandImage = pygame.image.load("images/units/EnemyStand.png")
enemyMove1Image = pygame.image.load("images/units/EnemyMove1.png")
enemyMove2Image = pygame.image.load("images/units/EnemyMove2.png")

class Enemy(AutoMover):

    def __init__(self, x, y, score):
        self.image = enemyMove1Image
        super(Enemy, self).__init__(x,y)
        self.angle = 0
        self.health = 10 + (score/2)
        self.timerMax = int(4)
        self.attackPower = 10

    def draw(self, screen, turrets, player, camera):
        super().draw(screen)
        if turrets.__len__() > 0:
            self.getNearestTarget(turrets, player)
        else:
            self.target = player
        if self.target is not None:
            self.pointAtPlayer(screen, camera)
        else:
            rotimage = pygame.transform.rotate(self.image, math.degrees(self.angle))
            rect = rotimage.get_rect(center=(self.centerX - camera.offsetX, self.centerY - camera.offsetY))
            screen.blit(rotimage, rect)

    def getNearestTarget(self, turrets, player):
        ni = 0
        if turrets.__len__() == 0:
            self.target = player
            return
        for i in range(turrets.__len__()):
            if ni != i:
                if abs(self.centerX - turrets[i].centerX) < abs(self.centerX - turrets[ni].centerX) and abs(self.centerY - turrets[i].centerY) < abs(self.centerY - turrets[ni].centerY):
                    ni = i
        self.target = turrets[ni]
        if abs(self.centerX - player.centerX) < abs(self.centerX - turrets[ni].centerX) + 100 and abs(self.centerY - player.centerY) < abs(self.centerY - turrets[ni].centerY) + 100:
            self.target = player


    def pointAtPlayer(self, screen, camera):
        self.face(self.target.centerX, self.target.centerY)
        rotimage = pygame.transform.rotate(self.image, math.degrees(self.angle))
        rect = rotimage.get_rect(center=(self.centerX - camera.offsetX, self.centerY - camera.offsetY))
        screen.blit(rotimage,rect)

    def update(self, walls, turrets, player):
        px = self.collider.centerX
        py = self.collider.centerY
        self.collider.centerX += self.velocityX
        self.collider.centerY += self.velocityY
        hitWall = False
        for i in range(walls.__len__()):
            if walls[i].collider.collideWithCircle(self.collider):
                walls[i].health -= self.attackPower
                self.stopHorizontal()
                self.stopVertical()
                if self.collider.centerX > walls[i].collider.centerX:
                    self.collider.centerX = px + self.moveSpeed
                if self.collider.centerX < walls[i].collider.centerX:
                    self.collider.centerX = px - self.moveSpeed
                if self.collider.centerY > walls[i].collider.centerY:
                    self.collider.centerY = py + self.moveSpeed
                if self.collider.centerY < walls[i].collider.centerY:
                    self.collider.centerY = py - self.moveSpeed
                self.centerX = self.collider.centerX
                self.centerY = self.collider.centerY
                hitWall = True
                break
        if not hitWall:
            if self.velocityX is not 0 or self.velocityY is not 0:
                if self.timer % 5 == 0:
                    if self.image == enemyMove1Image:
                        self.image = enemyMove2Image
                    else:
                        self.image = enemyMove1Image
            self.velocityX = int(math.cos(self.angle) * random.randrange(10,20))
            self.velocityY = -int(math.sin(self.angle) * random.randrange(10,20))
        else:
            self.getNearestTarget(turrets, player)
        super().update()

