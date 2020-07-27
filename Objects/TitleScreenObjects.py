from Bases.BaseObjects import BaseObject
from Tools import Images
from pygame import transform, font
import pygame


class BackgroundImage(BaseObject):
    """
    Class that creates background image object and blits to canvas
    """
    def __init__(self, il, x=0, y=0):
        BaseObject.__init__(self, il, x=x, y=y)

        self.width = 1000
        self.height = 955
        self.background = il.load_image(Images.ImageEnum.TitleBackground)
        self.resized_background = transform.scale(self.background, (self.width, self.height))

    def render(self, canvas):
        canvas.blit(self.resized_background, (self.x, self.y))


class PlayButton(BaseObject):
    """
   Class that creates Start button object and blits to canvas.
    """

    def __init__(self, il, x=393, y=340):
        BaseObject.__init__(self, il, x=x, y=y)

        self.font = font.Font("Fonts/OpenSans-Light.ttf", 50)
        self.start_button = self.font.render("Start Game", True, (255, 255, 255))

    def update(self, oh):
        location = pygame.mouse.get_pos()
        # if mouse is over start button, color is changed to red
        if 382 < location[0] < 642 and 358 < location[1] < 398:
            self.start_button = self.font.render("Start Game", True, (166, 31, 36))
        else:
            self.start_button = self.font.render("Start Game", True, (255, 255, 255))

    def render(self, canvas):
        canvas.blit(self.start_button, (self.x, self.y))


class SettingsButton(BaseObject):
    """
    Class that creates options button object and blits to screen
    """

    def __init__(self, il, x=416, y=460):
        BaseObject.__init__(self, il, x=x, y=y)

        self.font = font.Font("Fonts/OpenSans-Light.ttf", 50)
        self.settings_button = self.font.render("Settings", True, (255, 255, 255))

    def update(self, oh):
        location = pygame.mouse.get_pos()
        # if mouse is over settings button, color is changed to red
        if 420 < location[0] < 591 and 434 < location[1] < 516:
            self.settings_button = self.font.render("Settings", True, (166, 31, 36))
        else:
            self.settings_button = self.font.render("Settings", True, (255, 255, 255))

    def render(self, canvas):
        canvas.blit(self.settings_button, (self.x, self.y))


class AchievementButton(BaseObject):
    """
    Class that creates achievements button object and blits to screen
    """

    def __init__(self, il, x=355, y=580):
        BaseObject.__init__(self, il, x=x, y=y)

        self.font = font.Font("Fonts/OpenSans-Light.ttf", 50)
        self.achievements_button = self.font.render("Achievements", True, (255, 255, 255))

    def update(self, oh):
        location = pygame.mouse.get_pos()
        # if mouse is over achievements button, color is changed to red
        if 355 < location[0] < 662 and 598 < location[1] < 635:
            self.achievements_button = self.font.render("Achievements", True, (166, 31, 36))
        else:
            self.achievements_button = self.font.render("Achievements", True, (255, 255, 255))

    def render(self, canvas):
        canvas.blit(self.achievements_button, (self.x, self.y))


class BattleshipTitle(BaseObject):
    """
    Class that creates battleship title object and blits to screen
    """

    def __init__(self, il, x=200, y= 120):
        BaseObject.__init__(self, il, x=x, y=y)

        self.font = font.Font("Fonts/freesansbold.ttf", 120)
        self.battleship_title = self.font.render("Battleship", True, (255, 255, 255))

    def render(self, canvas):
        canvas.blit(self.battleship_title, (self.x, self.y))



