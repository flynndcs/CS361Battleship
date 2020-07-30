from Bases.BaseObjects import BaseObject
from Tools import Images
import pygame


class BackgroundImage(BaseObject):
    """
   Class that creates background image object and blits to screen
    """
    def __init__(self, il, x=0, y=0):
        BaseObject.__init__(self, il, x=x, y=y)

        self.width = 1000
        self.height = 955
        self.background = il.load_image(Images.ImageEnum.TitleBackground)
        self.resized_background = pygame.transform.scale(self.background,(self.width, self.height))

    def render(self, canvas):
        canvas.blit(self.resized_background, (self.x, self.y))


class OptionsScreenMessage(BaseObject):
    """
    Displays message to show user they have reached the Options screen
    """

    def __init__(self, il, x = 230, y = 120):
        BaseObject.__init__(self, il, x=x, y=y)

        self.font = pygame.font.Font("Fonts/freesansbold.ttf", 120)
        self.options = self.font.render("Settings", True, (255, 255, 255))

    def render(self, canvas):
        canvas.blit(self.options, (self.x, self.y))


class ToMainScreen(BaseObject):
    """
    Returns users to the main screen
    """

    def __init__(self, il, x=23, y=900):
        BaseObject.__init__(self, il, x=x, y=y)

        self.font = pygame.font.Font("Fonts/OpenSans-Light.ttf", 30)
        self.start_button = self.font.render("Return to Main Menu", True, (255, 255, 255))

    def update(self, oh):
        location = pygame.mouse.get_pos()
        # if mouse is over to main screen button, color is changed to red
        if 26 < location[0] < 307 and 912 < location[1] < 934:
            self.start_button = self.font.render("Return to Main Menu", True, (166, 31, 36))
        else:
            self.start_button = self.font.render("Return to Main Menu", True, (255, 255, 255))

    def render(self, canvas):
        canvas.blit(self.start_button, (self.x, self.y))