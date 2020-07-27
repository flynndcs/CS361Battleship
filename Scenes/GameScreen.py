from Bases.SceneBase import SceneBase
from Objects.GameScreenObjects import BackgroundImage
from Objects.BattleshipBoard import BattleshipBoard
from Objects.GameScreenObjects import GameSceneManager


class GameScreen(SceneBase):
    def __init__(self, il):
        """
        title screen scene
        :param il: the imageloader
        """
        SceneBase.__init__(self, il)
        self.OH.new_object(BackgroundImage(self.IL))
        self.player_board = BattleshipBoard(self.IL, 100, 150)
        self.OH.new_object(self.player_board)
        self.enemy_board = BattleshipBoard(self.IL, 550, 150)
        self.OH.new_object(self.enemy_board)
        self.OH.new_object(GameSceneManager(self.IL, self.player_board,
                           self.enemy_board))

    def update(self):
        SceneBase.update(self)

    def render(self, screen):
        SceneBase.render(self, screen)


