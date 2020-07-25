from Bases.BaseObjects import BaseObject
from Tools import Images
import pygame
from pygame import *

'''
Author: Daniel Brezavar
Daniel Flynn
Date: 21Jul2020
Description: Class that keeps track of ship positions and has methods for interacting
             with the game board.

usage: 
    player_board = BattleshipBoard()
    ai_board = BattleshipBoard()
'''

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

        self.current_position_x = -1
        self.current_position_y = -1
        self.activated_position = False
        self.activated_board = True

        #upper left corner of where object is created in scene
        self.x = x
        self.y = y

        #the image behind the board (TODO: will be seen easier when board positions are transparent)
        self.boardImage= il.load_image(Images.ImageEnum.BOARD)
        self.resizedBoardImage = transform.scale(self.boardImage, (self.width, self.height))

        #drawing surface that image placed upon
        self.image = Surface([self.width, self.height])
        self.image = self.resizedBoardImage

        #eventually will be used for ship/shot logic
        self.selectedBoardPosition = None 

        #may be used for holding all ships, shots, ai logic
        self.masterGameBoard = [["0" for x in range(10)] for y in range(10)]

        #source of rectangles that outline board positions and handle interaction
        self.boardPositions = [[] for y in range(10)] 

        #the rectangle for when a user is not hovering over it
        self.rect = pygame.Surface([35, 35])
        self.rect.fill((255,255,255))

        #initialized boardPositions - this blits the grid of rectangles to the screen and 
        #also stores their screen locations in boardPositions
        for i in range(10):
            for j in range(10):
                self.boardPositions[i].append(self.image.blit(self.rect, ((i * 40), (j * 40))))

        self.ship_count_tracker = {}
        self.total_ship_positions = 0

    def render(self, canvas):
        canvas.blit(self.image, (self.x, self.y))

    def _check_valid_mouse_position(self, position):
        '''
        Check that that mouse is on a valid mouse position
        '''

        if (position >= 0 and position < 400):
            return True

        if (self.activated_position):
            self._clear_position(self.current_position_x, self.current_position_y)

        return False

    def _activate_position(self, x, y):
        '''
        changes a board position to red
        '''
        red_rect = pygame.Surface([35,35])
        red_rect.fill((255,0,0))
        self.image.blit(red_rect, self.boardPositions[x][y])

        self.activated_position = True


    def _clear_position(self, x, y):
        '''
        changes a board position to white
        '''
        empty_rect = pygame.Surface([35,35])
        empty_rect.fill((255,255,255))
        self.image.blit(empty_rect, self.boardPositions[x][y])

        self.activated_position = False

    def _check_board_position(self):
        '''
        Determines where the mouse positions is located and if a square should be highlighted
        '''
        mouse_x, mouse_y = pygame.mouse.get_pos()

        mouse_position_x = mouse_x - self.x
        mouse_position_y = mouse_y - self.y
        board_position_x = int(mouse_position_x / 40)
        board_position_y = int(mouse_position_y / 40)

        if (self._check_valid_mouse_position(mouse_position_x) and self._check_valid_mouse_position(mouse_position_y)):
            if (not self.activated_position and self.current_position_x != -1):
                self._activate_position(self.current_position_x, self.current_position_y)

            if (self.current_position_x != board_position_x or self.current_position_y != board_position_y):
                self._change_positions(self.current_position_x,
                                       self.current_position_y,
                                       board_position_x,
                                       board_position_y)

    def _change_positions(self, old_x, old_y, new_x, new_y):
        '''
        Highlights the new position red and clears the old position
        '''
        if (old_x >= 0 and old_y >= 0):
            self._clear_position(old_x, old_y)

        self._activate_position(new_x, new_y)

        self.current_position_x = new_x
        self.current_position_y = new_y

    def handle_input(self, objHandler, events, pressed_keys):
        '''
        Determines if the board is activated and calls functions to check board positions
        '''

        if (self.activated_board):
            self._check_board_position()

    def activate_board(self):
        '''
        Allows the user to highlight squares on the board
        '''
        self.activated_board = True

    def deactivate_board(self):
        '''
        Prohibits the user from highlighting squares on the board
        '''
        self.activated_board = False

    # def _update_ship_count_number(self, ship_name, t = 0):
    #     '''
    #     Uses the ship_count_tracker class dictionary to track the number of positions
    #     each ship has taken up on the board. 
    #     '''

    #     if (t == 0):
    #         if ship_name in self.ship_count_tracker:
    #             self.ship_count_tracker[ship_name] += 1
    #         else:
    #             self.ship_count_tracker[ship_name] = 1
    #     else:
    #         self.ship_count_tracker[ship_name] -= 1

    # def _is_ship_sunk(self, ship_name):
    #     '''
    #     Determines if the ship that was hit has been sunk
    #     '''

    #     if (self.ship_count_tracker[ship_name] == 0):
    #         return True

    #     return False

    # def _extract_location(self, location):
    #     '''
    #     Return the row and column location as an array with 2 elements

    #     Precondition: location must be in the format "a-b" where a is the row
    #                   number and b is the column number
    #     '''

    #     return location.split("-")

    # def _update_location_to_used(self, row, column):
    #     '''
    #     Updates the gameboard location to "used" to signify that location has
    #     already been guessed
    #     '''

    #     self.gameboard[row][column] = "used"

    # def _get_gameboard_info(self, row, column):
    #     '''
    #     Returns string of the gameboard that is located at the row and column
    #     position passed into function
    #     '''

    #     return self.gameboard[row][column]

    # def _gameboard_hit(self, row, column, ship_name):
    #     '''
    #     Updates the gameboard and ship_count_tracker to account for a hit on the board.
    #     '''
        
    #     self._update_ship_count_number(ship_name, 1)
    #     self.total_ship_positions -= 1

    # def add_ship(self, ship_name, ship_array):
    #     '''
    #     Add a ship to the game board. 

    #     Precondition: funtion must be passed a ship name

    #     Precondition: function must be passed an array of locations. Each element
    #                   of the location array must be structured "a-b" where a is the
    #                   row number and b is the column number
    #     '''
    #     for location in ship_array:
    #         row, column = self._extract_location(location)

    #         self.total_ship_positions += 1
    #         self.gameboard[row][column] = ship_name
    #         self._update_ship_count_number(ship_name, 0)

    # def all_ships_sunk_check(self):
    #     '''
    #     Determine if all ships have been sunk on a gameboard. Return true if 
    #     all ships are sunk. Otherwise return false
    #     '''

    #     if (self.total_ship_positions == 0):
    #         return True

    #     return False

    # def make_guess(self, location):
    #     '''
    #     Allows for the user or AI to make a guess on the board.

    #     Precondition: location must be in the format "a-b" where a is the row
    #                   number and b is the column number

    #     Return types:
    #         0 = Guess was a miss
    #         1 = Guess was a hit
    #         2 = Location has already been guessed
    #     '''

    #     row, column = self._extract_location(location)
    #     location_info = self._get_gameboard_info(row, column)

    #     if (location_info == "used"):
    #         return 2
        
    #     self._update_location_to_used(row, column)

    #     if (location_info == "0"):
    #         return 0
    #     else:
    #         self._gameboard_hit(row, column, location_info)
    #         return 1
