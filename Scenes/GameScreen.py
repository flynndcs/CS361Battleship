from Bases.SceneBase import SceneBase
from Objects.GameScreenObjects import BackgroundImage, GameScreenMessage
from Objects.BattleshipBoard import BattleshipBoard


class GameScreen(SceneBase):
    def __init__(self, il):
        """
        title screen scene
        :param il: the imageloader
        """
        SceneBase.__init__(self, il)
        self.OH.new_object(BackgroundImage(self.IL))
        self.OH.new_object(GameScreenMessage(self.IL))
        self.OH.new_object(BattleshipBoard(self.IL, 800, 500))

    def update(self):
        SceneBase.update(self)

    def render(self, screen):
        SceneBase.render(self, screen)

