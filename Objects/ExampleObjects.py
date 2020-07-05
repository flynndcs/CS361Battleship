from Bases.BaseObjects import BaseObject
import pygame
from Tools import Images
from pygame import transform


class BouncingItem(BaseObject):

    def __init__(self, il, x=0, y=0):
        BaseObject.__init__(self, il, x=x, y=y)

        self.width = 50
        self.height = 50

        self.xdir = 1
        self.ydir = 1

        self.speed = 2

    def update(self, oh):

        self.x += self.speed * self.xdir
        self.y += self.speed * self.ydir

        if self.x > 1200 - self.width or self.x < 0:
            self.xdir *= -1

        if self.y > 800 - self.height or self.y < 0:
            self.ydir *= -1

    def render(self, canvas):

        pygame.draw.rect(canvas, (255, 0, 0), pygame.Rect(self.x, self.y, self.width, self.height))


class SpinningArrow(BaseObject):

    def __init__(self, il, x=0, y=0):
        BaseObject.__init__(self, il, x=x, y=y)

        self.width = 25
        self.height = 25

        self.image = il.load_image(Images.ImageEnum.ARROW)
        self.rotated_image = transform.rotate(self.image, 0)
        self.angle = 0

    def update(self, oh):
        self.angle += 0.2
        self.rotated_image = transform.rotate(self.image, self.angle)

    def render(self, canvas):
        canvas.blit(self.rotated_image, (self.x, self.y))
