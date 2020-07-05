from Bases.SceneBase import SceneBase
from Tools.Images import ImageEnum
from Objects.ExampleObjects import BouncingItem
from Objects.ExampleObjects import SpinningArrow


class TitleScene(SceneBase):
    def __init__(self, il):
        """
        title screen scene
        :param il: the imageloader
        """
        SceneBase.__init__(self, il)

        self.scene_background = self.IL.load_image(ImageEnum.TitleBackground)
        self.OH.new_object(BouncingItem(self.IL))  # just an example of adding an object to a scene
        self.OH.new_object(SpinningArrow(self.IL, x=582, y=375))

    def process_input(self, events, pressed_keys):
        SceneBase.process_input(self, events, pressed_keys)

    def update(self):
        SceneBase.update(self)

    def render(self, screen):
        screen.blit(self.scene_background, (0, 0))
        SceneBase.render(self, screen)
