'''
Author: Daniel Brezavar, Daniel Flynn
Date: 21Jul2020
Description: Class that manages interactions with the battleship board

usage: 
    player_board = BattleshipBoard()
    ai_board = BattleshipBoard()
'''

from Bases.BaseObjects import BaseObject
from Tools import Images, Sounds
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

        # sounds
        self.hit_sound = Sounds.SoundEnum.EXPLOSION
        self.miss_sound = Sounds.SoundEnum.MISS
        

#Begin Brian Additions
        #board to place ships on and check guesses against
        self.back_end_board = [[0 for x in range(10)] for y in range(10)]

        #track how many spaces each ship is occupying
        self.ship_counts = {"destroyer": 2,
                            "cruiser": 3,
                            "submarine": 3,
                            "battleship": 4,
                            "carrier": 5}
        
        #track total remaining squares occupied by ships 
        self.total_ship_positions = 0
        
    def init_back_end_board(self):
        for i in range(10):
            for j in range(10):
                self.back_end_board[i][j] = 0

    
    def add_ship(self, ship_name, ship_array):
    #     
    #     Adds ship to the back_end_board
    #     Increases total ship positions
    #  
        for location in ship_array:
            column, row = self._extract_location(location)
            intRow = int(row)
            intColumn = int(column)
            self.total_ship_positions = self.total_ship_positions + 1
            self.back_end_board[intRow][intColumn] = ship_name
    
    def _extract_location(self, location):

    #Return the row and column location as an array with 2 elements

    #Precondition: location must be in the format "a-b" where a is the row
    #              number and b is the column number

        return location.split("-")



    def check_hit(self, guess, il, oh, gpm):
    #     
    #     Check if guess was a hit or miss
    #  
        row, column = self._extract_location(guess)
        intRow = int(row)
        intColumn = int(column)
        print(intRow, intColumn)        
        boardValue = self.back_end_board[intRow][intColumn]
        for r in self.back_end_board:
            for c in r:
                print(c,end = " ")
            print()
        if boardValue == 0:
            self.back_end_board[intRow][intColumn] = "used"
            self._show_miss(il, oh)
            print("Spot was empty. Board updated to used")
            return False
        elif boardValue == "used":
            # square has already been guessed
            print("Spot has already been chosen")
            pass
        else:
            print("It's a hit! Proceed with all the updates")
            self._show_hit(il, oh)
            self.back_end_board[intRow][intColumn] = "used"            
            self.total_ship_positions = self.total_ship_positions - 1
            game_over = self._all_ships_sunk_check()
            if (game_over):
                print("Game Over Function")
                gpm.change_to_game_ending_phase(1)
                return None
            else:
                self._reduce_ship_count(boardValue)
                self._is_ship_sunk(boardValue)
            return True
    

    def get_coordinates(self, coordY, coordX):
        guess_coordinates = str(coordY) + "-" + str(coordX)
        return guess_coordinates



    def _reduce_ship_count(self, ship_name):
    #     
    #     Reduces space occupied by specific ship in dictionary
    #     after a hit
    #   
        self.ship_counts[ship_name] = self.ship_counts[ship_name] - 1
        
    

    def _is_ship_sunk(self, ship_name):
    #     
    #     Determines if the ship that was hit has been sunk
    #     

        if (self.ship_counts[ship_name] == 0):
            return ship_name
        else:
            return False



    def _all_ships_sunk_check(self):
    #     
    #     Determine if all ships have been sunk on the back_end_board. Return true 
    #     if all ships are sunk. Otherwise return false
    #     

        if (self.total_ship_positions == 0):
            return True

        return True



    def _get_back_end_board_info(self, row, column):
    #     
    #     Returns string of the back_end_board that is located at the row and column
    #     position passed into function
    #     

        return self.back_end_board[row][column]
        #End Brian Additions



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

        oh.new_object(BoardIcon(il, "HIT", icon_x, icon_y))
        oh.sound_loader.play_sound(self.hit_sound)

    def _show_miss(self, il, oh):
        icon_x = self._generate_icon_x()
        icon_y = self._generate_icon_y()

        oh.new_object(BoardIcon(il, "MISS", icon_x, icon_y))
        oh.sound_loader.play_sound(self.miss_sound)

    def determine_selection_result(self, il, oh):
        if (self.hit):
            self._show_hit(il, oh)
            self.hit = False
        else:
            self._show_miss(il, oh)
            self.hit = True
    