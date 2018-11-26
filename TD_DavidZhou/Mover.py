from Unit import Unit

class Mover(Unit):


    def __init__(self, x, y):
        super(Mover, self).__init__(x, y)
        self.velocityX = 0
        self.velocityY = 0
        self.moveSpeed = 5

    # def draw(self, screen):
    #     super().draw(screen)

    def update(self):
        super().update()
        self.centerX += self.velocityX
        self.centerY += self.velocityY

    def stopHorizontal(self):
        self.velocityX = 0

    def stopVertical(self):
        self.velocityY = 0
