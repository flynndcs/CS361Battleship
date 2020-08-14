'''
Author: Daniel Brezavar
Description: Controls AI ship placement and guessing on player board

How to use:
    ai = BattleshipControllerAI([rows], [cols], [mode])
        -[rows]: the number of rows on gameboard (integer)
        -[cols]: the number of cols on gameboard (integer)
        -[mode]: EASY or HARD (must be capitalized)

    ship_placements, ship_names = ai.place_ships()
        - Returns a list of ship placements in the format "a-b" where a refers to row number and b refers to col number
        - ship_placements will have the following format:
            - ship_placements = [element, element, element, element, element]
            - element will have the following format (list lenght will vary depending on ship length):
                - element = ["a-b", "a-b", "a-b"]
        - ship_names will have the following format:
            - ["Carrier", "Battleship", "Cruiser", "Submarine", "Destroyer"]

    guess = ai.get_next_guess()
        - Returns a guess to be used on the player board in the format "a-b"

    ai.record_result("HIT")
        - Informs that the last guess the AI made was a hit on player board

    ai.record_result("HIT", "[ship_name]")
        - Informs that the last guess the AI made was a hit on player board and the hit resulted in a sunken ship
        - ship_name refers to the name of the ship that was sunk.
            - ship_name must be all capitalized format. For example, if a carrier is sunk it must be passeed into the function as "CARRIER"

    ai.recored_result("MISS")
        -Informs that the last guess the AI made was a miss on the player board. 
'''

from random import randrange

class RandomGuesserAI:
    '''
    Author: Daniel Brezavar
    Description: Class that generates a random guess of all possible available guesses in the 
                 guess tracker class

    usage:
            guess = random_guesser.get_randomized_guess()
    '''
    def __init__(self, guess_tracker):
        self.guess_tracker = guess_tracker

    def _randomized_guess(self, available_guesses):
        '''
        Returns a randomized guess
        '''
        l = len(available_guesses)
        i = randrange(0, l)

        return available_guesses[i]

    def get_randomized_guess(self):
        '''
        Returns a random number between the min/max numbers passed in
        '''
        available_guesses = self.guess_tracker.get_all_available_guesses()

        return self._randomized_guess(available_guesses)

class GuessTrackerAI:
    '''
    Author: Daniel Brezavar
    Description: Keeps track of the guesses the AI makes. If a guess has been made on a 
                 board position, then update that position to either HIT or MISS.

    usage: 
            t = GuessTrackerAI

            t.get_all_available_guesses()

            if (t.is_guess_available(guess)):
                t.record_guess(guess, result)
    '''
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.available_guesses = []
        self.guess_tracker = [["   " for i in range(self.cols)] for j in range(self.rows)]

        self._initialize_available_guesses()

    def get_number_of_available_guesses(self):
        return len(self.available_guesses)

    def get_rows(self):
        return self.rows

    def get_cols(self):
        return self.cols

    def _initialize_available_guesses(self):
        '''
        Creates an array of all available guesses. Guesses will be in the form of "a-b" where
        a is the row number and b is the column number
        '''
        element = ""

        for i in range(0, self.rows):
            for j in range(0, self.cols):
                element = self.pack_guess(i, j)
                self._add_available_guess(element)

    def get_all_available_guesses(self):
        '''
        Returns list of all available guesses
        '''
        return self.available_guesses

    def _check_for_blank(self, row, col):
        '''
        Checks for a blank on the board
        '''
        if (self.guess_tracker[row][col] != "   "):
            return False

        return True

    def _check_for_hit(self, row, col):
        '''
        checks for a hit on the board
        '''
        if (self.guess_tracker[row][col] == "HIT"):
            return False

        return True

    def is_guess_valid(self, guess, check_type=0):
        '''
        Determines if a guess can be used or not

        Check_type determines what type of guess the function is looking for.
        if check_type is -1 just check to see if the guess is on the board (if row and col fit on board)
        If check_type is zero then the function is looking for a blank.
        If ckeck_type is 1 then the function is looking for a hit
        '''
        row, col = self.unpack_guess(guess)

        if (row < 0 or row >= self.get_rows()):
            return False

        if (col < 0 or col >= self.get_cols()):
            return False

        if (check_type == -1):
            return True
        if (check_type == 0):
            return self._check_for_blank(row, col)
        elif (check_type == 1):
            return self._check_for_hit(row, col)

    def _remove_available_guess(self, element):
        '''
        Removes a guess from the available_guesses array
        '''
        self.available_guesses.remove(element)

    def _add_available_guess(self, element):
        '''
        Adds element to available_guesses array
        '''
        self.available_guesses.append(element)

    def pack_guess(self, row, col):
        return "{0}-{1}".format(row, col)

    def unpack_guess(self, guess):
        '''
        Converts a guess to two integers. Guesses are in the format "a-b" where
        a is the row and b is the column
        '''
        u = guess.split("-")
        
        if (len(u) == 2):
            return [int(u[0]), int(u[1])]
        
        return [-1000, -1000]

    def _record_guess_result(self, guess, result):
        '''
        Adds the outcome of a guess to the guess_tracker array
        '''
        row, col = self.unpack_guess(guess)
        self.guess_tracker[row][col] = result

    def record_guess(self, guess, result):
        '''
        Record guess result in guess_tracker array
        '''
        self._remove_available_guess(guess)
        self._record_guess_result(guess, result)

    def get_guess_result(self, guess):
        '''
        Gets the result of a guess in the guess_tracker array
        '''
        row, col = self.unpack_guess(guess)

        if (self.is_guess_valid(guess, check_type=-1)):
            return self.guess_tracker[row][col]

        return "NON"

    def print_arr(self):
        for i in range(self.rows):
            print(self.guess_tracker[i])

class BattleshipEasyAI:
    '''
    Author: Daniel Brezavar
    Description: Handles the backed for the battleship AI easy difficulty. Battleship easy 
                 difficutly will be limited to making only random guesses. The AI will ensure
                 that the guess has not been previously made.
    '''
    def __init__(self, guess_tracker, random_guesser):
        self.guess_tracker = guess_tracker
        self.random_guesser = random_guesser
        self.pending_guess = ""
    
    def make_guess(self):
        '''
        AI makes guesses randomly and ensures the guess hasn't been made yet.
        '''
        self.pending_guess = self.random_guesser.get_randomized_guess()

        return self.pending_guess

    def record_result(self, result, sunk=""):
        self.guess_tracker.record_guess(self.pending_guess, result)

class GuessNavigatorAI:
    '''
    Author: Daniel Brezavar
    Description: When a non random guess needs to be made by the AI, this class controls
                 the directional movement of the AI guesses.

                 guess structure: [guess, direction, guess_info]
    '''
    def __init__(self, guess_tracker, random_guesser):
        self.guess_tracker = guess_tracker
        self.random_guesser = random_guesser
        self.stack = []
        self.pending_hits_queue = []
        self.pending_guess = []
        self.row = -1
        self.col = -1
        self.direction = ""
        self.ccc = 0

    def _get_stack_length(self):
        return len(self.stack)

    def _push_queue(self, guess):
        '''
        Pushes guesses on the pending hits queue. The direction of these hits will be none. This is due to the fact
        that when these hits need to be processed again, the direction of next path needs to be different from the 
        directions already used.
        '''
        self.pending_hits_queue.append([guess, None])

    def _pop_queue(self):
        '''
        Gets the next pending hit. This is done in case there is a sunken ship and there are additional
        hits on the board that need to be processed.
        '''
        return self.pending_hits_queue.pop(0)

    def _remove_all_queue_occurences(self, guess):
        '''
        Removes all occurences from the pending hits list
        '''
        new_list = []

        for element in self.pending_hits_queue:
            if (element[0] != guess):
                new_list.append(element)

        self.pending_hits_queue = new_list

    def _remove_pending_hits(self, guess_list):
        '''
        Removes all hits that resulted in a sunken ship
        '''
        for guess in guess_list:
            self._remove_all_queue_occurences(guess)

    def _stack_push(self, guess, direction):
        self.stack.append([guess, direction])

    def _stack_pop(self, return_type=0):
        guess = self.stack.pop()

        if (return_type == 0): #return full guess array
            return guess
        elif (return_type == 1): #return only the guess ("a-b")
            return guess[0]

    def get_next_guess_location(self):
        '''
        If stack is empty return a random guess. If stack is not empty return the next
        guess
        '''
        # get random guess if no pending guesses
        if (self._get_stack_length() == 0):
            guess = self.random_guesser.get_randomized_guess()
            direction = None

            self._stack_push(guess, direction)

        self.ccc += 1
        print("Round: {}".format(self.ccc))

        print("Stack:")
        print(self.stack)
        print("Queue:")
        print(self.pending_hits_queue)

        # ensures the next guess is a valid guess
        while True:
            # print(self.stack)
            guess = self.stack[-1][0]

            if (self.guess_tracker.is_guess_valid(guess)):
                self.pending_guess = self.stack[-1]
                break
            else:
                self._stack_pop()

        guess = self._stack_pop(return_type=1)
        print("Guess: " + guess)
        print("\n")
        return guess

    def _next_location(self, check_type=0):
        '''
        Determins the next locaiton based on parameters passed in. pushes the new direction on the stack.
        checks to see if the new guess is valid. If valid, the guess will be pushed on to stack.
        Returns true if the new location is valid, returns false if not.
        '''
        guess = ""

        if (self.direction == "NORTH"):
            self.row -= 1
        elif (self.direction == "SOUTH"):
            self.row += 1
        elif (self.direction == "EAST"):
            self.col += 1
        elif (self.direction == "WEST"):
            self.col -= 1

        # This indicates that guesses from pending hits queue are being removed
        if (check_type == 9):
            return

        guess = self.guess_tracker.pack_guess(self.row, self.col)

        if (self.guess_tracker.is_guess_valid(guess, check_type)):
            self._stack_push(guess, self.direction)
            return True

        return False

    def _process_base_hit(self):
        '''
        If the guess was a base and a hit, this function will push the next guesses on the stack around
        the hit. This means that the north, south, east, west positions will be pushed on the stack if they
        are valid
        '''
        row = self.row # must be saved to get accurate 4 positions around base
        col = self.col # must be saved to get accurate 4 positions around base
        index = -1
        directions = ["NORTH", "SOUTH", "EAST", "WEST"]
        l = len(directions)

        # Push the 4 positions around base onto stack
        while (l > 0):
            index = randrange(0, l)
            self.direction = directions[index]
            directions.pop(index)
            l -= 1

            self._next_location(check_type=0)

            self.row = row
            self.col = col

        # print(self.stack)

    def _get_next_non_hit(self):
        '''
        Pushes the next non in on the stack
        '''
        while True:
            # get next non hit
            if (self._next_location(check_type=1)):
                break

            #check to see if guess is not a miss or not on the board
            guess = self.guess_tracker.pack_guess(self.row, self.col)
            result = self.guess_tracker.get_guess_result(guess)

            if (result != "HIT"):
                break

    def _change_to_opposite_direction(self, get_next_non_hit=1):
        '''
        Searches for a miss in the opposite direction passed in as a parameter
        '''
        if (self.direction == "NORTH"):
            self.direction = "SOUTH"
        elif (self.direction == "SOUTH"):
            self.direction = "NORTH"
        elif (self.direction == "EAST"):
            self.direction = "WEST"
        elif (self.direction == "WEST"):
            self.direction = "EAST"

        # Find the next non hit in the opposite direction
        if (get_next_non_hit == 1):
            self._get_next_non_hit()

    def _process_branch_hit(self):
        '''
        If the guess was a branch and a hit, branch guesses will proceed in a line until either a miss is found
        or the guess is off the board. In these situations, the guess will proceed in the opposite direction from the initial hit
        '''

        # if this returns false, that means the guess will be off the board. 
        # In this instance, the next guess must be in the opposite direction of 
        # the original hit
        if (self._next_location(check_type=0)):
            return

        self._change_to_opposite_direction()

    def _set_last_guess_variables(self):
        '''
        Sets the varaibles to determine the last guess information
        '''
        self.row, self.col = self.guess_tracker.unpack_guess(self.pending_guess[0])
        self.direction = self.pending_guess[1]

    def _get_ship_length(self, sunk):
        '''
        Returns the length of the ship sunk
        '''
        if (sunk == "CARRIER"):
            return 5
        elif (sunk == "BATTLESHIP"):
            return 4
        elif (sunk == "SUBMARINE"):
            return 3
        elif (sunk == "CRUISER"):
            return 3

        return 2

    def _process_sunken_ship(self, sunk):
        '''
        processes a sunken ship. Removes all sunken ship locations from the pending hits queue. A sunken ship will be in the
        opposed direction of self.direction. 
        '''
        guess_list = []
        length = self._get_ship_length(sunk)
        self._change_to_opposite_direction(get_next_non_hit=0)

        # Remove the initial guess
        guess_list.append(self.guess_tracker.pack_guess(self.row, self.col))
        length -= 1

        for _ in range(length):
            self._next_location(check_type=9)
            guess_list.append(self.guess_tracker.pack_guess(self.row, self.col))

        self._remove_pending_hits(guess_list)

        # If pending hits queue is empty, then all hits have been processed and all other
        # guesses in the stack do not need to be processed. Stack will be cleared in this case. 
        # if pending hits queue is not empty, then there are pending hits that have not been
        # processed. In this case, the next guess in queue will be processed. 
        if (len(self.pending_hits_queue) == 0):
            self.stack = []
        else:
            guess, direction = self._pop_queue()
            self._stack_push(guess, direction)

    def process_hit(self, sunk):
        '''
        self.pending_guess was hit on the player board. If pending_guess was a base guess, calls function
        to push random directions on the stack in all 4 directions. If pending_guess was not a base, calls
        function to push the next position in the same direction on the stack
        '''
        self._set_last_guess_variables()

        # Record the result of the last guess
        guess = self.guess_tracker.pack_guess(self.row, self.col)
        self._push_queue(guess)
        self.guess_tracker.record_guess(guess, "HIT")

        if (sunk == ""):
            if (self.direction == None):
                self._process_base_hit()
                # print(self.stack)
            else:
                self._process_branch_hit()
        else:
            self._process_sunken_ship(sunk)

    def process_miss(self):
        '''
        Updates the guess tracker with a miss
        '''
        self._set_last_guess_variables()

        guess = self.guess_tracker.pack_guess(self.row, self.col)
        self.guess_tracker.record_guess(guess, "MIS")

class BattleshipHardAI:
    '''
    Author: Daniel Brezavar
    Description: AI makes random guesses until there is a hit. Once there is a hit the guess 
                 will no longer be random and start making guesses in a line. There are 4 outcomes
                 to guessing in a line:

                 1) The ship in question is eventually sunk
                 2) The AI encounters a miss. In this case the AI will proceed in the opposite
                    direction of the initial hit
                 3) The AI encounters a guess that is not on the board. In this case the AI will
                    proceed in the opposite direction of the initial hit
                 4) 2 or more ships are place side by side and the AI encounters a hit on either
                    end of the line. In this case the AI will proceed perpendicular in the direction
                    of the initial hit. The hits are 

                uses dfs to find hits after an initial hit.
                Need a check that the guess in stack is valid
                need a check that the ship is sunk
    '''
    def __init__(self, guess_tracker, random_guesser):
        self.guess_tracker = guess_tracker
        self.random_guesser = random_guesser
        self.navigator = GuessNavigatorAI(self.guess_tracker, self.random_guesser)

    def make_guess(self):
        '''
        returns a locational guess
        '''
        return self.navigator.get_next_guess_location()

    def record_result(self, result, sunk=""):
        if (result == "HIT"):
            self.navigator.process_hit(sunk)
        elif (result == "MISS"):
            self.navigator.process_miss()

class BattleshipControllerAI:
    '''
    Author: Daniel Brezavar
    Description: Handles the backend for the battleship AI guessing.

                 There are 2 levels of difficulty:
                    Level 1: AI only makes random guesses
                    Level 2: AI makes random guesses until hit, then builds off the initial hit
    '''
    def __init__(self, rows, cols, difficulty):
        self.guess_tracker = GuessTrackerAI(rows, cols)
        self.random_guesser = RandomGuesserAI(self.guess_tracker)
        self.ship_placer = ShipPlacerAI(rows, cols)
        self.ai = None

        if (difficulty == "EASY"):
            self.ai = BattleshipEasyAI(self.guess_tracker, self.random_guesser)
        elif (difficulty == "HARD"):
            self.ai = BattleshipHardAI(self.guess_tracker, self.random_guesser)

    def print(self):
        self.guess_tracker.print_arr()

    def get_next_guess(self):
        return self.ai.make_guess()

    def print_guesses(self):
        self.guess_tracker.print_arr()

    def make_all_guesses(self):
        result = "HIT"

        while (self.guess_tracker.get_number_of_available_guesses() > 0):
            # print(self.ai.make_guess())
            self.record_result(result)
            self.print()

    def record_result(self, result, sunk=""):
        self.ai.record_result(result, sunk)

    def place_ships(self):
        return self.ship_placer.place_ships()

class ShipPlacerAI:
    '''
    Author: Daniel Brezavar
    Description: Places the ships on a gameboard. Placement is carried out using the following structure:
        1) Randomly select a location on the gameboard
        2) Randomly choose a direction to place the ship (North, South, East, West)
        3) Determine if the ship fits in that location
        4) If ship fits, place ship. If ship doesn't fit continue to step 1
        5) Continue for all ships

    Ships are returned to the calling function as a array. Each element of the array is an array of ship locations in the format:
        a-b where a is the row and b is the col
    '''
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.directions = ["NORTH", "SOUTH", "EAST", "WEST"]
        self.guess_tracker = GuessTrackerAI(self.rows, self.cols)
        self.random_guesser = RandomGuesserAI(self.guess_tracker)
        self.ship_length_array = self._initialize_ship_lengths()
        
    def _initialize_ship_lengths(self):
        '''
        Sets the ship lengths that are to be used to place ships on the board
        '''
        ship_length_array = []

        # Length of carrier
        ship_length_array.append(5)

        # Length of battleship
        ship_length_array.append(4)

        # Length of cruiser
        ship_length_array.append(3)

        # Length of submarine
        ship_length_array.append(3)

        # Length of destroyer
        ship_length_array.append(2)

        return ship_length_array

    def _randomize_direction(self):
        '''
        Returns a randomized direction
        '''
        i = randrange(0, 4)
        return self.directions[i]

    def _move_directionally(self, row, col, direction, movement_len=1):
        '''
        Moves a ship and returns the new row and col
        '''
        if (direction == "NORTH"):
            row -= movement_len
        elif (direction == "SOUTH"):
            row += movement_len
        elif (direction == "EAST"):
            col += movement_len
        elif (direction == "WEST"):
            col -= movement_len

        return row, col

    def _check_each_location(self, row, col, ship_len, direction):
        '''
        checks if each location is valid before placing the ship on the game board
        '''
        for _ in range(ship_len):
            row, col = self._move_directionally(row, col, direction, 1)
            guess = self.guess_tracker.pack_guess(row, col)

            if (not self.guess_tracker.is_guess_valid(guess, 0)):
                return False

        return True

    def _is_ship_placement_valid(self, guess, ship_len, direction):
        '''
        Determines if the ship will fit on the board
        '''
        start_row, start_col = self.guess_tracker.unpack_guess(guess)
        end_row, end_col = self._move_directionally(start_row, start_col, direction, ship_len)
        end_location = self.guess_tracker.pack_guess(end_row, end_col)

        if (self.guess_tracker.is_guess_valid(end_location, 0)):
            return self._check_each_location(start_row, start_col, ship_len, direction)

        return False

    def _pack_ship_location(self, guess, ship_len, direction):
        '''
        Creates an array of a single ship location on a gameboard
        '''
        location = guess
        ship_location = []

        for _ in range(ship_len):
            start_row, start_col = self.guess_tracker.unpack_guess(location)
            next_row, next_col = self._move_directionally(start_row, start_col, direction, 1)
            location = self.guess_tracker.pack_guess(next_row, next_col)
            ship_location.append(location)
            self.guess_tracker.record_guess(location, "USED")
            # d_check.append(location)

        return ship_location

    def _determine_ship_location(self, ship_len):
        '''
        Determines where the ship location will be on the gameboard
        '''
        guess = ""
        direction = ""

        while True:
            guess = self.random_guesser.get_randomized_guess()
            direction = self._randomize_direction()

            if (self._is_ship_placement_valid(guess, ship_len, direction)):
                break

        return self._pack_ship_location(guess, ship_len, direction)

    def _get_ship_names(self):
        '''
        Returns the names of the ships
        '''

        ship_names = []

        ship_names.append("Carrier")
        ship_names.append("Battleship")
        ship_names.append("Cruiser")
        ship_names.append("Submarine")
        ship_names.append("Destroyer")

        return ship_names

    def place_ships(self):
        '''
        Places each ship on the board that is in the ship_length_array
        '''
        ship_locations = []
        ship_names = self._get_ship_names()

        for ship_len in self.ship_length_array:
            ship_locations.append(self._determine_ship_location(ship_len))

        return ship_locations, ship_names

# FOR TESTING PURPOSES ONLY - DANIEL BREZAVAR   


# Test easy AI
# battleship_ai = BattleshipControllerAI(10, 10, "EASY")
# battleship_ai.make_all_guesses()








# Test ship placement
# no_dup_count = 0
# has_dup_count = 0
# out_of_range_count = 0


# for i in range(10):
#     if (i % 1000 == 0):
#         print(i)

#     d_check = []
#     dup_check = []
#     ai = BattleshipControllerAI(10, 10, "HARD")
#     r, f = ai.place_ships()
#     print(f)
#     # print(r)
    
#     for j in range(0, len(d_check)):
#         dup_check.append(d_check[j])

#     # print(dup_check)

#     if len(dup_check) == len(set(dup_check)):
#         # print("No duplicates")
#         no_dup_count += 1
#     else:
#         # print("Duplicates")
#         has_dup_count += 1

#     for element in dup_check:
#         g = element.split("-")
#         row = int(g[0])
#         col = int(g[1])

#         if (row < 0 or row > 9):
#             out_of_range_count += 1
        
#         if (col < 0 or row > 9):
#             out_of_range_count += 1

# print("Duplicates: {}".format(has_dup_count))
# # print("No duplicates: {}".format(no_dup_count))
# print("Out of range count: {}".format(out_of_range_count))






# Test AI hard. test reversing directions
# ai = BattleshipControllerAI(10, 10, "HARD")
# print(ai.get_next_guess())
# ai.record_result("HIT")
# print(ai.get_next_guess())
# ai.record_result("HIT")
# print(ai.get_next_guess())
# ai.record_result("HIT")
# print(ai.get_next_guess())
# ai.record_result("HIT")
# print(ai.get_next_guess())
# ai.record_result("HIT")
# print(ai.get_next_guess())
# ai.record_result("HIT")
# print(ai.get_next_guess())
# ai.record_result("HIT")
# print(ai.get_next_guess())
# ai.record_result("HIT")
# print(ai.get_next_guess())
# ai.record_result("HIT")
# print(ai.get_next_guess())
# ai.record_result("HIT")
# print(ai.get_next_guess())
# ai.record_result("HIT")
# print(ai.get_next_guess())
# ai.record_result("HIT")
# print(ai.get_next_guess())
# ai.record_result("HIT")
# print(ai.get_next_guess())
# ai.record_result("HIT")
# print(ai.get_next_guess())
# ai.record_result("HIT")
# print(ai.get_next_guess())
# ai.record_result("HIT")
# print(ai.get_next_guess())
# ai.record_result("HIT")
# print(ai.get_next_guess())
# ai.record_result("HIT")
# print(ai.get_next_guess())
# ai.record_result("HIT")
# ai.print_guesses()











# Test ai hard sunk
# ai = BattleshipControllerAI(10, 10, "HARD")
# # 1
# ai.get_next_guess()
# ai.record_result("HIT")
# # 2
# ai.get_next_guess()
# ai.record_result("MISS")
# # 3
# ai.get_next_guess()
# ai.record_result("HIT")
# # 4
# ai.get_next_guess()
# ai.record_result("HIT")
# # 5
# ai.get_next_guess()
# ai.record_result("HIT")
# # 6
# ai.get_next_guess()
# ai.record_result("HIT", "CARRIER")
# # 7
# ai.get_next_guess()
# ai.record_result("HIT")
# # 8
# ai.get_next_guess()
# ai.record_result("MISS")
# # 9
# ai.get_next_guess()
# ai.record_result("HIT")
# ai.print_guesses()



