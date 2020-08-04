from Bases.SceneBase import SceneBase
from Objects.OptionsScreenObjects import BackgroundImage, ToMainScreen, OptionsScreenMessage, ResolutionSetting, DropDownBox, ApplyButton
from Scenes import TitleScene
import pygame


class OptionsScene(SceneBase):
    def __init__(self, il):
        """
        Options screen scene
        :param il: the imageloader
        """
        SceneBase.__init__(self, il)

        self.OH.new_object(BackgroundImage(self.IL))
        self.OH.new_object(OptionsScreenMessage(self.IL))
        self.OH.new_object(ResolutionSetting(self.IL))
        self.OH.new_object(DropDownBox(self.IL, OptionsScene))
        self.OH.new_object(ApplyButton(self.IL))
        self.OH.new_object(ToMainScreen(self.IL))

    
    def change_resolution(self, resolution):
        print("Calling change_resolution function") ## debugging line
        self.new_resolution = resolution
        print(self.new_resolution) ## debugging line

    
    def process_input(self, events, pressed_keys):
        SceneBase.process_input(self, events, pressed_keys)
        for event in events:
            location = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # if user presses return to menu button, scene is switched to title scene
                if 26 < location[0] < 307 and 912 < location[1] < 934:
                    self.switch_to_scene(TitleScene.TitleScene(self.IL))
                # if user presses the apply button, change the resolution
                if 450 < location [0] < 550 and 700 < location[1] < 740:
                    print(self.new_resolution) ## debugging line
                    self.screen = pygame.display.set_mode(self.new_resolution)


    def update(self):
        SceneBase.update(self)

    def render(self, screen):
        SceneBase.render(self, screen)