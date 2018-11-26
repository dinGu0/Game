import pygame

class Circle:
    def __init__(self, x, y, r):
        self.centerX = x
        self.centerY = y
        self.radius = r

    def draw(self, screen):
         pygame.draw.circle(screen, (255, 0, 0), (self.centerX - camera.offsetX, self.centerY - camera.offsetY), self.radius, 1)



    def collideWithCircle(self, other):
        return ((self.centerX - other.centerX)**2 + (self.centerY - other.centerY)**2)**0.5 <= self.radius + other.radius