from types import SimpleNamespace

import pygame
import math

from Mover import Mover
from Shooter import Shooter
from Turret import Turret

playerStandImage = pygame.image.load("images/units/PlayerStand.png")
playerMoveImage1 = pygame.image.load("images/units/PlayerMove1.png")
playerMoveImage2 = pygame.image.load("images/units/PlayerMove2.png")


class Player(Mover, Shooter):
    def __init__(self, x, y):
        self.image = playerStandImage
        super(Player, self).__init__(x, y)
        self.shootDelayMax = 5
        self.shootDelay = self.shootDelayMax
        self.turretDelayMax = 3
        self.turretDelay = self.turretDelayMax
        self.attackPower = 25
        self.runSpeed = 8
        self.walkSpeed = 4
        self.numTurrets = 2

    def draw(self, screen, camera):
        super().draw(screen)
        self.pointAtMouse(screen, camera)



    def update(self, walls, camera):
        self.shootDelay -= 1
        self.turretDelay -= 1
        px = self.collider.centerX
        py = self.collider.centerY
        self.collider.centerX += self.velocityX
        self.collider.centerY += self.velocityY
        hitWall = False
        for i in range(walls.__len__()):
            if walls[i].collider.collideWithCircle(self.collider):
                print("hit wall")
                self.stopHorizontal()
                self.stopVertical()
                if self.collider.centerX > walls[i].collider.centerX:
                    self.collider.centerX = px + self.moveSpeed
                    camera.offsetX += self.moveSpeed
                if self.collider.centerX < walls[i].collider.centerX:
                    self.collider.centerX = px - self.moveSpeed
                    camera.offsetX -= self.moveSpeed
                if self.collider.centerY > walls[i].collider.centerY:
                    self.collider.centerY = py + self.moveSpeed
                    camera.offsetY += self.moveSpeed
                if self.collider.centerY < walls[i].collider.centerY:
                    self.collider.centerY = py - self.moveSpeed
                    camera.offsetY -= self.moveSpeed
                self.centerX = self.collider.centerX
                self.centerY = self.collider.centerY
                hitWall = True
                break
        if not hitWall:
            box = 400
            boy = 300
            bgw = 1900
            bgh = 1400
            if self.velocityX < 0:
                if camera.offsetX > int(-bgw/2 - box):
                    camera.offsetX += self.velocityX
                else:
                    camera.offsetX = int(-bgw/2 - box)
                    self.stopHorizontal()
            else:
                if camera.offsetX < int(bgw/2-800 + box):
                    camera.offsetX += self.velocityX
                else:
                    camera.offsetX = int(bgw/2-800 + box)
                    self.stopHorizontal()
            if self.velocityY < 0:
                if camera.offsetY > int(-bgh/2 - boy):
                    camera.offsetY += self.velocityY
                else:
                    camera.offsetY = int(-bgh/2 - boy)
                    self.stopVertical()
            else:
                if camera.offsetY < int(bgh/2-600 + boy):
                    camera.offsetY += self.velocityY
                else:
                    camera.offsetY = int(bgh/2-600 + boy)
                    self.stopVertical()
            super().update()
        if self.velocityX != 0 or self.velocityY != 0:
            if self.shootDelay % 5 == 0:
                if self.image == playerMoveImage1:
                    self.image = playerMoveImage2
                else:
                    self.image = playerMoveImage1
        else:
            self.image = playerStandImage
    def pointAtMouse(self, screen, camera):
        mouse = pygame.mouse.get_pos()
        self.target = SimpleNamespace(centerX=mouse[0] + camera.offsetX, centerY=mouse[1] + camera.offsetY)
        self.face(self.target.centerX, self.target.centerY)
        rotimage = pygame.transform.rotate(self.image, math.degrees(self.angle))
        rect = rotimage.get_rect(center=(self.centerX - camera.offsetX, self.centerY - camera.offsetY))
        screen.blit(rotimage, rect)
    def shoot(self, bullets):
        if self.shootDelay <= 0:
            super().shoot(bullets)
            self.shootDelay = self.shootDelayMax\

    def moveLeft(self):
        self.velocityX = -self.moveSpeed

    def moveRight(self):
        self.velocityX = self.moveSpeed

    def moveUp(self):
        self.velocityY = -self.moveSpeed

    def moveDown(self):
        self.velocityY = self.moveSpeed

    def placeTurret(self, turrets):
        if self.numTurrets > 0:
            if self.turretDelay <= 0:
                turrets.append(Turret(self.centerX, self.centerY))
                self.turretDelay = self.turretDelayMax
                self.numTurrets -= 1