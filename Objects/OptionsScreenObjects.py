from Bases.BaseObjects import BaseObject
from Tools import Images
from pygame import transform, font


class BackgroundImage(BaseObject):
    """
   Class that creates background image object and blits to screen
    """
    def __init__(self, il, x=0, y=0):
        BaseObject.__init__(self, il, x=x, y=y)

        self.width = 1000
        self.height = 955
        self.background = il.load_image(Images.ImageEnum.TitleBackground)
        self.resized_background = transform.scale(self.background,(self.width, self.height))

    def render(self, canvas):
        canvas.blit(self.resized_background, (self.x, self.y))


class OptionsScreenMessage(BaseObject):
    """
    Displays message to show user they have reached the Options screen
    """

    def __init__(self, il, x=300, y=120):
        BaseObject.__init__(self, il, x=x, y=y)

        self.font = font.Font("freesansbold.ttf", 25)
        self.game_message = self.font.render("This is the Options Screen", True, (255, 255, 255))

    def render(self, canvas):
        canvas.blit(self.game_message, (self.x, self.y))
