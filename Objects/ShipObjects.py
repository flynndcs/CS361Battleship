from Bases.BaseObjects import BaseObject
from Tools import Images
import pygame


class BaseShip(BaseObject):

    def __init__(self, il, x=0, y=0):
        BaseObject.__init__(self, il, x=x, y=y)

        self.size = 0  # number of squares to take up

        # available directions:
        #     HORIZONTAL_RIGHT
        #     HORIZONTAL_LEFT
        #     VERTICAL_UP
        #     VERTICAL_DOWN
        self.directional_state = "HORIZONTAL_RIGHT"
        self.turned_image = None

        self.ship_game_state = "INACTIVE"

        self.grid_x = 0
        self.grid_y = 0

        self.life = []
        for segment in range(self.size):
            self.life.append(1)

    def rotate_ship_90(self):

        if self.directional_state == "HORIZONTAL_RIGHT":
            self.directional_state = "VERTICAL_DOWN"
        elif self.directional_state == "VERTICAL_DOWN":
            self.directional_state = "HORIZONTAL_LEFT"
        elif self.directional_state == "HORIZONTAL_LEFT":
            self.directional_state = "VERTICAL_UP"
        elif self.directional_state == "VERTICAL_UP":
            self.directional_state = "HORIZONTAL_RIGHT"

        self.set_rotated_image()

    def change_directional_state(self, direction):
        self.directional_state = direction
        self.set_rotated_image()

    def set_rotated_image(self):
        angles = {"HORIZONTAL_RIGHT": 0,
                  "HORIZONTAL_LEFT": 180,
                  "VERTICAL_UP": 270,
                  "VERTICAL_DOWN": 90}

        center = self.image.get_rect().center
        self.turned_image = \
            pygame.transform.rotate(self.image, angles[self.directional_state])
        new_rect = self.turned_image.get_rect(center=center)
        self.x = new_rect.topleft[0]
        self.y = new_rect.topright[0]

    def selected_placing(self):

        self.x = pygame.mouse.get_pos()[0]
        self.y = pygame.mouse.get_pos()[1]

