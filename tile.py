"""
This file creates a Tile class that models a Scrabble tile. The type
of a Tile is a capital letter A-Z or ? for blanks. You can choose what a blank
is set to by calling set_face, but for non-blank tiles this will return
an error. Tiles are immutable and you should make a new Tile instead of
changing an existing one.
"""

from constants import ALPHABET_WITH_Q_MARK  # with ? added
from constants import TILE_VALUES


class Tile:
    """This class models a Scrabble tile."""
    def __init__(self, tile_type):
        "tile_type is a character A-Z or '?' for blanks"
        if tile_type not in ALPHABET_WITH_Q_MARK:
            raise ValueError("tile_type must be in A-Z or '?'")
        self.__type = tile_type
        self.__face = tile_type  # represents the face of the tile
        self.__value = TILE_VALUES[tile_type]

    def set_face(self, face):
        """
        face is a letter A-Z for the blank to be set to (used by str)
        If self's type is not '?', this will raise a TypeError.
        """
        # Note that ? is an acceptable face, representing a blank face.
        if face not in ALPHABET_WITH_Q_MARK:
            raise ValueError("Face must be A-Z or '?'")
        self.__face = face
    
    def __repr__(self):
        """Returns the face of the tile"""
        return self.__face

    def __str__(self):
        """Returns the face of the tile"""
        return self.__face

    def get_value(self):
        """Returns the point value of the tile"""
        return self.__value
