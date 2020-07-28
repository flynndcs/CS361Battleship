from Bases.SceneBase import SceneBase
from Objects.GameScreenObjects import BackgroundImage, GameScreenStatusMenu
# from Objects.MasterBoard import MasterBoard
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

        # self.master_board = MasterBoard()
        # self.OH.new_object(self.master_board)
        self.status_menu = GameScreenStatusMenu(self.IL)
        self.player_board = BattleshipBoard(self.IL, 100, 200)
        self.enemy_board = BattleshipBoard(self.IL, 550, 200)

        self.OH.new_object(self.player_board)
        self.OH.new_object(self.enemy_board)
        self.OH.new_object(self.status_menu)
        self.OH.new_object(GameSceneManager(self.IL, self.status_menu,
                                            self.player_board, self.enemy_board))

    def update(self):
        SceneBase.update(self)

    def render(self, screen):
        SceneBase.render(self, screen)


