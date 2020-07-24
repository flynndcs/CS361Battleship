from Bases.BaseObjects import BaseObject
from Tools import Images
import pygame
from pygame import *

'''
Author: Daniel Brezavar
Daniel Flynn
Date: 21Jul2020
Description: Class that manages interactions with the battleship board

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

        #upper left corner of where object is created in scene
        self.x = x
        self.y = y

        #drawing surface 
        self.image = Surface([self.width, self.height])

        #eventually will be used for ship/shot logic
        self.selectedBoardPosition = None 

        #source of rectangles that outline board positions and handle interaction
        self.boardPositions = [[] for y in range(10)] 

        #the blank rectangle for when a user is not hovering over it
        self.rect = pygame.Surface([35, 35])
        # self.rect.set_alpha(0)
        self.rect.fill((255,255,255))

        self.init_board_positions()
        
        self.ship_count_tracker = {}
        self.total_ship_positions = 0
    
    def init_board_positions(self):
        for i in range(10):
            for j in range(10):
                self.boardPositions[i].append(self.image.blit(self.rect, ((i * 40), (j * 40))))

    def render(self, canvas):
        canvas.blit(self.image, (self.x, self.y))
    
    def confirm_shot_dialog(self, boardPosition):
        shot_dialog = pygame.Surface([100, 50])
        shot_dialog.fill((0,0,255))
        self.image.blit(shot_dialog, boardPosition)

    def handle_input(self, objHandler, events, pressed_keys):
        mouseX, mouseY = pygame.mouse.get_pos()

        #on any event, this checks all squares to see if they were hovered over
        #this is local
        for i in range(10):
            for j in range(10):
                if self.boardPositions[i][j].collidepoint(mouseX - self.x, mouseY - self.y):
                    if self.selectedBoardPosition is not None:
                        self.image.blit(self.rect, self.selectedBoardPosition)

                    self.selectedBoardPosition = self.boardPositions[i][j]
                    highlightRect = pygame.Surface([35,35])
                    highlightRect.fill((255,0,0))
                    self.image.blit(highlightRect, self.boardPositions[i][j])
    
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
