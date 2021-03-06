"""
This file creates the Board class which models a normal 15x15 Scrabble board.
You can put only Tiles on a board, and the board provides convenience functions
that allow you to add new Tiles, remove Tiles, move Tiles, score words, etc.
"""

from constants import NON, DLS, DWS, TLS, TWS
from constants import BOARD_LAYOUT
import coordinate as coordinate_module
from move import Move


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

    def safe_get_tile(self, coordinate):
        """Returns the tile at the specified coordinate but returns None
        if the coordinate is None"""
        try:
            return self.__tiles[coordinate.get_row()][coordinate.get_col()]
        except AttributeError:
            return None

    def remove_tile(self, coordinate):
        """
        Removes the tile at the given coordinate: raises an error
        if the square has nothing on it.
        """
        self.__tiles[coordinate.get_row()][coordinate.get_col()] = None

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

    def is_valid_move(self, move):
        """Returns True if the play is possible (no spaces or overlapping tiles)
        and False otherwise."""
        current_coord = move.get_coord()  # track where we are in the word
        word = move.get_just_played_tiles()
        #print(word)
        for tile in word:
            #print("Checking if {} can be played over {}".format(
            #     str(tile), str(self.get_tile(current_coord)))
            #)
            if tile is None:  # existing tile SHOULD be there
                if self.get_tile(current_coord) is None:
                    return False
            else:
                if self.get_tile(current_coord) is not None:
                    return False

            current_coord = current_coord.safe_increment()
        return True
        
    def add_move(self, move):
        """Adds the given move to the board."""
        word = move.get_just_played_tiles()
        coordinate = move.get_coord()

        if not self.is_valid_move(move):
            raise ValueError("Invalid word: overlapping or missing tiles")
        
        current_coord = coordinate  # track where we are in the word
        for tile in word:
            if tile is not None:  # existing tile should not be there
                self.add_tile(tile, current_coord)
            current_coord = current_coord.safe_increment()

    def remove_move(self, move):
        """Removes a given Move from the board."""
        current_coord = move.get_coord()

        for index, tile in enumerate(move):
            if move.was_just_played(index):
                self.remove_tile(current_coord)
            current_coord = current_coord.safe_increment()
    

    def count_move(self, move):
        """Scores a word, NOT including parallel plays."""
        word_added = False  # flag  
        if not self.is_move_present(move):  # move not on board
            self.add_move(move)  # add the word
            word_added = True  # flag

        word = move.get_just_played_tiles()
        coordinate = move.get_coord()
        current_coord = coordinate  # track our place in the word
        score = 0
        word_multiplier = 1  # to keep track of word multipliers
        
        for tile in word:
            if tile is None: # just count letter value then move on
                score += self.get_tile(current_coord).get_value()
            
            else:
                score += (self.get_letter_multiplier(current_coord) *
                            tile.get_value())
        
                word_multiplier *= self.get_word_multiplier(current_coord)
            
            current_coord = current_coord.safe_increment()

        score *= word_multiplier  # update score with word bonuses
        # check for bingo bonus
        if len([tile for tile in word if tile is not None]) == 7:
            score += 50

        if word_added:  # remove the word after done scoring it
            self.remove_move(move)

        return score
    
    def score_move(self, move):
        """Scores the given move, including parallel plays."""
        # if the word isn't on the board, we add it then remove it again
        word_added = False  # flag  
        if not self.is_move_present(move):  # move not on board
            self.add_move(move)  
            word_added = True  # flag

        word = move.get_just_played_tiles()
        coordinate = move.get_coord()
        current_coord = coordinate  # used for tracking
        total_score = self.count_move(move)  # count the main play


        if coordinate.is_horizontal():  # parallel plays in columns
            for tile in word:
                # if this is an existing tile, nothing needs to be done
                if tile is None:
                    pass

                else:
                    above_current = current_coord.safe_move_up()
                    below_current = current_coord.safe_move_down()
                    
                    # avoid error if on the border of the board
                    above_tile = self.safe_get_tile(above_current)
                    below_tile = self.safe_get_tile(below_current)
                    
                    # no parallel plays
                    if above_tile is None and below_tile is None:
                        pass
                    else:
                        word_multiplier = self.get_word_multiplier(current_coord)
                        score = 0  # keep track of score for this parallel play
                        # count the tile in the main word
                        score += (self.get_letter_multiplier(current_coord) *
                                    tile.get_value())
                        
                        # check for letters above the main word
                        above = current_coord.safe_move_up()
                        while (above is not None and
                                self.get_tile(above) is not None):
                            # no multipliers
                            score += self.get_tile(above).get_value()
                            above = above.safe_move_up()
                        
                        below = current_coord.safe_move_down()
                        while (below is not None and
                                self.get_tile(below) is not None):
                            # no multipliers
                            score += self.get_tile(below).get_value()
                            below = below.safe_move_down()
                        # update main score                        
                        total_score += score * word_multiplier
                # move along in word     
                current_coord = current_coord.safe_increment()

        else:  # just flip the board to run the algorithm
            return self.flip().score_move(move.flip())

        if word_added:  # remove the word after done scoring it
            self.remove_move(move)
            pass

        return total_score

    def play_move(self, move):
        """Adds the word to the board and returns the score"""
        self.add_move(move)
        return self.score_move(move)

    def is_move_present(self, move):
        """Returns True if the move is present and False otherwise"""
        #print("is_move_present called")
        coordinate = move.get_coord()
        current_coord = coordinate
        
        for tile in move:
            #print("Testing tile {} against board space {}".format(self.get_tile(current_coord), tile))
            if self.get_tile(current_coord) != tile:
                return False
            current_coord = current_coord.safe_increment()
        return True

    def flip(self):
        """
        Returns a new Board with horizontal and vertical switched, like
        a reflection over the line from A1 to O15"""
        new_board = Board()
        for i in range(15):
            for j in range(15):
                coord = coordinate_module.Coordinate(i, j, 0)
                # direction doesn't matter
                tile = self.get_tile(coord)
                new_board.add_tile(tile, coord.flip())
        return new_board


################################################
# The following provides support for iteration #
# and the immutable container protocol         #
################################################

    def __len__(self):
        return len(self.__tiles)

    def __iter__(self):
        return iter(self.__tiles)

    def __reversed__(self):
        return reversed(self.__tiles)