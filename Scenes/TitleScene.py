from Bases.SceneBase import SceneBase
from Objects.TitleScreenObjects import *
from Scenes.GameScreen import GameScreen
from Scenes.OptionsScene import OptionsScene
from Scenes.AchievementsScene import AchievementScene
import pygame


class TitleScene(SceneBase):
    def __init__(self, il):
        """
        Title screen scene
        :param il: the imageloader
        """
        SceneBase.__init__(self, il)
        self.OH.new_object(BackgroundImage(self.IL))
        self.OH.new_object(PlayButton(self.IL))
        self.OH.new_object(SettingsButton(self.IL))
        self.OH.new_object(AchievementButton(self.IL))
        self.OH.new_object(BattleshipTitle(self.IL))
        self.OH.new_object(ExitGame(self.IL))

    
    def process_input(self, events, pressed_keys):
        SceneBase.process_input(self, events, pressed_keys)
        for event in events:
            location = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # user presses play button, screen is switched to game screen
                if 382 < location[0] < 642 and 358 < location[1] < 398:
                    self.switch_to_scene(GameScreen(self.IL))
                # user presses settings button, screen is switched to settings screen
                if 420 < location[0] < 591 and 434 < location[1] < 516:
                    self.switch_to_scene(OptionsScene(self.IL))
                # user presses achievements button, screen is switched to achievements screen
                if 355 < location[0] < 662 and 598 < location[1] < 635:
                    self.switch_to_scene(AchievementScene(self.IL))
                # user presses exit game button, game is terminated
                if 25 < location[0] < 159 and 912 < location[1] < 935:
                    self.terminate()

    def update(self):
        SceneBase.update(self)

    def render(self, screen):
        SceneBase.render(self, screen)