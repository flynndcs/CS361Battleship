from Bases.SceneBase import SceneBase
from Objects.GameScreenObjects import BackgroundImage, GameScreenStatusMenu
# from Objects.MasterBoard import MasterBoard
from Objects.GameScreenObjects import GameSceneManager


class GameScreen(SceneBase):
    def __init__(self, il):
        """
        title screen scene
        :param il: the imageloader
        """
        SceneBase.__init__(self, il)
        # self.master_board = MasterBoard()
        # self.OH.new_object(self.master_board)
        self.OH.new_object(BackgroundImage(self.IL))
        self.OH.new_object(GameSceneManager(self.IL, self.OH))

    def update(self):
        SceneBase.update(self)

    def render(self, screen):
        SceneBase.render(self, screen)
