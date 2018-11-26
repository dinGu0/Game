import pygame


from Rectangle import Rectangle
from Unit import Unit


class Wall(Unit):
    def __init__(self, x, y, w, h):
        super().__init__(x, y)
        self.width = w
        self.height = h
        self.health = 3000
        self.collider = Rectangle(self.centerX, self.centerY, self.width, self.height)

    def draw(self, screen, camera):
        pygame.draw.rect(screen, (200, 150, 100), [self.centerX - self.width / 2 - camera.offsetX, self.centerY - self.height / 2 - camera.offsetY, self.width, self.height], 0)
        super().draw(screen)

    def update(self):
        super().update()
def createWalls():
    walls = []
# outer walls
    walls.append(Wall(0, -725, 1900, 50))
    walls.append(Wall(0, 725, 1900, 50))
    walls.append(Wall(-975, 0, 50, 1400))
    walls.append(Wall(975, 0, 50, 1400))

    # starting box
    walls.append(Wall(100, 300, 50, 600))
    walls.append(Wall(700, 300, 50, 600))
    walls.append(Wall(400, 25, 650, 50))
    walls.append(Wall(500, 575, 450, 50))

    # randoms
    walls.append(Wall(-500, 200, 200, 50))
    walls.append(Wall(-500, 400, 200, 50))
    walls.append(Wall(-500, 600, 200, 50))

    walls.append(Wall(-625, 200, 50, 200))
    walls.append(Wall(-625, 400, 50, 200))
    walls.append(Wall(-625, 600, 50, 200))

    walls.append(Wall(-500, -200, 200, 50))
    walls.append(Wall(-500, -400, 200, 50))
    walls.append(Wall(-500, -600, 200, 50))

    walls.append(Wall(-625, -200, 50, 200))
    walls.append(Wall(-625, -400, 50, 200))
    walls.append(Wall(-625, -600, 50, 200))
    return walls




