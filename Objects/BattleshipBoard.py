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

class HitIcon(BaseObject):
    def __init__(self, il, x=0, y=0):
        BaseObject.__init__(self, il, x=x, y=y)

        self.image = il.load_image(Images.ImageEnum.HIT)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

class MissIcon(BaseObject):
    def __init__(self, il, x=0, y=0):
        BaseObject.__init__(self, il, x=x, y=y)

        self.image = il.load_image(Images.ImageEnum.MISS)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

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

    def confirm_shot(self):
        mouseX, mouseY = pygame.mouse.get_pos()
    #     for button in self.confirm_deny_buttons:
    #     print("confirm within dialog class")
    #     hit_or_miss = pygame.Surface([99,49])
    #     hit_or_miss.fill((0,255,0))
        
    #     font = pygame.font.Font(pygame.font.get_default_font(),50)
    #     text = font.render('Hit', True, (0,0,0))
    #     hit_or_miss.blit(text, (0,0))
    #     self.image.blit(hit_or_miss, (0,0))


# Brian Add

class ShipTracker():
    def __init___(self):
        self.gameboard = [[0 for i in range(10)] for j in range(10)]
        self.ship_counts = {}
        self.total_ship_positions = 0


    def add_ship(self, ship_name, ship_array):

        for location in ship_array:
            row = self._extract_location(location)
            column = self._extract_location(location)

        self.total_ship_positions = self.total_ship_positions + 1
        self.gameboard[row][column] = ship_name
        self._update_ship_count_number(ship_name, 0)

    
    def _extract_location(self, location):
    
    #     Return the row and column location as an array with 2 elements

    #     Precondition: location must be in the format "a-b" where a is the row
    #                   number and b is the column number

        return location.split("-")

    
    def _update_ship_count_number(self, ship_name, t = 0):
    #     '''
    #     Uses the ship_count_tracker class dictionary to track the number of positions
    #     each ship has taken up on the board. 
    #     '''

         if (t == 0):
             if ship_name in self.ship_counts:
                 self.ship_counts[ship_name] += 1
             else:
                 self.ship_counts[ship_name] = 1
         else:
             self.ship_counts[ship_name] -= 1


    def check_hit(self, guess):

        arrayLoc = _extract_location(self, guess)
        if self.gameboard[arrayLoc[0]][arrayLoc[1]] != 0
            return [True, gameboard[arrayLoc[0]][arrayLoc[1]]]
    
    
    def _is_ship_sunk(self, ship_name):
    #     '''
    #     Determines if the ship that was hit has been sunk
    #     '''

         if (self.ship_counts[ship_name] == 0):
             return True

         return False

    def all_ships_sunk_check(self):
    #     '''
    #     Determine if all ships have been sunk on a gameboard. Return true if 
    #     all ships are sunk. Otherwise return false
    #     '''

         if (self.total_ship_positions == 0):
             return True

         return False



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

        #upper left corner of where board is created in scene
        self.x = x
        self.y = y

        #dialog position
        self.dialogX = None
        self.dialogY = None

        #drawing surface 
        self.image = Surface([self.width, self.height])
        self.image.fill((255, 255, 255))

        #dialog box open
        self.dialogOpen = False
        self.dialogPositions = []
        self.dialogBoxPosition = [self.x, self.y]

        #source of rectangles that outline board positions and handle interaction
        self.boardPositions = [[] for y in range(10)] 

        #the blank rectangle for when a user is not hovering over it
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
        self.image.fill((255,255,255))
        for i in range(10):
            for j in range(10):
                self.image.blit(self.rect, ((i*40), (j * 40)))
    
    def init_board_positions(self):
        for i in range(10):
            for j in range(10):
                self.boardPositions[i].append(self.image.blit(self.rect, ((i * 40), (j * 40))))

    def render(self, canvas):
        canvas.blit(self.image, (self.x, self.y))
    
    def confirm_shot_dialog(self, boardPosition):
        shot_dialog = pygame.Surface([100, 51])
        shot_dialog.fill((0,0,255))

        confirm = pygame.Surface([35, 35])
        confirm.fill((0,255,0))

        deny = pygame.Surface([35, 35])
        deny.fill((255,0,0))

        self.dialogPositions.append(shot_dialog.blit(confirm, (10, 8)))
        self.dialogPositions.append(shot_dialog.blit(deny, (55, 8)))

        print(self.dialogPositions)

        self.image.blit(shot_dialog, boardPosition)

    def hoverHighlight(self, boardPosition):
        highlightRect = pygame.Surface([35,35])
        highlightRect.fill((255,0,0))
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

        oh.new_object(HitIcon(il, icon_x, icon_y))

    def _show_miss(self, il, oh):
        icon_x = self._generate_icon_x()
        icon_y = self._generate_icon_y()

        oh.new_object(MissIcon(il, icon_x, icon_y))

    def determine_selection_result(self, il, oh):
        if (self.hit):
            self._show_hit(il, oh)
            self.hit = False
        else:
            self._show_miss(il, oh)
            self.hit = True
        
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
