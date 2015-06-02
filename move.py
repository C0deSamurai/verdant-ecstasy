"""
This file provides the Move class, which provides a unified interface
for dealing with moves in Scrabble. Note that score is in no way a
part of this class: it is the responsibility of the Board class (and maybe
later, a Game class or other such classes) to count score and keep track of it.

This class also provides a convenience function that takes a string and
returns a list of Tiles. Note that this is case-sensitive: 'f' represents
a blank that has been set to F (like in 'fAINTERS'), while 'F' represents
a normal F tile. This function can be called from Move if desired.
"""

from coordinate import Coordinate
from tile import Tile
import re

class Move():
    """
    A class for dealing with moves in Scrabble. Note that scoring moves
    is not this class's responsibility, but keeping track of tiles on the board
    vs. tiles from the rack is.
    
    Move syntax is as follows: 'F' denotes the F tile. 'f' denotes a blank
    tile played as an 'f'. (F) denotes an F on the board. (f) denotes a blank
    tile as an f already on the board. Example syntax:
    PORt(MANTEaU)X
    
    Note that this class is iterable: if you iterate over this, it will
    iterate over every tile in the move, including ones on the board.
    """

    def __init__(self, word, coord):
        """
        Initializes a Move with the given string (only alphabetic characters)
        and coordinate. Coord can either be a Coordinate or a string, which
        will be converted to a Coordinate. Word is a string, following the
        rules of the class doc: lowercase means blank, parentheses mean already
        played. Example: PORt(MANTEaU)X
        """
        
        tilelist = self.tiles_from_string(word)
        
        self.__all_tiles = tilelist[0]
        self.__just_played_tiles = tilelist[1]
        
        if isinstance(coord, str):
            self.__coord = Coordinate.initialize_from_string(coord)
        else:
            self.__coord = coord

    def to_string(self):
        """Returns just the move string in proper syntax."""
        string = ""

        for index, tile in enumerate(self):
            if self.__just_played_tiles[index] is None:  # tile already on board
                if string.count('(') > string.count(')'):  # one of many
                    string += str(tile)  # already a left paren
                else:  # need to add a left paren
                    string += '(' + str(tile)
            else:  # tile from rack
                # need to add a right paren
                if string.count('(') > string.count(')'):
                    string += ')' + str(tile)
                else:
                    string += str(tile)

        return string
    def __str__(self):
        """Returns a string in the syntax described in the class doc."""
        string = ""
        
        for index, tile in enumerate(self):
            if self.__just_played_tiles[index] is None:  # tile already on board
                if string.count('(') > string.count(')'):  # one of many
                    string += str(tile)  # already a left paren
                else:  # need to add a left paren
                    string += '(' + str(tile)
            else:  # tile from rack
                # need to add a right paren
                if string.count('(') > string.count(')'):  
                    string += ')' + str(tile)
                else:
                    string += str(tile)

        return str(self.__coord) + ' ' + string
    
    @classmethod
    def tiles_from_string(cls, word):
        """
        Takes a string, with blanks in lowercase and pre-played tiles
        in parentheses, and returns a list of two lists of tiles: the
        first with all the tiles, and the other with just the played ones
        and None where tiles are on the board.
        Example: PORt(MANtEAU)X
        """
        without_parens = word.replace('()', '')  # remove parentheses
        
        all_tiles = []
        just_played_tiles = []
        
        for index, tile in enumerate(without_parens):
            if tile in '()':  #  skip over these
                continue
            first_part = word[:index]
            if first_part.count('(') > first_part.count(')'):  # on board
                if tile.islower():  # a blank
                    blank = Tile('?')
                    blank.set_face(tile.upper())
    
                    all_tiles.append(blank)
                    just_played_tiles.append(None)  # mark spot
                else:
                    all_tiles.append(Tile(tile))
                    just_played_tiles.append(None)  # mark spot
            else:  # belongs in both
                if tile.islower():  # a blank
                    blank = Tile('?')
                    blank.set_face(tile.upper())
    
                    just_played_tiles.append(blank)
                    all_tiles.append(blank)
                else:
                    just_played_tiles.append(Tile(tile))
                    all_tiles.append(Tile(tile))

        return [all_tiles, just_played_tiles]

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return False
        return (self.__all_tiles == other.__all_tiles and
                    self.__just_played_tiles == other.__just_played_tiles and
                    self.__coord == other.__coord)

    def get_coord(self):
        return self.__coord
    
    def get_just_played_tiles(self):
        """
        Returns a list of tiles with None in spaces
        where the board already had the tile.
        """
        return self.__just_played_tiles

    def was_just_played(self, index):
        """
        Returns True if the tile at index was just played and False otherwise.
        """
        return self.__just_played_tiles[index] is not None

    def flip(self):
        """
        Returns the exact same Move with flipped coordinate.
        """
        return Move(self.to_string(), self.__coord.flip())
    #####################################################################
    # The immutable container and iterator protocols are defined below. #
    #####################################################################
    
    def __len__(self):
        return len(self.__all_tiles)

    def __iter__(self):
        return iter(self.__all_tiles)

    def __getitem__(self, index):
        return self.__all_tiles[index]
    
    def __reversed__(self):
        return reversed(self.__all_tiles)
