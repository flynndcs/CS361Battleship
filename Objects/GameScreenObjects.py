from Bases.BaseObjects import BaseObject
from Tools import Images
from pygame import transform, font
import Objects.ShipObjects
import Objects.BattleshipBoard
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

class GameSceneManager(BaseObject):

    def __init__(self, il, player_board, enemy_board, x=0, y=0):
        BaseObject.__init__(self, il, x=x, y=y)

        # this variable will keep track of what phase of the game the player
        # is in.
        self.current_phase = "OPTIONS"
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

        self.ship_lot_start_x = 200
        self.ship_lot_start_y = 700

        # --------------------------------
        #VARIABLES FOR THE PLAYER TURN PHASE
        self.battleship_board_positions = enemy_board.boardPositions

        self.dialog_box = Objects.BattleshipBoard.DialogBox(il)

        #avoids bug where the second turn selection automatically pops up a "hit" dialog without confirm
        self.post_confirm = False

        self.shot_result_displayed = False

        self.selected_position = None
        self.hover_position = None

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
        placed_x_offset = 0
        if not self.ships_added:
            for ship in self.available_ships:
                ship.x = self.ship_lot_start_x + placed_x_offset
                ship.y = self.ship_lot_start_y
                ship.change_directional_state("VERTICAL_DOWN")
                placed_x_offset += ship.width + 20
                oh.new_object(ship)
            self.ships_added = True

        if self.selected_ship:
            self.selected_ship.selected = True
            self.selected_ship.selected_x, self.selected_ship.selected_y =\
                pygame.mouse.get_pos()

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
            #temporary
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    self.current_phase = "PLAYER_TURN"


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

                elif self.dialog_box.confirm_deny_buttons[1].collidepoint(mouseX - self.dialog_box.x, mouseY - self.dialog_box.y):
                    print("pressed deny")
                    self.selected_position = None
                    self.enemy_board.clear_board(oh, self.dialog_box)

            elif event.type == pygame.MOUSEMOTION and self.selected_position is None and self.shot_result_displayed is False:
                mouseX, mouseY = pygame.mouse.get_pos()
                if ((mouseX > 550 and mouseX <= 950) and (mouseY > 150 and mouseY <= 550)):
                    mouse_pos_x = mouseX - self.enemy_board.x
                    mouse_pos_y = mouseY - self.enemy_board.y

                    board_position_x = int(mouse_pos_x / 40)
                    board_position_y = int(mouse_pos_y / 40)

                    if self.hover_position:
                        self.enemy_board.clear_board(oh, None)
                    self.hover_position = self.battleship_board_positions[board_position_x][board_position_y]
                    self.enemy_board.hoverHighlight(self.hover_position)

    def enemy_turn_phase_input(self, oh, events, pressed_keys):
        pass

    def game_ending_phase_input(self, oh, events, pressed_keys):
        pass
