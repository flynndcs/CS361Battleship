from Bases.SceneBase import SceneBase
from Tools.Images import ImageEnum
from Bases.BaseObjects import BaseObject


class TitleScene(SceneBase):
    def __init__(self, il):
        """
        title screen scene
        :param il: the imageloader
        """
        SceneBase.__init__(self, il)

        self.scene_background = self.IL.load_image(ImageEnum.TitleBackground)
        self.OH.new_object(BaseObject(self.IL))  # just an example of adding an object to a scene

    def process_input(self, events, pressed_keys):
        SceneBase.process_input(self, events, pressed_keys)

    def update(self):
        SceneBase.update(self)

    def render(self, screen):
        screen.blit(self.scene_background, (0, 0))
        SceneBase.render(self, screen)
