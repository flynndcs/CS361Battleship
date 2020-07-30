import Objects.ShipObjects
import Objects.BattleshipBoard
import pygame.mouse
from Objects.BattleshipBoard import BattleshipBoard
from Bases.BaseObjects import BaseObject
from Tools import Images
from pygame import transform, font
from random import randrange


class GameScreenStatusMenu(BaseObject):
    '''
    Author: Daniel Brezavar
    Description: Displays game status and actions required for the user
    '''

    def __init__(self, il, x=0, y= 0):
        BaseObject.__init__(self, il, x=x, y=y)

        self.font1 = font.Font("Fonts/OpenSans-Light.ttf", 25)
        self.font2 = font.Font("Fonts/OpenSans-Light.ttf", 20)

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

    def _render_status_menu_border(self, canvas):
        '''
        Renders the status menu border
        '''
        pygame.draw.circle(canvas, (255, 255, 255), (self.border_x, self.y), self.border_circle_radius)
        pygame.draw.circle(canvas, (255, 255, 255), (self.border_x, self.y + self.border_height), self.border_circle_radius)
        pygame.draw.circle(canvas, (255, 255, 255), (self.border_x + self.border_width, self.y), self.border_circle_radius)
        pygame.draw.circle(canvas, (255, 255, 255), (self.border_x + self.border_width, self.y + self.border_height), self.border_circle_radius)
        pygame.draw.rect(canvas, (255, 255, 255), (self.border_x, self.y - self.border_circle_radius, self.border_width, self.border_height + (2 * self.border_circle_radius)))
        pygame.draw.rect(canvas, (255, 255, 255), (self.border_x - self.border_circle_radius, self.y, self.border_width + (2 * self.border_circle_radius), self.border_height))

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
        
        self.player_board = BattleshipBoard(self.IL, self.player_board_x, self.board_y)
        self.player_title = BoardIdentifier(self.IL, "Player Board", 128, 25, self.player_board_x + 10, self.board_y - 35)
        self.enemy_board = BattleshipBoard(self.IL, self.enemy_board_x, self.board_y)
        self.enemy_title = BoardIdentifier(self.IL, "Enemy Board", 128, 25, self.enemy_board_x + 10, self.board_y - 35)
        self.status_menu = GameScreenStatusMenu(self.IL, 60, 60)

        self.placement_phase_manager = PlacementPhaseHandler(self.IL, self.status_menu, self.player_board, self.enemy_board, self)
        self._initialize_placement_phase_objects()


        #VARIABLES FOR THE PLAYER TURN PHASE
        self.battleship_board_positions = self.enemy_board.boardPositions

        self.dialog_box = Objects.BattleshipBoard.DialogBox(self.IL)

        #avoids bug where the second turn selection automatically pops up a "hit" dialog without confirm
        self.post_confirm = False

        self.shot_result_displayed = False

        self.selected_position = None
        self.hover_position = None

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
        self.current_phase = "PLACEMENT"  # just skipping this phase for now

    def placement_phase(self, oh):
        self.placement_phase_manager.update(oh)

    def player_turn_phase(self, oh):
        if (self.enemy_board_initialized == False):
            self._initialize_enemy_board()

    def enemy_turn_phase(self, oh):
        pass

    def game_ending_phase(self, oh):
        pass

    def options_phase_input(self, oh, events, pressed_keys):
        pass

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
                if self.dialog_box.confirm_deny_buttons[0].collidepoint(mouseX - self.dialog_box.x, mouseY - self.dialog_box.y):
                    print("pressed confirm")
                    self.dialog_box.confirm_shot()
                    self.shot_result_displayed = True
                    self.selected_position = None
                    self.enemy_board.determine_selection_result(self.IL, self.OH)
                    self._change_to_enemy_phase()
                    self.enemy_board.clear_board(oh, self.dialog_box)

                elif self.dialog_box.confirm_deny_buttons[1].collidepoint(mouseX - self.dialog_box.x, mouseY - self.dialog_box.y):
                    print("pressed deny")
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
        x = randrange(10)
        y = randrange(10)
        self.player_board.set_square_selection(x, y)
        self.player_board.determine_selection_result(self.IL, self.OH)
        self._change_to_player_phase()

    def game_ending_phase_input(self, oh, events, pressed_keys):
        pass

    def _change_to_player_phase(self):
        '''
        Change phase to player turn
        '''
        # self.player_board.deactivate_board()
        # self.enemy_board.activate_board()
        self.current_phase = "PLAYER_TURN"
        self.status_menu.set_status("Player Turn")
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

class PlacementPhaseHandler:

    def __init__(self, il, status_menu, player_board, enemy_board, phase_manager):

        self.player_board = player_board
        self.enemy_board = enemy_board
        self.status_menu = status_menu
        self.phase_manager = phase_manager

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

        # self.ship_lot_start_x = self.player_board.x + (
        #             self.player_board.width / 2)
        # self.ship_lot_start_y = self.player_board.y + self.player_board.height + 125

        self.ship_lot_start_x = self.player_board.x + 640
        self.ship_lot_start_y = self.player_board.y + 125

        self.ship_lot_x_offset = 20

        self.resize_ships()

    def update(self, oh):
        # self.player_board.activate_board()
        # self.enemy_board.deactivate_board()
        self.status_menu.set_status("Placement")
        self.status_menu.set_action("Please place your ships on the player gameboard")

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

        if not self.text_placed:
            middle_x = self.ship_lot_start_x + (placed_x_offset / 2)
            above_y = self.ship_lot_start_y - self.available_ships_text.height - 10

            self.available_ships_text.x = middle_x - (
                        self.available_ships_text.width / 2)
            self.available_ships_text.y = above_y

            oh.new_object(self.available_ships_text)

            board_1_right_x = self.player_board.x + self.player_board.width
            board_2_left_x = self.enemy_board.x

            # self.start_game_text.x = board_1_right_x + (
            #             (board_2_left_x - board_1_right_x) / 2)
            # self.start_game_text.x -= self.start_game_text.width / 2
            # self.start_game_text.y = self.ship_lot_start_y + 150

            self.start_game_text.x = self.ship_lot_start_x
            # self.start_game_text.x -= self.start_game_text.width / 2
            self.start_game_text.y = self.ship_lot_start_y + 225

            oh.new_object(self.start_game_text)

            self.text_placed = True

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
                        else:
                            self.display_not_possible()
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
                # FOR TESTING PURPOSES ONLY - Joshua Shequin
                if event.button == 1:
                    if self.start_game_text.hovered:
                        self.clean_up_placement_phase(oh)
                        self.phase_manager._change_to_player_phase()

    def clean_up_placement_phase(self, oh):

        oh.remove_object(self.start_game_text)
        self.start_game_text = None

        oh.remove_object(self.available_ships_text)
        self.available_ships_text = None

    def get_size_of_rects(self):
        # currently just a placeholder function return until there is an
        # outward facing function/variable from the boards.
        return 40, 40

    def resize_ships(self):

        new_x, new_y = self.get_size_of_rects()

        for ship in self.available_ships:
            ship.scale_ship(new_x, new_y)

    def snap_ship_to_grid(self, mouse_x, mouse_y):

        left_side_of_board = self.player_board.x
        y_of_board = self.player_board.y
        snapped_x = left_side_of_board
        snapped_y = y_of_board
        x_box_size, y_box_size = self.get_size_of_rects()

        mouse_pos_x = mouse_x - self.player_board.x
        mouse_pos_y = mouse_y - self.player_board.y

        board_position_x = (mouse_pos_x // x_box_size) * 40 + left_side_of_board
        board_position_y = (mouse_pos_y // y_box_size) * 40 + y_of_board

        if mouse_y > y_of_board:
            snapped_y = board_position_y
        if mouse_x > left_side_of_board:
            snapped_x = board_position_x

        if self.selected_ship.directional_state == "HORIZONTAL_LEFT":
            snapped_x += 40
        elif self.selected_ship.directional_state == "VERTICAL_UP":
            snapped_y += 40
        self.selected_ship.selected_x = snapped_x
        self.selected_ship.selected_y = snapped_y

    def check_placement(self):

        return True

    def display_not_possible(self):

        pass

    def place_ship(self):

        pass


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


class ToMainScreen(BaseObject):
    """
    Returns users to the main screen
    Author: Alex Wilson
    """

    def __init__(self, il, x=23, y=900):
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
        # if user hovers over quit game, color is changed from white to red
        if 23 < location[0] < 169 and 910 < location[1] < 935 and self.click_num == 0:
            self.quit_game = self.quit_game_hover
        # if users cursor anywhere else on board, quit message is white
        elif self.click_num == 0:
            self.quit_game = self.font.render("Quit Game", True, (255, 255, 255))
        # if user hovers over confirm quit, color is changed from white to red
        elif 23 < location[0] < 312 and 911 < location[1] < 935 and self.click_num == 1:
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
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # if user clicks quit game, they are prompted with a confirm quit message
                if 23 < location[0] < 169 and 910 < location[1] < 935 and self.click_num == 0:
                    self.click_num += 1
                    self.quit_game = self.quit_game_pressed
                # if the user clicks to confirm quit, true is returned and they are returned to menu screen
                elif 23 < location[0] < 312 and 911 < location[1] < 935 and self.click_num == 1:
                    return True
                # if user doesn't confirm to quit, quit game message and click number are reset
                else:
                    self.quit_game = self.font.render("Quit Game", True, (255, 255, 255))
                    self.click_num = 0

    def render(self, canvas):
        canvas.blit(self.quit_game, (self.x, self.y))



