'''
Author: Daniel Brezavar
Date: 21Jul2020
Description: GameController class controls the flow of the game. This class controls when the game starts,
             when the game ends, keeps track of turns, and determines if the game finishes.

usage:
    game_controller = GameController()
    
    if (game_controller.continue_game()):
        game_controller.next_turn()
'''

class GameController:
    '''
    Class that keeps track of game flow

    Attributes:
        player_board        board that the player is currently using
        ai_baoard           board that the AI is currently using
        battleship_ai       algorithm for controlling AI guesses

    '''
    def __init__(self):
        battleship_player = BattleshipPlayer()
        battleship_ai = BattleshipAI()
        winner = ""

    def get_winner_message(self):
        '''
        Return the winning message that should be displayed on screen when the
        game has been completed. 
        '''
        message = ""

        if (winner == "Player"):
            message = "Congratulations! The player has won Battleship."
        else:
            message = "The AI has won Battleship. Better luck next time."

        return message

    def continue_game(self):
        '''
        Determine if the game should continue. This is decided by making calls
        to both player and AI battleship classes. If all ships on either board 
        have been sunk then the function returns false to indicate the game 
        has been completed. Otherwise return true
        '''

        if (!self.battleship_player.are_ships_sunk()):
            self.winner = "AI"
            return False

        if (!self.battleship_ai.are_ships_sunk()):
            self.winner = "Player"
            return False

        return True

    def next_turn(self):