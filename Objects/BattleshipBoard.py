from Bases.BaseObjects import BaseObject
from Tools import Images
import pygame
from pygame import *

'''
Author: Daniel Brezavar
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

    def __init__(self, il, width, height):
        BaseObject.__init__(self, il, 100, 150)

        self.width = width
        self.height = height

        self.hoverStatus = False
        
        self.boardDisplaySource = il.load_image(Images.ImageEnum.BOARD)
        self.resizedDisplaySource = transform.scale(self.boardDisplaySource, (self.width, self.height))

        self.blackHoverImage = il.load_image(Images.ImageEnum.BLACKHOVER)
        self.resizedBlackHoverImage = transform.scale(self.blackHoverImage, (self.width, self.height))

        self.gameboard = [["0" for x in range(width)] for y in range(height)]
        self.ship_count_tracker = {}
        self.total_ship_positions = 0

    def render(self, canvas):
        canvas.blit(self.resizedDisplaySource, (self.x, self.y))

    def handle_input(self, objHandler, events, pressed_keys):
        mouseX, mouseY = pygame.mouse.get_pos()

        if (mouseX > 100 and mouseX < 900) and (mouseY > 150 and mouseY < 950):
            self.hoverStatus = True
            # print("hovering")
        
        if self.hoverStatus == True:
            # print("hovering") uncomment this for the console to log hovering 
            # once per tick

            

    def _update_ship_count_number(self, ship_name, t = 0):
        '''
        Uses the ship_count_tracker class dictionary to track the number of positions
        each ship has taken up on the board. 
        '''

        if (t == 0):
            if ship_name in self.ship_count_tracker:
                self.ship_count_tracker[ship_name] += 1
            else:
                self.ship_count_tracker[ship_name] = 1
        else:
            self.ship_count_tracker[ship_name] -= 1

    def _is_ship_sunk(self, ship_name):
        '''
        Determines if the ship that was hit has been sunk
        '''

        if (self.ship_count_tracker[ship_name] == 0):
            return True

        return False

    def _extract_location(self, location):
        '''
        Return the row and column location as an array with 2 elements

        Precondition: location must be in the format "a-b" where a is the row
                      number and b is the column number
        '''

        return location.split("-")

    def _update_location_to_used(self, row, column):
        '''
        Updates the gameboard location to "used" to signify that location has
        already been guessed
        '''

        self.gameboard[row][column] = "used"

    def _get_gameboard_info(self, row, column):
        '''
        Returns string of the gameboard that is located at the row and column
        position passed into function
        '''

        return self.gameboard[row][column]

    def _gameboard_hit(self, row, column, ship_name):
        '''
        Updates the gameboard and ship_count_tracker to account for a hit on the board.
        '''
        
        self._update_ship_count_number(ship_name, 1)
        self.total_ship_positions -= 1

    def add_ship(self, ship_name, ship_array):
        '''
        Add a ship to the game board. 

        Precondition: funtion must be passed a ship name

        Precondition: function must be passed an array of locations. Each element
                      of the location array must be structured "a-b" where a is the
                      row number and b is the column number
        '''
        for location in ship_array:
            row, column = self._extract_location(location)

            self.total_ship_positions += 1
            self.gameboard[row][column] = ship_name
            self._update_ship_count_number(ship_name, 0)

    def all_ships_sunk_check(self):
        '''
        Determine if all ships have been sunk on a gameboard. Return true if 
        all ships are sunk. Otherwise return false
        '''

        if (self.total_ship_positions == 0):
            return True

        return False

    def make_guess(self, location):
        '''
        Allows for the user or AI to make a guess on the board.

        Precondition: location must be in the format "a-b" where a is the row
                      number and b is the column number

        Return types:
            0 = Guess was a miss
            1 = Guess was a hit
            2 = Location has already been guessed
        '''

        row, column = self._extract_location(location)
        location_info = self._get_gameboard_info(row, column)

        if (location_info == "used"):
            return 2
        
        self._update_location_to_used(row, column)

        if (location_info == "0"):
            return 0
        else:
            self._gameboard_hit(row, column, location_info)
            return 1
