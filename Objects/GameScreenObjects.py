from Bases.BaseObjects import BaseObject
from Tools import Images
from pygame import transform, font
import Objects.ShipObjects
import pygame.mouse


class BackgroundImage(BaseObject):
    def __init__(self, il, x=0, y=0):
        BaseObject.__init__(self, il, x=x, y=y)

        self.width = 1000
        self.height = 955
        self.background = il.load_image(Images.ImageEnum.TitleBackground)
        self.resized_background = transform.scale(self.background, (self.width, self.height))

    def render(self, canvas):
        canvas.blit(self.resized_background, (self.x, self.y))

class GameScreenMessage(BaseObject):

    def __init__(self, il, x=300, y= 120):
        BaseObject.__init__(self, il, x=x, y=y)

        self.font = font.Font("Fonts/freesansbold.ttf", 25)
        self.game_message = self.font.render("This is the Game Screen", True, (255, 255, 255))

    def render(self, canvas):
        canvas.blit(self.game_message, (self.x, self.y))

class GameScreenStatusMenu(BaseObject):
    '''
    Author: Daniel Brezavar
    Description: Displays game status and actions required for the user
    '''

    def __init__(self, il, x=45, y=45):
        BaseObject.__init__(self, il, x=x, y=y)

        self.font1 = font.Font("Fonts/freesansbold.ttf", 25)
        self.font2 = font.Font("Fonts/freesansbold.ttf", 20)

        self.rect_width = 900
        self.rect_height = 110

        self.title = "Status Menu"
        self.title_x = 55
        self.title_y = 55

        self.status = ""
        self.status_x = 80
        self.status_y = 90

        self.action = ""
        self.action_x = 80
        self.action_y = 120

        self.line_x1 = 55
        self.line_x2 = 214
        self.line_y = 80

    def _get_formatted_status_message(self):
        '''
        Returns the status message with font format
        '''
        message = "Status: " + self.status
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

    def _render_title(self, canvas):
        '''
        Renders the status menu title
        '''
        message = self._get_formatted_title_message()
        canvas.blit(message, (self.title_x, self.title_y))

    def _render_title_underscore(self, canvas):
        '''
        Renders the underscore for the status menu title
        '''
        pygame.draw.line(canvas, (0, 0, 0), (self.line_x1, self.line_y), (self.line_x2, self.line_y))

    def _render_status_menu_border(self, canvas):
        '''
        Renders the status menu border
        '''
        pygame.draw.rect(canvas, (255, 255, 255, .5), pygame.Rect(self.x, self.y, self.rect_width, self.rect_height))

    def render(self, canvas):
        self._render_status_menu_border(canvas)
        self._render_title(canvas)
        self._render_title_underscore(canvas)
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

class GameSceneManager(BaseObject):
    '''
    Author: Joshua Shequin, Daniel Brezavar
    Description: Controls the game scene including ship placement, turn management, and determines winner
    '''
    def __init__(self, il, status_menu, player_board, enemy_board, x=0, y=0):
        BaseObject.__init__(self, il, x=x, y=y)

        # this variable will keep track of what phase of the game the player
        # is in.
        self.current_phase = "OPTIONS"
        self.status_menu = status_menu
        self.player_board = player_board
        self.enemy_board = enemy_board

        # VARIABLES FOR THE OPTIONS PHASE

        # -------------------------------

        # VARIABLE FOR THE PLACEMENT PHASE

        self.ships_added = False
        self.available_ships = [Objects.ShipObjects.Carrier(il),
                                Objects.ShipObjects.Battleship(il),
                                Objects.ShipObjects.Cruiser(il),
                                Objects.ShipObjects.Submarine(il),
                                Objects.ShipObjects.Destroyer(il)]
        self.ships_placed = []

        self.selected_ship = None

        self.available_ships_text = AvailableShipsText(il)
        self.start_game_text = StartBattleText(il)
        self.text_placed = False

        self.ship_lot_start_x = self.player_board.x + (self.player_board.width/2)
        self.ship_lot_start_y = self.player_board.y + self.player_board.height + 125
        self.ship_lot_x_offset = 20

        # --------------------------------

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
        self.current_phase = "PLACEMENT"  # just skipping this phase for now

    def placement_phase(self, oh):
        # self.player_board.activate_board()
        # self.enemy_board.deactivate_board()
        self.status_menu.set_status("Placement Phase")
        self.status_menu.set_action("Please place your ships on the gameboard")

        placed_x_offset = 0
        if not self.ships_added:
            total_width_of_lot = 0
            for ship in self.available_ships:
                total_width_of_lot += ship.width + self.ship_lot_x_offset
            total_width_of_lot -= self.available_ships[0].width
            self.ship_lot_start_x -= (total_width_of_lot/4)
            for ship in self.available_ships:
                ship.x = self.ship_lot_start_x + placed_x_offset
                ship.y = self.ship_lot_start_y
                ship.change_directional_state("VERTICAL_DOWN")
                placed_x_offset += ship.width + self.ship_lot_x_offset
                oh.new_object(ship)
            self.ships_added = True

        if not self.text_placed:
            middle_x = self.ship_lot_start_x + (placed_x_offset/2)
            above_y = self.ship_lot_start_y - self.available_ships_text.height - 10

            self.available_ships_text.x = middle_x - (self.available_ships_text.width / 2)
            self.available_ships_text.y = above_y

            oh.new_object(self.available_ships_text)

            board_1_right_x = self.player_board.x + self.player_board.width
            board_2_left_x = self.enemy_board.x

            self.start_game_text.x = board_1_right_x + ((board_2_left_x - board_1_right_x)/2)
            self.start_game_text.x -= self.start_game_text.width / 2
            self.start_game_text.y = self.ship_lot_start_y + 150

            oh.new_object(self.start_game_text)

            self.text_placed = True

        if self.selected_ship:
            self.selected_ship.selected = True
            self.selected_ship.selected_x, self.selected_ship.selected_y =\
                pygame.mouse.get_pos()

    def _change_to_player_phase(self):
        '''
        Change phase to player turn
        '''
        # self.player_board.deactivate_board()
        # self.enemy_board.activate_board()
        self.current_phase = "PLAYER_TURN"
        self.status_menu.set_status("Player Turn")
        self.status_menu.set_action("Please make a selection on the AI board")


    def _change_to_enemy_phase(self):
        '''
        Change phase to enemey turn
        '''
        # self.player_board.deactivate_board()
        # self.enemy_board.deactivate_board()
        self.current_phase = "ENEMY_TURN"
        self.status_menu.set_status("Enemy Turn")
        self.status_menu.set_action("Please wait while the AI makes a selection on your board")

    def player_turn_phase(self, oh):
        pass

    def enemy_turn_phase(self, oh):
        pass

    def game_ending_phase(self, oh):
        pass

    def options_phase_input(self, oh, events, pressed_keys):
        pass

    def placement_phase_input(self, oh, events, pressed_keys):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.selected_ship:
                        self.selected_ship.selected = False
                        self.selected_ship = None
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

                #FOR TESTING PURPOSES ONLY - Joshua Shequin
                if event.button == 1:
                    if self.start_game_text.hovered:
                        self.clean_up_placement_phase(oh)
                        self._change_to_player_phase()

    def player_turn_phase_input(self, oh, events, pressed_keys):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                #FOR TESTING PURPOSES ONLY - Daniel Brezavar
                if event.button == 2:
                    self._change_to_enemy_phase()

    def enemy_turn_phase_input(self, oh, events, pressed_keys):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                #FOR TESTING PURPOSES ONLY - Daniel Brezavar
                if event.button == 2:
                    self._change_to_player_phase()

    def game_ending_phase_input(self, oh, events, pressed_keys):
        pass

    def clean_up_placement_phase(self, oh):

        oh.remove_object(self.start_game_text)
        self.start_game_text = None

        oh.remove_object(self.available_ships_text)
        self.available_ships_text = None


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

    def __init__(self, il, x=0, y=0):
        BaseObject.__init__(self, il, x=x, y=y)

        self.image_normal = il.load_image(Images.ImageEnum.STARTBATTLE)
        self.image_hovered = il.load_image(Images.ImageEnum.STARTBATTLEHOVERED)
        self.width = self.image_normal.get_width()
        self.height = self.image_normal.get_height()

        self.hovered = False
        self.image = self.image_normal

    def scale_images(self, factor_x, factor_y):
        self.image_normal = transform.scale(self.image_normal,
                                            (self.width*factor_x,
                                             self.height*factor_y))
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
