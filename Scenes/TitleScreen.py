from Bases.SceneBase import SceneBase
from Objects.TitleScreenObjects import BackgroundImage, PlayButton, OptionsButton, AchievementButton, BattleshipTitle
import pygame
from Scenes.GameScreen import GameScreen
from Scenes.OptionsScreen import OptionsScreen
from Scenes.AchievementsScreen import AchievementScreen


class TitleScene(SceneBase):
    def __init__(self, il):
        """
        Title screen scene
        :param il: the imageloader
        """
        SceneBase.__init__(self, il)
        self.OH.new_object(BackgroundImage(self.IL))
        self.OH.new_object(PlayButton(self.IL))
        self.OH.new_object(OptionsButton(self.IL))
        self.OH.new_object(AchievementButton(self.IL))
        self.OH.new_object(BattleshipTitle(self.IL))

    def process_input(self, events, pressed_keys):
        SceneBase.process_input(self, events, pressed_keys)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos()
                # user presses play button, screen is switched to game screen
                if 384 < location[0] < 634 and 340 < location[1] < 437:
                    self.switch_to_scene(GameScreen(self.IL))
                # user presses options button, screen is switched to options screen
                if 384 < location[0] < 634 and 463 < location[1] < 557:
                    self.switch_to_scene(OptionsScreen(self.IL))
                # user presses achievements button, screen is switched to achievements screen
                if 384 < location[0] < 634 and 583 < location[1] < 674:
                    self.switch_to_scene(AchievementScreen(self.IL))

    def update(self):
        SceneBase.update(self)

    def render(self, screen):
        SceneBase.render(self, screen)