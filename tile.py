"""
This file creates a Tile class that models a Scrabble tile. The type
of a Tile is a capital letter A-Z or ? for blanks. You can choose what a blank
is set to by calling set_face, but for non-blank tiles this will return
an error. Tiles are immutable and you should make a new Tile instead of
changing an existing one.

Note: blanks are sorted as after every other letter of the alphabet.
"""

import constants
from functools import total_ordering

@total_ordering
class Tile:
    """This class models a Scrabble tile."""
    def __init__(self, tile_type):
        "tile_type is a character A-Z or '?' for blanks"
        if tile_type not in constants.ALPHABET_WITH_Q_MARK:
            raise ValueError("tile_type must be in A-Z or '?'")
        self.__type = tile_type
        self.__face = tile_type  # represents the face of the tile
        self.__value = constants.TILE_VALUES[tile_type]

    def set_face(self, face):
        """
        face is a letter A-Z for the blank to be set to (used by str)
        If self's type is not '?', this will raise a TypeError.
        """
        # Note that ? is an acceptable face, representing a blank face.
        if face not in constants.ALPHABET_WITH_Q_MARK:
            raise ValueError("Face must be A-Z or '?'")
        self.__face = face
    
    def __repr__(self):
        """Returns the face of the tile, uppercase if normal, lower if blank"""
        if self.__type == '?':
            return self.__face.lower()
        else:
            return self.__face

    def __str__(self):
        """Returns the face of the tile, uppercase if normal, lower if blank"""
        if self.__type == '?':
            return self.__face.lower()
        else:
            return self.__face

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.__type == '?' and other.__type != '?':
            return False
        elif self.__type != '?' and other.__type == '?':
            return False
        else:
            return self.__face < other.__face

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return (self.__face == other.__face and self.__type == other.__type)
    
    def get_value(self):
        """Returns the point value of the tile"""
        return self.__value

    def is_blank(self):
        """Returns True if this is a blank and False otherwise."""
        return self.__type == '?'

