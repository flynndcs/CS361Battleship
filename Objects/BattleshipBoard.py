'''
Author: Daniel Brezavar, Daniel Flynn
Date: 21Jul2020
Description: Class that manages interactions with the battleship board

usage: 
    player_board = BattleshipBoard()
    ai_board = BattleshipBoard()
'''
from Bases.BaseObjects import BaseObject
from Tools import Images
import pygame
from pygame import *



class BoardIcon(BaseObject):
    def __init__(self, il, icon_type, x=0, y=0):
        BaseObject.__init__(self, il, x=x, y=y)

        if (icon_type == "HIT"):
            self.image = il.load_image(Images.ImageEnum.HIT)
        elif (icon_type == "MISS"):
            self.image = il.load_image(Images.ImageEnum.MISS)

        self.width = self.image.get_width()
        self.height = self.image.get_height()


class Animating:
    def __init__(self):
        self.animating = False

    def set_animating(self, value):
        self.animating = value

    def get_animating(self):
        return self.animating




class TargetIcon(BaseObject):
    """TargetIcon position moves through random points in coordinates array until it reaches the end of the array and it is
    removed from screen"""

    def __init__(self, il, x, y, coord, oh, animating):
        BaseObject.__init__(self, il, x, y)
        self.image = il.load_image(Images.ImageEnum.TARGET)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.coord = coord
        self.position = 0
        self.speed = 1
        oh.new_object(self)
        self.animating = animating


    def update(self, oh):
        """Updates x/y variables to move target position"""
        if self.x == self.coord[self.position][0] and self.y == self.coord[self.position][1]:
            if self.position == len(self.coord) - 1:
                self.animating.set_animating(False)
                oh.remove_object(self)
                print(self.animating.get_animating())
            else:
                self.position += 1

        if self.position != len(self.coord):

            if self.position == len(self.coord) - 1:
                self.speed = 0.5

            if self.x < self.coord[self.position][0]:
                self.x += 10 * self.speed

            if self.y < self.coord[self.position][1]:
                self.y += 10 * self.speed

            if self.y > self.coord[self.position][1]:
                self.y -= 10 * self.speed

            if self.x > self.coord[self.position][0]:
                self.x -= 10 * self.speed
    #
    # def get_move(self):
    #     return self.move

class DialogBox(BaseObject):
    confirm_deny_buttons = []
    def __init__(self, il, x=0, y=0):
        BaseObject.__init__(self, il, x=x, y=y)
        self.width = 100
        self.height = 50
        self.x = x
        self.y = y

        self.confirmX = self.x + 10
        self.confirmY = self.y + 8

        self.denyX = self.x + 55
        self.denyY = self.y + 8

        self.image = Surface([self.width, self.height])

        self.init_confirm_deny_buttons()

    def init_confirm_deny_buttons(self):
        self.image.fill((0,0,255))
        confirm = pygame.Surface([35, 35])
        confirm.fill((0,255,0))

        deny = pygame.Surface([35, 35])
        deny.fill((255,0,0))

        self.confirm_deny_buttons.append(self.image.blit(confirm, (self.confirmX, self.confirmY)))
        self.confirm_deny_buttons.append(self.image.blit(deny, (self.denyX, self.denyY)))

class BattleshipBoard(BaseObject):
    '''
    Keep track of ship positions and create functionality for interacting
    with the game board.
    Attributes:
        gameboard               2D board that keeps track of ship positions
                                    "0" = No ship located at position
                                    "ship_name" = ship located at position
                                    "used" = location has already been guessed
        ship_count_tracker      Keeps track of each ship and the number of positions
                                that they take up on the board
        total_ship_positions    The number of remaining ship positions that have not
                                been hit
    '''

    def __init__(self, il, x, y):
        BaseObject.__init__(self, il, x=0, y=0)

        # size of board, may need to change if scaling
        self.width = 400
        self.height = 400

        # upper left corner of where board is created in scene
        self.x = x
        self.y = y

        # dialog position
        self.dialogX = None
        self.dialogY = None

        # drawing surface
        self.image = Surface([self.width, self.height])
        self.image.fill((255, 255, 255))

        # dialog box open
        self.dialogOpen = False
        self.dialogPositions = []
        self.dialogBoxPosition = [self.x, self.y]

        # source of rectangles that outline board positions and handle interaction
        self.boardPositions = [[] for y in range(10)]

        # the blank rectangle for when a user is not hovering over it
        self.rect = pygame.Surface([35, 35])
        self.rect.set_alpha(50)
        self.rect.fill((0, 0, 255))

        self.init_board_positions()

        self.hit = True
        self.selection_x = -1
        self.selection_y = -1

        # self.ship_count_tracker = {}
        # self.total_ship_positions = 0

    def clear_board(self, oh, surface):
        if surface:
            oh.remove_object(surface)
        self.image.fill((255, 255, 255))
        for i in range(10):
            for j in range(10):
                self.image.blit(self.rect, ((i * 40), (j * 40)))

    def init_board_positions(self):
        for i in range(10):
            for j in range(10):
                self.boardPositions[i].append(self.image.blit(self.rect, ((i * 40), (j * 40))))

    def render(self, canvas):
        canvas.blit(self.image, (self.x, self.y))

    def confirm_shot_dialog(self, boardPosition):
        shot_dialog = pygame.Surface([100, 51])
        shot_dialog.fill((0, 0, 255))

        confirm = pygame.Surface([35, 35])
        confirm.fill((0, 255, 0))

        deny = pygame.Surface([35, 35])
        deny.fill((255, 0, 0))

        self.dialogPositions.append(shot_dialog.blit(confirm, (10, 8)))
        self.dialogPositions.append(shot_dialog.blit(deny, (55, 8)))

        print(self.dialogPositions)

        self.image.blit(shot_dialog, boardPosition)

    def hoverHighlight(self, boardPosition):
        highlightRect = pygame.Surface([35, 35])
        highlightRect.fill((255, 0, 0))
        self.image.blit(highlightRect, boardPosition)

    def set_square_selection(self, x, y):
        self.selection_x = x
        self.selection_y = y

    def _generate_icon_x(self):
        return self.x + (self.selection_x * 40)

    def _generate_icon_y(self):
        return self.y + (self.selection_y * 40)

    def _show_hit(self, il, oh):
        icon_x = self._generate_icon_x()
        icon_y = self._generate_icon_y()

        oh.new_object(BoardIcon(il, "HIT", icon_x, icon_y))

    def _show_miss(self, il, oh):
        icon_x = self._generate_icon_x()
        icon_y = self._generate_icon_y()

        oh.new_object(BoardIcon(il, "MISS", icon_x, icon_y))

    def show_target(self, il, oh, coord, animating):

        for x in range(len(coord)):
            self.set_square_selection(coord[x][0], coord[x][1])
            icon_x = self._generate_icon_x()
            icon_y = self._generate_icon_y()
            coord[x][0] = icon_x
            coord[x][1] = icon_y
        # return coord
        TargetIcon(il, coord[0][0], coord[0][1], coord, oh, animating)

    # def convert_coordinates(self, il, oh, coord):
    #
    #     for x in range(len(coord)):
    #         self.set_square_selection(coord[x][0], coord[x][1])
    #         icon_x = self._generate_icon_x()
    #         icon_y = self._generate_icon_y()
    #         coord[x][0] =icon_x
    #         coord[x][1] = icon_y
    #     return coord

    # oh.new_object(TargetIcon(il, icon_x, icon_y, coord))

    def determine_selection_result(self, il, oh):
        if (self.hit):
            self._show_hit(il, oh)
            self.hit = False
        else:
            self._show_miss(il, oh)
            self.hit = True

