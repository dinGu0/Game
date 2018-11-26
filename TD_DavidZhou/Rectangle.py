import pygame
import math



class Rectangle:
    def __init__(self, x, y, w, h):
        self.centerX = x
        self.centerY = y
        self.width = w
        self.height = h

    def draw(self, screen, camera):
        pygame.draw.rect(screen, (255, 0, 0), [self.centerX - self.width / 2 - camera.offsetX, self.centerY - self.height / 2 - camera.offsetY, self.width, self.height], 1)

    def collideWithCircle(self, circle):
        # complete boundbox of the rectangle
        rleft = self.centerX - self.width / 2
        rtop = self.centerY - self.height / 2
        rright = self.centerX + self.width / 2
        rbottom = self.centerY + self.height / 2
        # bounding box of the circle
        cleft, ctop = circle.centerX - circle.radius, circle.centerY - circle.radius
        cright, cbottom = circle.centerX + circle.radius, circle.centerY + circle.radius

        # trivial reject if bounding boxes do not intersect
        if rright < cleft or rleft > cright or rbottom < ctop or rtop > cbottom:
            return False  # no collision possible

        # check whether any point of rectangle is inside circle's radius
        for x in (rleft, rleft + self.width):
            for y in (rtop, rtop + self.height):
                # compare distance between circle's center point and each point of
                # the rectangle with the circle's radius
                if math.hypot(x - circle.centerX, y - circle.centerY) <= circle.radius:
                    return True  # collision detected

        # check if center of circle is inside rectangle
        if rleft <= circle.centerX <= rright and rtop <= circle.centerY <= rbottom:
            return True  # overlaid

        return False  # no collision detected