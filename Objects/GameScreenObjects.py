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

        self.ship_lot_start_x = 200
        self.ship_lot_start_y = 700

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

    def player_turn_phase_input(self, oh, events, pressed_keys):
        pass

    def enemy_turn_phase_input(self, oh, events, pressed_keys):
        pass

    def game_ending_phase_input(self, oh, events, pressed_keys):
        pass
