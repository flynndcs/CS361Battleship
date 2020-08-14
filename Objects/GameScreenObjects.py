import Objects.ShipObjects
import Objects.BattleshipBoard
import pygame.mouse
from Objects.BattleshipBoard import BattleshipBoard
from Bases.BaseObjects import BaseObject
from Tools import Images
from pygame import transform, font
from random import randrange
from os import path, mkdir
from datetime import datetime
from Tools.Sounds import SoundEnum
import Objects.BattleshipAI


class GameScreenStatusMenu(BaseObject):
    '''
    Author: Daniel Brezavar
    Description: Displays game status and actions required for the user
    '''

    def __init__(self, il, x=0, y= 0):
        BaseObject.__init__(self, il, x=x, y=y)

        self.font1 = font.Font("Fonts/OpenSans-Light.ttf", 20)
        self.font2 = font.Font("Fonts/OpenSans-Light.ttf", 18)

        self.window_width, self.window_height = pygame.display.get_surface().get_size()

        self.border_width = 700
        self.border_height = 80
        self.border_circle_radius = 10
        self.border_x = int((self.window_width - self.border_width) / 2)

        self.title = "Status Menu"
        self.title_x = x + 22
        self.title_y = y - 33

        self.status = ""
        self.status_x = self.border_x + 15
        self.status_y = y + 10

        self.action = ""
        self.action_x = self.border_x + 15
        self.action_y = y + 40

    def _get_formatted_status_message(self):
        '''
        Returns the status message with font format
        '''
        message = "Phase: " + self.status
        return self.font2.render(message, True, (0, 0, 0))

    def _render_status(self, canvas):
        '''
        Renders the status message in the status menu
        '''
        message = self._get_formatted_status_message()
        canvas.blit(message, (self.status_x, self.status_y))

    def _get_formatted_action_message(self):
        '''
        Returns the actions message with font format
        '''
        message = "Action Required: " + self.action
        return self.font2.render(message, True, (0, 0, 0))

    def _render_action(self, canvas):
        '''
        Renders the actions required by the user in the status menu
        '''
        message = self._get_formatted_action_message()
        canvas.blit(message, (self.action_x, self.action_y))

    def _get_formatted_title_message(self):
        '''
        Returns the title message with font format
        '''
        return self.font1.render(self.title, True, (0, 0, 0))

    def _draw_circle(self, x, y, canvas):
        '''
        Draws a circle on the screen. This represents a rounded corner of the menu screen border
        '''
        pygame.draw.circle(canvas, (255, 255, 255), (x, y), self.border_circle_radius)

    def _draw_rectangle(self, x, y, width, height, canvas):
        '''
        Draws a rectangle on the screen. This represents the north/south or east/west border of the menu screen border
        '''
        pygame.draw.rect(canvas, (255, 255, 255), (x, y, width, height))

    def _render_status_menu_border(self, canvas):
        '''
        Renders the status menu border

        The version of pygame that was used to develop this version of battleship does not support rounded corners
        for rectangles. Therefore, to create rounded corners, 4 circles and 2 rectangles need to be rendered on the screen.
        '''
        #draw top left circle of border
        self._draw_circle(self.border_x, self.y, canvas)

        #draw bottom left circle of border
        self._draw_circle(self.border_x, (self.y + self.border_height), canvas)

        #draw top right circle of border
        self._draw_circle((self.border_x + self.border_width), self.y, canvas)

        #draw bottom right circle of border
        self._draw_circle((self.border_x + self.border_width), (self.y + self.border_height), canvas)

        #draw rectangle that represents the north/south border
        x = self.border_x
        y = self.y - self.border_circle_radius
        width = self.border_width
        height = self.border_height + (2 * self.border_circle_radius)
        self._draw_rectangle(x, y, width, height, canvas)

        #draw rectangle that represents the east/west border
        x = self.border_x - self.border_circle_radius
        y = self.y
        width = self.border_width + (2 * self.border_circle_radius)
        height = self.border_height
        self._draw_rectangle(x, y, width, height, canvas)

    def render(self, canvas):
        self._render_status_menu_border(canvas)
        self._render_status(canvas)
        self._render_action(canvas)

    def set_status(self, message):
        '''
        Sets the status message that is displayed in the status menu
        '''
        self.status = message

    def set_action(self, message):
        '''
        Sets the action message that is displayed in the status menu
        '''
        self.action = message

class BoardIdentifier(BaseObject):
    def __init__(self, il, title, width, height, x=0, y= 0):
        BaseObject.__init__(self, il, x=x, y=y)

        self.font = font.Font("Fonts/OpenSans-Light.ttf", 20)

        self.title = title

        self.border_width = width
        self.border_height = height
        self.border_circle_radius = 10

    def _get_formatted_title(self):
        '''
        Returns the status message with font format
        '''
        return self.font.render(self.title, True, (0, 0, 0))

    def _render_title(self, canvas):
        title = self._get_formatted_title()
        canvas.blit(title, (self.x + 5, self.y - 3))

    def _render_border(self, canvas):
        '''
        Renders the status menu border
        '''
        pygame.draw.circle(canvas, (255, 255, 255), (self.x, self.y), self.border_circle_radius)
        pygame.draw.circle(canvas, (255, 255, 255), (self.x, self.y + self.border_height), self.border_circle_radius)
        pygame.draw.circle(canvas, (255, 255, 255), (self.x + self.border_width, self.y), self.border_circle_radius)
        pygame.draw.circle(canvas, (255, 255, 255), (self.x + self.border_width, self.y + self.border_height), self.border_circle_radius)
        pygame.draw.rect(canvas, (255, 255, 255), (self.x, 
                                                   self.y - self.border_circle_radius, 
                                                   self.border_width, 
                                                   self.border_height + (2 * self.border_circle_radius)))
        pygame.draw.rect(canvas, (255, 255, 255), (self.x - self.border_circle_radius, 
                                                   self.y, 
                                                   self.border_width + (2 * self.border_circle_radius), 
                                                   self.border_height + self.border_circle_radius))
        pygame.draw.line(canvas, (0, 0, 0), (self.x - 10, self.y + self.border_height + self.border_circle_radius - 1), 
                                            (self.x + self.border_circle_radius + self.border_width, self.y + self.height + self.border_height + self.border_circle_radius - 1))

    def render(self, canvas):
        self._render_border(canvas)
        self._render_title(canvas)

class BackgroundImage(BaseObject):
    def __init__(self, il, x=0, y=0):
        BaseObject.__init__(self, il, x=x, y=y)

        self.width = 1000
        self.height = 955
        self.background = il.load_image(Images.ImageEnum.TitleBackground)
        self.resized_background = transform.scale(self.background, (self.width, self.height))

    def render(self, canvas):
        canvas.blit(self.resized_background, (self.x, self.y))


class GameSceneManager(BaseObject):
    def __init__(self, IL, OH, x=0, y=0):
        BaseObject.__init__(self, IL, x=x, y=y)

        # this variable will keep track of what phase of the game the player
        # is in.
        self.IL = IL
        self.OH = OH
        self.current_phase = "OPTIONS"
        self.player_board_x = 100
        self.enemy_board_x = 550
        self.board_y = 300
        self.enemy_board_initialized = False

        self.back_end_coords = "0-0"

        self.ai_choice = None
        self.ai = None
        
        self.player_board = BattleshipBoard(self.IL, self.player_board_x, self.board_y)
        self.player_title = BoardIdentifier(self.IL, "Player Board", 128, 25, self.player_board_x + 10, self.board_y - 35)
        self.enemy_board = BattleshipBoard(self.IL, self.enemy_board_x, self.board_y)
        self.enemy_title = BoardIdentifier(self.IL, "Enemy Board", 128, 25, self.enemy_board_x + 10, self.board_y - 35)
        self.player_board.player = True
        self.status_menu = GameScreenStatusMenu(self.IL, 60, 60)

        self.options_menu = OptionsMenu(self.IL, 300, 150)

        self.options_phase_manager = OptionsPhaseHandler(self.IL, self.options_menu, self.status_menu, self)
        self._initialize_options_phase_objects()

        self.placement_phase_manager = PlacementPhaseHandler(self.IL, self.status_menu, self.player_board, self.enemy_board, self)
        # self._initialize_placement_phase_objects()

        #VARIABLES FOR THE PLAYER TURN PHASE
        self.battleship_board_positions = self.enemy_board.boardPositions

        self.dialog_box = Objects.BattleshipBoard.DialogBox(self.IL)

        #Initialize back end boards to track ship positions
        self.player_board.init_back_end_board()
        self.enemy_board.init_back_end_board()

        #avoids bug where the second turn selection automatically pops up a "hit" dialog without confirm
        self.post_confirm = False

        self.shot_result_displayed = False

        self.selected_position = None
        self.hover_position = None

        self.win_sound = SoundEnum.WIN
        self.loss_sound = SoundEnum.LOSS

    def _initialize_options_phase_objects(self):
        self.OH.new_object(self.options_menu)

    def _initialize_placement_phase_objects(self):
        self.OH.new_object(self.player_board)
        self.OH.new_object(self.status_menu)
        self.OH.new_object(self.player_title)
    
    def _initialize_enemy_board(self):
        self.OH.new_object(self.enemy_board)
        self.OH.new_object(self.enemy_title)
        self.enemy_board_initialized = True

    def update(self, oh):
        if self.current_phase == "OPTIONS":
            self.options_phase(oh)
        elif self.current_phase == "PLACEMENT":
            self.placement_phase(oh)
        elif self.current_phase == "PLAYER_TURN":
            self.player_turn_phase(oh)
        elif self.current_phase == "ENEMY_TURN":
            self.enemy_turn_phase(oh)
        elif self.current_phase == "GAME_ENDING":
            self.game_ending_phase(oh)

    def handle_input(self, oh, events, pressed_keys):
        if self.current_phase == "OPTIONS":
            self.options_phase_input(oh, events, pressed_keys)
        elif self.current_phase == "PLACEMENT":
            self.placement_phase_input(oh, events, pressed_keys)
        elif self.current_phase == "PLAYER_TURN":
            self.player_turn_phase_input(oh, events, pressed_keys)
        elif self.current_phase == "ENEMY_TURN":
            self.enemy_turn_phase_input(oh, events, pressed_keys)
        elif self.current_phase == "GAME_ENDING":
            self.game_ending_phase_input(oh, events, pressed_keys)

    def options_phase(self, oh):
        self.options_phase_manager = OptionsPhaseHandler(self.IL, self.options_menu, self.status_menu, self)
        self._initialize_options_phase_objects()
        self.options_phase_manager.update(oh)
        # self.current_phase = "PLACEMENT"  # just skipping this phase for now

    def placement_phase(self, oh):
        # self.placement_phase_manager = PlacementPhaseHandler(self.IL, self.status_menu, self.player_board, self.enemy_board, self)
        self._initialize_placement_phase_objects()
        self.placement_phase_manager.update(oh)

    def player_turn_phase(self, oh):
        if (self.enemy_board_initialized == False):
            self._initialize_enemy_board()

    def enemy_turn_phase(self, oh):
        pass

    def game_ending_phase(self, oh):
        pass

    def options_phase_input(self, oh, events, pressed_keys):
        self.options_phase_manager.handle_input(oh, events, pressed_keys)

    def placement_phase_input(self, oh, events, pressed_keys):
        self.placement_phase_manager.handle_input(oh, events, pressed_keys)

    def player_turn_phase_input(self, oh, events, pressed_keys):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and self.shot_result_displayed is True:
                self.enemy_board.clear_board(oh, self.dialog_box)
                self.shot_result_displayed = False
            elif event.type == pygame.MOUSEBUTTONDOWN and self.selected_position is None:
                self.dialog_box.init_confirm_deny_buttons()
                if event.button == 1:
                    mouseX, mouseY = pygame.mouse.get_pos()
                    for i in range(10):
                        for j in range(10):
                            if self.battleship_board_positions[i][j].collidepoint(mouseX - self.enemy_board.x, mouseY - self.enemy_board.y):
                                self.enemy_board.clear_board(oh, None)
                                self.selected_position = self.battleship_board_positions[i][j]
                                if self.dialog_box not in oh.objects:
                                    oh.new_object(self.dialog_box)
                                else:
                                    oh.remove_object(self.dialog_box)
                                    oh.new_object(self.dialog_box)
                                self.dialog_box.x = mouseX
                                self.dialog_box.y = mouseY

            elif event.type == pygame.MOUSEBUTTONDOWN and self.selected_position:
                mouseX, mouseY = pygame.mouse.get_pos()

                board_position_x = int(self.selected_position.y / 40)
                board_position_y = int(self.selected_position.x / 40)
#                   
#                    I'm subtracting 1 in the get_coordinates function so this isn't needed
#                    if (board_position_x == 10):
#                        board_position_x -= 1
#                    
#                    if (board_position_y == 10):
#                        board_position_y -= 1

                back_end_coords = self.player_board.get_coordinates(board_position_x, board_position_y)
                print(self.back_end_coords)
               
                if self.dialog_box.confirm_deny_buttons[0].collidepoint(mouseX - self.dialog_box.x, mouseY - self.dialog_box.y):
                    self.shot_result_displayed = True
                    check_hit_return = self.enemy_board.check_hit(back_end_coords, self.IL, self.OH, self)
                    self.selected_position = None
                    #self.enemy_board.determine_selection_result(self.IL, self.OH)
                    if (check_hit_return is not None):
                        self._change_to_enemy_phase()
                    self.enemy_board.clear_board(oh, self.dialog_box)

                elif self.dialog_box.confirm_deny_buttons[1].collidepoint(mouseX - self.dialog_box.x, mouseY - self.dialog_box.y):
                    self.selected_position = None
                    self.enemy_board.clear_board(oh, self.dialog_box)

            elif event.type == pygame.MOUSEMOTION and self.selected_position is None and self.shot_result_displayed is False:
                mouseX, mouseY = pygame.mouse.get_pos()
                if ((mouseX > 550 and mouseX <= 950) and (mouseY > 300 and mouseY <= 700)):
                    mouse_pos_x = mouseX - self.enemy_board.x
                    mouse_pos_y = mouseY - self.enemy_board.y

                    board_position_x = int(mouse_pos_x / 40)
                    board_position_y = int(mouse_pos_y / 40)

                    if (board_position_x == 10):
                        board_position_x -= 1
                    
                    if (board_position_y == 10):
                        board_position_y -= 1

                    self.enemy_board.set_square_selection(board_position_x, board_position_y)

                    if self.hover_position:
                        self.enemy_board.clear_board(oh, None)
                    self.hover_position = self.battleship_board_positions[board_position_x][board_position_y]
                    self.enemy_board.hoverHighlight(self.hover_position)

    def enemy_turn_phase_input(self, oh, events, pressed_keys):

        coords = self.ai.get_next_guess()
        self.player_board.set_square_selection(int(coords[2]), int(coords[0]))
        result = self.player_board.check_hit(coords, self.IL, self.OH, self)
        if result is True:
            if isinstance(result, str):
                self.ai.record_result("HIT", result)
            else:
                self.ai.record_result("HIT")
        else:
            self.ai.record_result("MISS")
        # self.player_board.determine_selection_result(self.IL, self.OH)
        if self.current_phase != "GAME_ENDING":
            self.change_to_player_phase()

    def game_ending_phase_input(self, oh, events, pressed_keys):
        pass

    def change_to_placement_phase(self, ai_choice):
        self.current_phase = "PLACEMENT"
        self.status_menu.set_status("Placement, AI = " + ai_choice)
        self.status_menu.set_action("Please place your ships on the player gameboard.")
        self.ai_choice = ai_choice
        self.ai = Objects.BattleshipAI.BattleshipControllerAI(10, 10, self.ai_choice)
        ship_arrays, ship_names = self.ai.place_ships()
        print(ship_names, ship_arrays)
        for ship in range(0, len(ship_names)):
            print(ship)
            self.enemy_board.add_ship(ship_names[ship], ship_arrays[ship])

    def change_to_player_phase(self):
        '''
        Change phase to player turn
        '''
        # self.player_board.deactivate_board()
        # self.enemy_board.activate_board()
        self.current_phase = "PLAYER_TURN"
        self.status_menu.set_status("Player Turn, AI = " + self.ai_choice)
        self.status_menu.set_action("Please make a selection on the Enemy board")

    def _change_to_enemy_phase(self):
        '''
        Change phase to enemey turn
        '''
        # self.player_board.deactivate_board()
        # self.enemy_board.deactivate_board()
        self.current_phase = "ENEMY_TURN"
        self.status_menu.set_status("Enemy Turn")
        self.status_menu.set_action("Please wait. The enemy is making a selection.")

    def change_to_game_ending_phase(self, outcome, oh):

        self.current_phase = "GAME_ENDING"
        if outcome == 0:
            oh.sound_loader.play_sound(self.loss_sound)
        elif outcome == 1:
            oh.sound_loader.play_sound(self.win_sound)


class OptionsMenu(BaseObject):
    def __init__(self, il, x=0, y=0):
        BaseObject.__init__(self, il, x=x, y=y)

        self.xPosition = x
        self.yPosition = y

        self.font = font.Font("Fonts/OpenSans-Light.ttf", 40)
        self.prompts_with_choices = [["Choose your difficulty", "EASY", "HARD"]]

        self.image = pygame.Surface([500, 500], pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()

        self.choiceRects = [] 
        self.confirm_buttons = []

        self.ai_choice = None

        self._init_prompts_with_choices()
        self._init_confirm_dialog()

    def _init_prompts_with_choices(self):
        self.x = 0
        self.y = 0
        for prompt in self.prompts_with_choices:
            innerArray = []
            innerArray.append(prompt[0])
            self.image.blit(self.font.render(prompt[0], True, (255,255,255)), (self.x, self.y))
            self.y += 100
            for i in range (1, len(prompt)):
                choiceRender = self.font.render(prompt[i], True, (255,255,255))
                innerArray.append((self.image.blit(choiceRender, (self.x, self.y)), prompt[i]))
                self.x += 300 
            self.y += 100
            self.choiceRects.append(innerArray)

    def _init_confirm_dialog(self):
        self.x = 50 
        confirm = self.font.render("Confirm", True, (255,255,255))
        self.confirm_buttons.append((self.image.blit(confirm, (self.x, self.y)), confirm))
        self.x += 180 
        deny = self.font.render("Discard", True, (255,255,255))
        self.confirm_buttons.append((self.image.blit(deny, (self.x, self.y)), deny))
    
    def render_choice(self, rectTuple):
        s = pygame.Surface((400,100))
        s.set_alpha(255)
        self.image.blit(s, (0,0,))
        self.image.blit(self.font.render("Selected: " + rectTuple[1], True, (0,120,0)), (0,0))

    def render(self, canvas):
        self.x = self.xPosition
        self.y = self.yPosition
        canvas.blit(self.image, (self.x, self.y))
        pass


class OptionsPhaseHandler:
    def __init__(self, il, options_menu, status_menu, phase_manager):
        self.options_menu = options_menu
        self.status_menu = status_menu
        self.phase_manager = phase_manager

        self.choiceSelected = None

        self.choiceRects = self.options_menu.choiceRects
        self.confirm_buttons = self.options_menu.confirm_buttons
    
    def update(self, oh):
        self.status_menu.set_status("Options")
        self.status_menu.set_action("Choose your game options")

    def handle_input(self, oh, events, pressed_keys):
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                mouseX, mouseY = pygame.mouse.get_pos()
                for group in self.choiceRects:
                    if group[1][0].collidepoint(mouseX - self.options_menu.x, mouseY - self.options_menu.y):
                        pass
                    if group[2][0].collidepoint(mouseX - self.options_menu.x, mouseY - self.options_menu.y):
                        pass
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouseX, mouseY = pygame.mouse.get_pos()
                    for group in self.choiceRects:
                        if group[1][0].collidepoint(mouseX - self.options_menu.x, mouseY - self.options_menu.y):
                            self.choiceSelected = group[1]
                            self.options_menu.render_choice(self.choiceSelected)
                            self.options_menu.ai_choice = group[1][1]
                        if group[2][0].collidepoint(mouseX - self.options_menu.x, mouseY - self.options_menu.y):
                            self.choiceSelected = group[2]
                            self.options_menu.render_choice(self.choiceSelected)
                            self.options_menu.ai_choice = group[2][1]
                    if self.confirm_buttons[0][0].collidepoint(mouseX - self.options_menu.x, mouseY - self.options_menu.y) and self.options_menu.ai_choice is None:
                        pass
                    elif self.confirm_buttons[0][0].collidepoint(mouseX - self.options_menu.x, mouseY - self.options_menu.y):
                        self.clean_up_options_phase(oh)
                        self.phase_manager.change_to_placement_phase(self.options_menu.ai_choice)
                    elif self.confirm_buttons[1][0].collidepoint(mouseX - self.options_menu.x, mouseY - self.options_menu.y):
                        self.options_menu.ai_choice = 'EASY'
                        self.choiceSelected = None

    def clean_up_options_phase(self, oh):
        oh.remove_object(self.phase_manager.options_menu)


class PlacementPhaseHandler:

    def __init__(self, il, status_menu, player_board, enemy_board, phase_manager):
        self.player_board = player_board
        self.enemy_board = enemy_board
        self.status_menu = status_menu
        self.phase_manager = phase_manager

        self.incorrect_placement_sound = SoundEnum.INCORRECTPLACEMENT
        self.button_press_sound = SoundEnum.CLICK

        self.ships_added = False
        self.available_ships = [Objects.ShipObjects.BaseShip(il, "Carrier"),
                                Objects.ShipObjects.BaseShip(il, "Battleship"),
                                Objects.ShipObjects.BaseShip(il, "Cruiser"),
                                Objects.ShipObjects.BaseShip(il, "Submarine"),
                                Objects.ShipObjects.BaseShip(il, "Destroyer")]
        self.ships_placed = []

        self.selected_ship = None

        self.available_ships_text = AvailableShipsText(il)
        self.start_game_text = StartBattleText(il)
        self.text_placed = False

        # self.ship_lot_start_x = self.player_board.x + (
        #             self.player_board.width / 2)
        # self.ship_lot_start_y = self.player_board.y + self.player_board.height + 125

        self.ship_lot_start_x = self.player_board.x + self.get_board_width() + 200
        self.ship_lot_start_y = self.player_board.y + 125

        self.ship_lot_x_offset = 20

        self.error_display_timer_maximum = 64
        self.error_display_timer_current = self.error_display_timer_maximum
        self.epm = ErrorPlacingMessage(il)

        self.error_NASP_display_timer_maximum = 64
        self.error_NASP_display_timer_current = self.error_NASP_display_timer_maximum
        self.NASP = ErrorNotAllShipsPlaced(il)

        self.psm = PlacementSaveManager(il, self, x=200, y=700)

        self.resize_ships()

    def check_timers(self, oh):

        if self.error_display_timer_current < self.error_display_timer_maximum:
            if self.error_display_timer_current == 0:
                oh.new_object(self.epm)
            self.error_display_timer_current += 1

            if self.error_display_timer_current == self.error_display_timer_maximum:
                oh.remove_object(self.epm)

        if self.error_NASP_display_timer_current < self.error_NASP_display_timer_maximum:
            if self.error_NASP_display_timer_current == 0:
                oh.new_object(self.NASP)
            self.error_NASP_display_timer_current += 1

            if self.error_NASP_display_timer_current == self.error_NASP_display_timer_maximum:
                oh.remove_object(self.NASP)

    def check_ships_placed(self, oh):

        placed_x_offset = 0
        if not self.ships_added:
            total_width_of_lot = 0
            for ship in self.available_ships:
                total_width_of_lot += ship.width + self.ship_lot_x_offset
            total_width_of_lot -= self.available_ships[0].width
            self.ship_lot_start_x -= (total_width_of_lot / 4)
            for ship in self.available_ships:
                ship.x = self.ship_lot_start_x + placed_x_offset
                ship.y = self.ship_lot_start_y
                ship.change_directional_state("VERTICAL_DOWN")
                placed_x_offset += ship.width + self.ship_lot_x_offset
                oh.new_object(ship)
            self.ships_added = True

            self.check_text_placed(oh, placed_x_offset)

    def check_text_placed(self, oh, placed_x_offset):

        if not self.text_placed:
            middle_x = self.ship_lot_start_x + (placed_x_offset / 2)
            above_y = self.ship_lot_start_y - self.available_ships_text.height - 10

            self.available_ships_text.x = middle_x - (
                        self.available_ships_text.width / 2)
            self.available_ships_text.y = above_y

            oh.new_object(self.available_ships_text)

            board_1_right_x = self.player_board.x + self.player_board.width
            board_2_left_x = self.enemy_board.x

            self.start_game_text.x = self.ship_lot_start_x

            self.start_game_text.y = self.ship_lot_start_y + 225

            oh.new_object(self.start_game_text)
            oh.new_object(self.psm)

            self.text_placed = True

    def update(self, oh):
        # self.player_board.activate_board()
        # self.enemy_board.deactivate_board()
        # self.status_menu.set_status("Placement")
        # self.status_menu.set_action("Please place your ships on the player gameboard")

        self.check_timers(oh)
        self.check_ships_placed(oh)

        if self.selected_ship:
            self.selected_ship.selected = True
            self.snap_ship_to_grid(pygame.mouse.get_pos()[0],
                                   pygame.mouse.get_pos()[1])

    def handle_input(self, oh, events, pressed_keys):

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.selected_ship:
                        if self.check_placement():
                            self.place_ship()
                            self.selected_ship.selected = False
                            self.selected_ship = None
                            if self.error_display_timer_current < self.error_display_timer_maximum:
                                self.error_display_timer_current = self.error_display_timer_maximum
                                oh.remove_object(self.epm)
                        else:
                            self.display_not_possible(self.selected_ship.x, self.selected_ship.y, oh)
                    else:
                        mouse_pos = event.pos
                        for ship in self.available_ships:
                            if ship.x < mouse_pos[0] < ship.x + ship.width:
                                if ship.y < mouse_pos[1] < ship.y +\
                                        ship.height:
                                    self.selected_ship = ship
                elif event.button == 3:
                    if self.selected_ship:
                        self.selected_ship.rotate_ship_90()

                if event.button == 1:
                    if self.start_game_text.hovered:
                        oh.sound_loader.play_sound(
                            self.button_press_sound)
                        if len(self.ships_placed) == len(self.available_ships):
                            self.clean_up_placement_phase(oh)
                            self.phase_manager.change_to_player_phase()
                        else:
                            self.display_not_all_ships_placed(oh)

    def clean_up_placement_phase(self, oh):

        oh.remove_object(self.start_game_text)
        self.start_game_text = None

        oh.remove_object(self.available_ships_text)
        self.available_ships_text = None

        if self.error_NASP_display_timer_current < self.error_NASP_display_timer_maximum:
            oh.remove_object(self.NASP)
        if self.error_display_timer_current < self.error_display_timer_maximum:
            oh.remove_object(self.epm)

        oh.remove_object(self.psm)

        self.put_ships_in_board()

    def get_size_of_rects(self):
        # currently just a placeholder function return until there is an
        # outward facing function/variable from the boards.
        return 40, 40

    def get_offset_size(self):
        # currently just a placeholder function return until there is an
        # outward facing function/variable from the boards.
        return 35, 35

    def resize_ships(self):

        new_x, new_y = self.get_size_of_rects()
        offset_size = self.get_size_of_rects()[0] - self.get_offset_size()[0]

        for ship in self.available_ships:
            ship.scale_ship(new_x, new_y, offset_size)

    def snap_ship_to_grid(self, mouse_x, mouse_y):

        left_side_of_board = self.player_board.x
        y_of_board = self.player_board.y
        snapped_x = left_side_of_board
        snapped_y = y_of_board
        x_box_size, y_box_size = self.get_size_of_rects()

        mouse_pos_x = mouse_x - self.player_board.x
        mouse_pos_y = mouse_y - self.player_board.y

        min_right = self.get_board_width() + self.player_board.x
        min_down = self.get_board_height() + self.player_board.y

        max_left = self.player_board.x
        max_up = self.player_board.y

        if self.selected_ship.directional_state == "HORIZONTAL_RIGHT":
            min_right = min_right - self.selected_ship.width - (self.get_size_of_rects()[0] - self.get_offset_size()[0])
            min_down -= self.get_size_of_rects()[1]
        elif self.selected_ship.directional_state == "HORIZONTAL_LEFT":
            min_right -= self.get_size_of_rects()[0]
            min_down -= self.get_size_of_rects()[1]
            max_left += (self.selected_ship.width - self.get_size_of_rects()[0])+(self.get_size_of_rects()[0] - self.get_offset_size()[0])
        elif self.selected_ship.directional_state == "VERTICAL_DOWN":
            min_down -= self.selected_ship.height+(self.get_size_of_rects()[1] - self.get_offset_size()[1])
            min_right -= self.get_size_of_rects()[0]
        elif self.selected_ship.directional_state == "VERTICAL_UP":
            min_right -= self.get_size_of_rects()[0]
            min_down -= self.get_size_of_rects()[1]
            max_up += (self.selected_ship.height - self.get_size_of_rects()[1])+(self.get_size_of_rects()[1] - self.get_offset_size()[1])

        board_position_x = min((mouse_pos_x // x_box_size) * x_box_size + left_side_of_board,
                               min_right)
        board_position_y = min((mouse_pos_y // y_box_size) * y_box_size + y_of_board,
                               min_down)

        board_position_x = max(max_left, board_position_x)
        board_position_y = max(max_up, board_position_y)

        snapped_y = board_position_y
        snapped_x = board_position_x

        if self.selected_ship.directional_state == "HORIZONTAL_LEFT":
            snapped_x += self.get_offset_size()[0]
        elif self.selected_ship.directional_state == "VERTICAL_UP":
            snapped_y += self.get_offset_size()[1]
        self.selected_ship.selected_x = snapped_x
        self.selected_ship.selected_y = snapped_y

    def check_placement(self):

        allowed = True

        for ship in self.ships_placed:
            if ship == self.selected_ship:
                continue
            else:
                if ship.x - self.selected_ship.width <= self.selected_ship.x <= ship.x + ship.width:
                    if ship.y - self.selected_ship.height <= self.selected_ship.y <= ship.y + ship.height:
                        allowed = False

        return allowed

    def display_not_possible(self, x, y, oh):

        self.epm.x = x - self.epm.width
        self.epm.y = y - self.epm.height

        self.error_display_timer_current = 0

        oh.sound_loader.play_sound(self.incorrect_placement_sound)

    def display_not_all_ships_placed(self, oh):

        self.NASP.x = (self.start_game_text.x + self.start_game_text.width/2) - (self.NASP.width/2)
        self.NASP.y = self.start_game_text.y + self.start_game_text.height + 50

        self.error_NASP_display_timer_current = 0

        oh.sound_loader.play_sound(self.incorrect_placement_sound)

    def place_ship(self):
        if self.selected_ship not in self.ships_placed:
            self.ships_placed.append(self.selected_ship)

    def get_board_width(self):

        return self.get_number_of_squares()[0] * self.get_size_of_rects()[0]

    def get_board_height(self):

        return self.get_number_of_squares()[1] * self.get_size_of_rects()[1]

    def get_number_of_squares(self):

        return 10, 10

    def put_ships_in_board(self):

        for ship in self.ships_placed:
            ship_array = self.get_ship_array(ship)
            self.player_board.add_ship(ship.name, ship_array)

    def get_ship_array(self, ship):
        ship_array = []
        starting_x_square = (ship.selected_x - self.player_board.x) // 40
        starting_y_square = (ship.selected_y - self.player_board.y) // 40
        for x in range(0, ship.size):
            if ship.directional_state == "HORIZONTAL_RIGHT":
                ship_array.append(
                    str(starting_x_square + x) + "-" + str(starting_y_square))
            elif ship.directional_state == "HORIZONTAL_LEFT":
                ship_array.append(
                    str(starting_x_square - x) + "-" + str(starting_y_square))
            elif ship.directional_state == "VERTICAL_DOWN":
                ship_array.append(
                    str(starting_x_square) + "-" + str(starting_y_square+x))
            elif ship.directional_state == "VERTICAL_UP":
                ship_array.append(
                    str(starting_x_square) + "-" + str(starting_y_square-x))
        return ship_array

    def get_ship_placement_save_info(self):
        output_data = []

        directional_dict = {"HORIZONTAL_RIGHT": "0",
                            "VERTICAL_DOWN": "1",
                            "HORIZONTAL_LEFT": "2",
                            "VERTICAL_UP": "3"}
        for ship in self.ships_placed:
            starting_x_square = (ship.selected_x - self.player_board.x) // 40
            starting_y_square = (ship.selected_y - self.player_board.y) // 40
            """
            if ship.directional_state == "HORIZONTAL_LEFT":
                if starting_x_square > 0:
                    starting_x_square += 1
            elif ship.directional_state == "VERTICAL_UP":
                if starting_y_square > 0:
                    starting_y_square += 1
            """
            output_data.append((directional_dict[ship.directional_state] +
                                ":" + str(starting_x_square) + ":" +
                                str(starting_y_square)))

        return output_data

    def place_ships_from_save(self, ship_info):

        directional_dict = {"0": "HORIZONTAL_RIGHT",
                            "1": "VERTICAL_DOWN",
                            "2": "HORIZONTAL_LEFT",
                            "3": "VERTICAL_UP"}

        for x in range(len(self.available_ships)):
            specific_ship_info = ship_info[x].split(":")
            self.available_ships[x].change_directional_state(directional_dict[
                specific_ship_info[0]])
            self.available_ships[x].selected_x = int(
                specific_ship_info[1]) * 40 + self.player_board.x
            if self.available_ships[x].directional_state == "HORIZONTAL_LEFT":
                self.available_ships[x].selected_x += self.get_offset_size()[0]
            self.available_ships[x].selected_y = int(
                specific_ship_info[2]) * 40 + self.player_board.y
            if self.available_ships[x].directional_state == "VERTICAL_UP":
                self.available_ships[x].selected_y += self.get_offset_size()[1]
            self.available_ships[x].change_base_coords()
            if self.available_ships[x] not in self.ships_placed:
                self.ships_placed.append(self.available_ships[x])

        self.selected_ship = None


class AvailableShipsText(BaseObject):

    def __init__(self, il, x=0, y=0):
        BaseObject.__init__(self, il, x=x, y=y)

        self.image = il.load_image(Images.ImageEnum.AVAILABLESHIPS)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def scale_images(self, factor_x, factor_y):
        self.image = transform.scale(self.image, (self.width*factor_x,
                                                  self.height*factor_y))
        self.width = self.image.get_width()
        self.height = self.image.get_height()


class StartBattleText(BaseObject):

    def __init__(self, il, x=0, y=200):
        BaseObject.__init__(self, il, x=x, y=y)

        self.image_normal = il.load_image(Images.ImageEnum.STARTBATTLE)
        self.image_hovered = il.load_image(Images.ImageEnum.STARTBATTLEHOVERED)
        self.width = self.image_normal.get_width()
        self.height = self.image_normal.get_height()

        self.hovered = False
        self.image = self.image_normal

    def scale_images(self, factor_x, factor_y):
        self.image_normal = transform.scale(self.image_normal,
                                            (self.width * factor_x,
                                             self.height * factor_y))
        self.image_hovered = transform.scale(self.image_hovered,
                                             (self.width * factor_x,
                                              self.height * factor_y))
        self.width = self.image_normal.get_width()
        self.height = self.image_normal.get_height()

    def update(self, oh):

        mouse_pos = pygame.mouse.get_pos()
        self.hovered = False
        if self.x <= mouse_pos[0] <= self.x + self.width:
            if self.y <= mouse_pos[1] <= self.y + self.height:
                self.hovered = True

        if self.hovered:
            self.image = self.image_hovered
        else:
            self.image = self.image_normal


class ErrorPlacingMessage(BaseObject):

    def __init__(self, il, x=0, y=0):
        BaseObject.__init__(self, il, x=x, y=y)

        self.image = il.load_image(Images.ImageEnum.INCORRECTPLACEMENT)
        self.width = self.image.get_width()
        self.height = self.image.get_height()


class ErrorNotAllShipsPlaced(BaseObject):

    def __init__(self, il, x=0, y=0):

        BaseObject.__init__(self, il, x=x, y=y)
        self.image = il.load_image(Images.ImageEnum.NOTALLSHIPSPLACED)
        self.width = self.image.get_width()
        self.height = self.image.get_height()


class PlacementSaveManager(BaseObject):

    def __init__(self, il, placement_phase_manager, x=0, y=0):
        BaseObject.__init__(self, il, x=x, y=y)

        # only 5 slots of saves
        self.saves = [[], [], [], [], []]

        self.image = il.load_image(Images.ImageEnum.SAVEDPLACEMENTS)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.save_file = "saves/placement_saves.ps"
        self.save_folder = "saves"

        self.check_save_file_exists()
        self.load_saves()

        self.font = font.Font("Fonts/OpenSans-Light.ttf", 20)

        self.placement_phase_manager = placement_phase_manager

    def load_saves(self):

        open_file = open(self.save_file, "r")
        file_content = open_file.read()
        saved_content = file_content.split("\n")

        for x in range(len(saved_content)):
            save_split = saved_content[x].split(" ")
            if len(save_split) > 6:
                date_created = save_split[0]
                time_created = save_split[1]
                carrier_placement = save_split[2]
                battleship_placement = save_split[3]
                cruiser_placement = save_split[4]
                submarine_placement = save_split[5]
                destroyer_placement = save_split[6]

                self.saves[x] = [date_created, time_created, carrier_placement,
                                 battleship_placement, cruiser_placement,
                                 submarine_placement, destroyer_placement]


    def new_save(self, save_data, slot):

        open_file = open(self.save_file, "w+")
        open_file.truncate(0)

        self.saves[slot] = save_data

        for save in self.saves:
            for info in save:
                open_file.write(info + " ")
            open_file.write("\n")

    def check_save_file_exists(self):

        if not path.exists(self.save_file):
            if not path.exists(self.save_folder):
                try:
                    mkdir(self.save_folder)
                except OSError:
                    return False
            open_file = open(self.save_file, "w")
            open_file.close()

    def create_new_save_data(self, ship_placements, slot):
        if len(ship_placements) == 5:
            time_info = datetime.now()
            date = str(time_info.day) + str(time_info.month) + str(time_info.year)
            time = str(time_info.hour) + str(time_info.minute)
            save_data = [date, time, ship_placements[0], ship_placements[1],
                         ship_placements[2], ship_placements[3],
                         ship_placements[4]]

            self.new_save(save_data, slot)

    def initiate_load(self, slot):
        if len(self.saves[slot]) > 0:
            save_data = list()
            save_data.append(self.saves[slot][2])
            save_data.append(self.saves[slot][3])
            save_data.append(self.saves[slot][4])
            save_data.append(self.saves[slot][5])
            save_data.append(self.saves[slot][6])
            self.placement_phase_manager.place_ships_from_save(save_data)

    def draw_save_slots(self, canvas):

        save_strings = list()
        for save in self.saves:
            if len(save) == 0:
                continue
            apparent_string = save[0] + " " + save[1]
            save_strings.append(self.font.render(apparent_string,
                                                 True, (0, 0, 184)))

        y_offset = 27
        x_offset = 7
        for save in save_strings:
            pygame.draw.rect(canvas, (94, 197, 255), pygame.Rect(self.x + x_offset, self.y + y_offset + 3, 198, 40))
            canvas.blit(save, (self.x + x_offset, self.y + y_offset + 5))
            y_offset += 42

    def render(self, canvas):
        canvas.blit(self.image, (self.x, self.y))

        self.draw_save_slots(canvas)

    def handle_input(self, oh, events, pressed_keys):

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # left click pressed

                    mouse_pos = event.pos
                    if self.x <= mouse_pos[0] <= self.x+self.width:
                        if self.y <= mouse_pos[1] <= self.y+self.height:
                            save_clicked = False
                            ship_placements = []
                            # mouse clicked within the object
                            if self.x + 208 <= mouse_pos[0] <= self.x + 238:
                                save_clicked = True
                                ship_placements = self.placement_phase_manager.get_ship_placement_save_info()

                            # slot one
                            if mouse_pos[1] <= self.y + 68:
                                if save_clicked:
                                    self.create_new_save_data(
                                        ship_placements, 0)
                                else:
                                    self.initiate_load(0)
                            # slot two
                            elif mouse_pos[1] <= self.y + 111:
                                if save_clicked:
                                    self.create_new_save_data(
                                        ship_placements, 1)
                                else:
                                    self.initiate_load(1)
                            # slot three
                            elif mouse_pos[1] <= self.y + 154:
                                if save_clicked:
                                    self.create_new_save_data(
                                        ship_placements, 2)
                                else:
                                    self.initiate_load(2)
                            # slot four
                            elif mouse_pos[1] <= self.y + 197:
                                if save_clicked:
                                    self.create_new_save_data(
                                        ship_placements, 3)
                                else:
                                    self.initiate_load(3)
                            # slot five
                            else:
                                if save_clicked:
                                    self.create_new_save_data(
                                        ship_placements, 4)
                                else:
                                    self.initiate_load(4)

                                    
class ToMainScreen(BaseObject):
    """
    Returns users to the main screen
    Author: Alex Wilson
    """

    def __init__(self, il, x=700, y=3):
        BaseObject.__init__(self, il, x=x, y=y)

        self.click_num = 0
        self.font = pygame.font.Font("Fonts/OpenSans-Light.ttf", 30)
        self.quit_game = self.font.render("Quit Game", True, (255, 255, 255))
        self.quit_game_hover = self.font.render("Quit Game", True, (166, 31, 36))
        self.quit_game_pressed = self.font.render("Click again to confirm", True, (255, 255, 255))
        self.quit_game_pressed_hover = self.font.render("Click again to confirm", True, (166, 31, 36))

    def update(self, oh):
        """
        Changes color of Quit Game message from white to red with hover
        """
        location = pygame.mouse.get_pos()
        quit_coord = 703 < location[0] < 845 and 13 < location[1] < 41
        confirm_coord = 700 < location[0] < 989 and 12 < location[1] < 38
        # if user hovers over quit game, color is changed from white to red
        if quit_coord and self.click_num == 0:
            self.quit_game = self.quit_game_hover
        # if users cursor anywhere else on board, quit message is white
        elif self.click_num == 0:
            self.quit_game = self.font.render("Quit Game", True, (255, 255, 255))
        # if user hovers over confirm quit, color is changed from white to red
        elif confirm_coord and self.click_num == 1:
            self.quit_game = self.quit_game = self.quit_game_pressed_hover
        # if user is not hovering over confirm quit, color is white
        elif self.click_num == 1:
            self.quit_game = self.quit_game = self.quit_game_pressed

    def handle_input(self, oh, events, pressed_keys):
        """
        Returns user to home screen if user clicks quit game message. 1st click prompts confirm, 2nd returns user to
        menu scene.
        """
        location = pygame.mouse.get_pos()
        quit_coord = 703 < location[0] < 845 and 13 < location[1] < 41
        confirm_coord = 700 < location[0] < 989 and 12 < location[1] < 38
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # if user clicks quit game, they are prompted with a confirm quit message
                if quit_coord and self.click_num == 0:
                    self.click_num += 1
                    self.quit_game = self.quit_game_pressed
                # if the user clicks to confirm quit, true is returned and they are returned to menu screen
                elif confirm_coord and self.click_num == 1:
                    return True
                else:
                    self.quit_game = self.font.render("Quit Game", True, (255, 255, 255))
                    self.click_num = 0

    def render(self, canvas):
        canvas.blit(self.quit_game, (self.x, self.y))
