"""
This file creates the Board class which models a normal 15x15 Scrabble board.
You can put only Tiles on a board, and the board provides convenience functions
that allow you to add new Tiles, remove Tiles, move Tiles, score words, etc.
"""

from constants import NON, DLS, DWS, TLS, TWS
from constants import BOARD_LAYOUT

BOARD_SIZE = 15


class Board:
    """This class models a Scrabble board.
    You can manage tiles and score words."""
    bonuses = BOARD_LAYOUT # 2-dimensional array with normal bonus squares
    
    
    def __init__(self):
        """Creates a Board with the normal bonus squares and size."""
        self.__tiles = [[None for x in range(BOARD_SIZE)]
            for y in range(BOARD_SIZE)]
        # a 2-dimensional array with blank spaces as None

    def add_tile(self, tile, coordinate):
        """Adds the specified tile at the specified coordinate"""
        self.__tiles[coordinate.get_row()][coordinate.get_col()] = tile
    
    def get_tile(self, coordinate):
        """Returns the tile at the specified coordinate or None"""
        return self.__tiles[coordinate.get_row()][coordinate.get_col()]
    
    def get_bonus(self, coordinate):
        """
        Returns the bonus square in particular space. The values mean:
        0 => normal square
        1 => Double Letter Score
        2 => Double Word Score
        3 => Triple Letter Score
        4 => Triple Word Score
        """
        return BOARD_LAYOUT[coordinate.get_row()][coordinate.get_col()]

    def get_letter_multiplier(self, coordinate):
        """Returns 2 if coordinate has a DLS and 3 if
        it has a TLS, 1 otherwise."""
        if self.get_bonus(coordinate) == DLS:
            return 2
        elif self.get_bonus(coordinate) == TLS:
            return 3
        else:
            return 1

    def get_word_multiplier(self, coordinate):
        """Returns 2 if coordinate has a DWS and 3 if
        it has a TWS, 1 otherwise."""
        if self.get_bonus(coordinate) == DWS:
            return 2
        elif self.get_bonus(coordinate) == TWS:
            return 3
        else:
            return 1

    def __str__(self):
        """Returns a human-readable table with * standing in for blank spots"""
        string = ""
        for row in self.__tiles:
            for tile in row:
                if tile is None:
                    string += '*'
                else:
                    string += str(tile)
            string += '\n'
        return string

    def is_valid_word(self, word, coordinate):
        """Returns True if the play is possible (no spaces or overlapping tiles)
        and False otherwise."""
        current_coord = coordinate  # track where we are in the word
        for tile in word:
           # print("Checking if {} can be played over {}".format(
           #     str(tile), str(self.get_tile(current_coord)))
           #)
            if tile is None:  # existing tile SHOULD be there
                if self.get_tile(current_coord) is None:
                    return False
            else:
                if self.get_tile(current_coord) is not None:
                    return False
            print(str((current_coord.get_col() <=
                    coordinate.get_col() + len(word) - 1)))
            print("Tried {}".format(tile))
            print(word.index(tile))
            current_coord = current_coord.safe_increment()
        return True
        
    def add_word(self, word, coordinate):
        """
        Adds the given word (a list of Tiles with None to mark
        existing tiles) to the board at the given coordinate, raising
        ValueError if the word goes out of bounds, is completely overlapped
        by existing tiles, or has None in a spot where there is no existing
        tile.
        """
        if not self.is_valid_word(word, coordinate):
            raise ValueError("Invalid word: overlapping or missing tiles")
        
        current_coord = coordinate  # track where we are in the word
        for tile in word:
            if tile is not None:  # existing tile should not be there
                self.add_tile(tile, current_coord)
            current_coord = current_coord.safe_increment()

    def count_word(self, word, coordinate):
        """Scores a word, NOT including parallel plays."""
        current_coord = coordinate #track our place in the word
        score = 0
        word_multiplier = 1  # to keep track of word multipliers
        
        for tile in word:  # score the main play first
            print("Playing '{}' at {}".format(str(tile), str(current_coord)))
            if tile is None:  # just score the letter value
                existing_tile = self.get_tile(current_coord)
                score += (existing_tile.get_value() *
                            self.get_letter_multiplier(current_coord))
            else:
                word_multiplier *= self.get_word_multiplier(current_coord)
                score += (tile.get_value() *
                            self.get_letter_multiplier(current_coord))
            try:
                #print("Increment {}".format(str(current_coord)))
                current_coord = current_coord.increment()
            except ValueError:
                pass  # went over the border, but fine: if real error, will
                      # get thrown in next loop run
            
        score *= word_multiplier
        # add bingo bonus
        if len([letter for letter in word if letter is not None]) == 7:
            score += 50
        return score
    
    def score_word(self, word, coordinate):
        """Scores the given word, including parallel plays. Raises ValueError
        if the word cannot play in the given space."""
        
        current_coord = coordinate  # track our place in the word    
        total_score = self.count_word(word, coordinate)  # score the main word
        word_multiplier = 1
        
        if coordinate.is_horizontal():  #parallel plays will be in columns
            # for all columns, find parallel plays and score them
            while (current_coord is not None and current_coord.get_row() <=
                    coordinate.get_row() + len(word) - 1):
                print("Checking coordinate {}".format(current_coord))
                score = 0
                # check above the word for parallel plays, avoiding ValueError
                above_coord = current_coord.safe_move_up()
                
                below_coord = current_coord.safe_move_down()
                
                # if there is a parallel play to check
                if not (self.get_tile(above_coord) is None and
                            self.get_tile(below_coord) is None):

                    word_multiplier *= self.get_word_multiplier(current_coord)
                    print("Scoring column {} at row {}".format(
                      current_coord.get_col(), current_coord.get_row()))
                    # count the tiles below the world, including the actual word
                    coord_below = current_coord
                    # until the word ends                    
                    while self.get_tile(coord_below) is not None:  
                        score += (self.get_tile(coord_below).get_value() *
                                    self.get_letter_multiplier(coord_below))
                        print("Adding to score")
                        coord_below = coord_below.safe_move_down()
                    
                    # count the tiles above the word
                    coord_above = current_coord.safe_move_up()
                    # until the word stops
                    while self.get_tile(coord_above) is not None: 
                        score += (self.get_tile(coord_above).get_value() *
                                    self.get_letter_multiplier(coord_above))

                        coord_above = coord_above.safe_move_up()
                    total_score += word_multiplier * score

                
                #print(str(coordinate) + "----")
                print("The coordinate is " + str(current_coord))
                print(str((current_coord.get_col() <=
                    coordinate.get_col() + len(word) - 1)))
                #print("The score is " + str(total_score))
                #print("Above_tile is " + str(above_tile))
                #print("Below_tile is " + str(below_tile))
                current_coord = current_coord.safe_increment()
        else:  # parallel plays in the rows
            # for all rows, find the parallel plays
            while (current_coord is not None and
                    current_coord.get_row() <=
                    coordinate.get_row() + len(word) - 1):
                score = 0
                print("Checking coordinate {}".format(current_coord))
                # check above the word for parallel plays
                left_coord = current_coord.safe_move_left()
                
                right_coord = current_coord.safe_move_right()
                
                # if there is a parallel play to check
                if not (self.get_tile(left_coord) is None and
                            self.get_tile(right_coord) is None): 
                    word_multiplier *= self.get_word_multiplier(current_coord)
                    # count the tiles to the left of the world
                    # including the actual word
                    coord_left = current_coord 
                    # until the word stops
                    while self.get_tile(coord_left) is not None:
                        score += (self.get_tile(coord_left).get_value() *
                                    self.get_letter_multiplier(coord_left))
                        print("Adding {} to score".format(
                            (self.get_tile(coord_left).get_value() *
                                    self.get_letter_multiplier(coord_left))
                        ))
                        #print(coord_left)
                        coord_left = coord_left.safe_move_left()
                    
                    # count the tiles to the right of the word
                    coord_right = current_coord.safe_move_right()
                    # until the word stops
                    while self.get_tile(coord_right) is not None:
                        score += (self.get_tile(coord_right).get_value() *
                                    self.get_letter_multiplier(coord_right))
                        coord_right = coord_right.safe_move_right()
                    total_score += word_multiplier * score

                print("The coordinate is " + str(current_coord))
                print(str((current_coord.get_col() <=
                    coordinate.get_col() + len(word) - 1)))
                #print("The score is " + str(total_score))
                current_coord = current_coord.safe_increment()
        return total_score

    def play_word(self, word, coordinate):
        """Adds the word to the board and returns the score"""
        self.add_word(word, coordinate)
        return self.score_word(word, coordinate)

    
                
                
                
                
                
                
                
                
                
                
                
                