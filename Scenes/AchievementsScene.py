from Bases.SceneBase import SceneBase
from Objects.AchievementsScreenObjects import BackgroundImage, ToMainScreen
from Scenes import TitleScene
import pygame

class AchievementScene(SceneBase):
    def __init__(self, il):
        """
        Achievement screen scene
        :param il: the imageloader
        """
        SceneBase.__init__(self, il)

        self.OH.new_object(BackgroundImage(self.IL))
        self.OH.new_object(ToMainScreen(self.IL))

    def process_input(self, events, pressed_keys):
        SceneBase.process_input(self, events, pressed_keys)
        SceneBase.process_input(self, events, pressed_keys)
        for event in events:
            location = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # if user presses return to menu button, scene is switched to title scene
                if 26 < location[0] < 307 and 912 < location[1] < 934:
                    self.switch_to_scene(TitleScene.TitleScene(self.IL))


    def update(self):
        SceneBase.update(self)

    def render(self, screen):
        SceneBase.render(self, screen)
