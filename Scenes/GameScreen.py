from Bases.SceneBase import SceneBase
from Scenes import TitleScene
from Objects.GameScreenObjects import BackgroundImage, GameScreenStatusMenu, ToMainScreen
# from Objects.MasterBoard import MasterBoard
from Objects.GameScreenObjects import GameSceneManager
import pygame


class GameScreen(SceneBase, ToMainScreen):
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
        self.OH.new_object(ToMainScreen(self.IL))
        self.click_num = 0

    def process_input(self, events, pressed_keys):
        SceneBase.process_input(self, events, pressed_keys)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos()
                # if user clicks to quit game, click_num is incremented
                if 23 < location[0] < 169 and 910 < location[1] < 935 and self.click_num == 0:
                    self.click_num += 1
                # if user clicks to confirm quit, game is terminated
                elif 23 < location[0] < 312 and 911 < location[1] < 935 and self.click_num == 1:
                    self.switch_to_scene(TitleScene.TitleScene(self.IL))
                # user does not confirm to quit, click number is reset
                else:
                    self.click_num = 0

    def update(self):
        SceneBase.update(self)

    def render(self, screen):
        SceneBase.render(self, screen)

