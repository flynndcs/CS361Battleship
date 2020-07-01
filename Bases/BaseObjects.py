import pygame.sprite


class BaseObject(pygame.sprite.Sprite):

    def __init__(self, IL, x=0, y=0):
        """
        The basest object for the game.
        :param IL: The imageloader so that we do not load an image multiple times.
        :param x: default to 0, the x position for the object
        :param y: default to 0, the y position for the object
        """
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([0, 0])

        self.width = 0
        self.height = 0
        self.x = x
        self.y = y

    def update(self, oh):
        """
        The frame update call for the object
        :param oh: the object handler for the scene
        :return: None
        """
        pass

    def render(self, canvas):
        """
        Renders the image on to the canvas
        :param canvas: The pygame surface/drawing board.
        :return: None
        """

        canvas.blit(self.image, (self.x, self.y))

    def get_dimensions(self):
        """
        Simple function to return the x, y, width, and height of an object
        :return: [x, y, width, height]
        """

        return self.x, self.y, self.width, self.height

    def handle_input(self, oh, events, pressed_keys):
        """
        Fires whenever an event happens through pygame's event system.
        :param oh: The object handler for the scene
        :param events: The list of events from pygame
        :param pressed_keys: long list of 0 or 1 for if a key is pressed. pygame.K_#### works in the array indexing.
        :return: None
        """
        pass
