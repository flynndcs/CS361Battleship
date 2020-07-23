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
        self.OH.new_object(BattleshipBoard(self.IL, 100, 150))
        self.OH.new_object(BattleshipBoard(self.IL, 550, 150))


    def update(self):
        SceneBase.update(self)

    def render(self, screen):
        SceneBase.render(self, screen)

