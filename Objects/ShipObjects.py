from Bases.BaseObjects import BaseObject
from Tools import Images
import pygame


class BaseShip(BaseObject):

    def __init__(self, il, name, x=0, y=0):
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

        self.selected_x = self.x
        self.selected_y = self.y

        self.selected = False

        self.name = name
        self.size = {"submarine": 3,
                     "carrier": 5,
                     "battleship": 4,
                     "cruiser": 3,
                     "destroyer": 2}[self.name]
        self.image = {"submarine": il.load_image(Images.ImageEnum.SUBMARINE),
                      "carrier": il.load_image(Images.ImageEnum.AIRCRAFTCARRIER),
                      "battleship": il.load_image(Images.ImageEnum.BATTLESHIP),
                      "cruiser": il.load_image(Images.ImageEnum.CRUISER),
                      "destroyer": il.load_image(Images.ImageEnum.PATROLBOAT)}[self.name]

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
                  "VERTICAL_UP": 90,
                  "VERTICAL_DOWN": 270}
        center = (self.x + self.width, self.y + self.height)
        self.turned_image = \
            pygame.transform.rotate(self.image, angles[self.directional_state])
        # new_rect = self.turned_image.get_rect(center=center)
        # self.x = new_rect.topleft[0]
        # self.y = new_rect.topright[0]
        self.width = self.turned_image.get_width()
        self.height = self.turned_image.get_height()

    def selected_placing(self):

        self.x = pygame.mouse.get_pos()[0]
        self.y = pygame.mouse.get_pos()[1]

    def render(self, canvas):
        if self.turned_image:
            canvas.blit(self.turned_image, (self.x, self.y))
        else:
            BaseShip.render(self, canvas)

    def update(self, oh):
        if self.selected:
            if self.directional_state == "HORIZONTAL_RIGHT":
                self.x = self.selected_x
                self.y = self.selected_y

            elif self.directional_state == "VERTICAL_DOWN":
                self.x = self.selected_x
                self.y = self.selected_y

            elif self.directional_state == "HORIZONTAL_LEFT":
                self.x = self.selected_x - self.width
                self.y = self.selected_y

            elif self.directional_state == "VERTICAL_UP":
                self.x = self.selected_x
                self.y = self.selected_y - self.height

    def change_base_coords(self):
        if self.directional_state == "HORIZONTAL_RIGHT":
            self.x = self.selected_x
            self.y = self.selected_y

        elif self.directional_state == "VERTICAL_DOWN":
            self.x = self.selected_x
            self.y = self.selected_y

        elif self.directional_state == "HORIZONTAL_LEFT":
            self.x = self.selected_x - self.width
            self.y = self.selected_y

        elif self.directional_state == "VERTICAL_UP":
            self.x = self.selected_x
            self.y = self.selected_y - self.height

    def scale_ship(self, new_x, new_y, offset_size):

        self.image = pygame.transform.scale(self.image, (new_x*self.size - offset_size, new_y - offset_size))
