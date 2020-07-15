from Bases.SceneBase import SceneBase
from Objects.AchievementsScreenObjects import BackgroundImage, AchievementScreenMessage


class AchievementScreen(SceneBase):
    def __init__(self, il):
        """
        Achievement screen scene
        :param il: the imageloader
        """
        SceneBase.__init__(self, il)

        self.OH.new_object(BackgroundImage(self.IL))
        self.OH.new_object(AchievementScreenMessage(self.IL))

    def process_input(self, events, pressed_keys):
        SceneBase.process_input(self, events, pressed_keys)

    def update(self):
        SceneBase.update(self)

    def render(self, screen):
        SceneBase.render(self, screen)
