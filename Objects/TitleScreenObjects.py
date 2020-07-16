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
        self.resized_background = transform.scale(self.background, (self.width, self.height))

    def render(self, canvas):
        canvas.blit(self.resized_background, (self.x, self.y))


class PlayButton(BaseObject):
    """
   Class that creates play button object and blits to screen
    """

    def __init__(self, il, x=380, y=340):
        BaseObject.__init__(self, il, x=x, y=y)

        self.width = 260
        self.height = 100
        self.play_button = il.load_image(Images.ImageEnum.PLAY)
        self.resized_play_button = transform.scale(self.play_button, (self.width, self.height))

    def render(self, canvas):
        canvas.blit(self.resized_play_button, (self.x, self.y))


class OptionsButton(BaseObject):
    """
    Class that creates options button object and blits to screen
    """

    def __init__(self, il, x=380, y=460):
        BaseObject.__init__(self, il, x=x, y=y)

        self.width = 260
        self.height = 100
        self.options_button = il.load_image(Images.ImageEnum.OPTIONS)
        self.resized_options_button = transform.scale(self.options_button, (self.width, self.height))

    def render(self, canvas):
        canvas.blit(self.resized_options_button, (self.x, self.y))


class AchievementButton(BaseObject):
    """
    Class that creates achievements button object and blits to screen
    """

    def __init__(self, il, x=380, y=580):
        BaseObject.__init__(self, il, x=x, y=y)

        self.width = 260
        self.height = 100
        self.achievements_button = il.load_image(Images.ImageEnum.ACHIEVEMENTS)
        self.resized_acievements_button = transform.scale(self.achievements_button, (self.width, self.height))

    def render(self, canvas):
        canvas.blit(self.resized_acievements_button, (self.x, self.y))


class BattleshipTitle(BaseObject):
    """
    Class that creates battleship title object and blits to screen
    """

    def __init__(self, il, x=200, y= 120):
        BaseObject.__init__(self, il, x=x, y=y)

        self.font = font.Font("freesansbold.ttf", 120)
        self.battleship_title = self.font.render("Battleship", True, (255, 255, 255))

    def render(self, canvas):
        canvas.blit(self.battleship_title, (self.x, self.y))



