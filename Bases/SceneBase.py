import Bases.ObjectHandler
import Tools.Sounds


class SceneBase:
    def __init__(self, il):
        """
        Basest scene for the game.
        :param il: imageloader object
        """
        self.next = self  # the next scene to switch to
        self.IL = il  # image loader to make sure we are not loading images multiple times.
        self.SL = Tools.Sounds.SoundLoader()
        self.OH = Bases.ObjectHandler.ObjectHandler(self.SL)

    def process_input(self, events, pressed_keys):
        """
        fires whenever an event happens in pygame
        :param events: list of pygame events that happened
        :param pressed_keys:  long list of 0 or 1 for if a key is pressed. pygame.K_#### works in the array indexing.
        :return: None
        """
        self.OH.handle_input(events, pressed_keys)

    def update(self):
        """
        Every game tick will call an update to all objects in the OH
        :return: None
        """
        self.OH.update_objects()

    def render(self, screen):
        """
        Every game drawing tick will call to draw the objects on to the screen.
        :param screen: the pygame drawing surface we will draw stuff upon
        :return: None
        """
        self.OH.draw_objects(screen)

    def switch_to_scene(self, next_scene):
        """
        Change the scene.
        :param next_scene: The next scene to change to
        :return: None
        """
        self.next = next_scene

    def terminate(self):
        """
        Essentially exit the game by setting scene to None, handled at the battleship.py level.
        :return:
        """
        self.switch_to_scene(None)
