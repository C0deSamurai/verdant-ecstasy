"""
This file provides the MoveFinder class, which allows you to find any moves on a Scrabble
board. This class is an Abstract Base Class and is intended to be a Strategy pattern, as
there are different move-finding algorithms that can be used.
"""

from abc import *

class MoveFinder(ABC):
    """A class that models any algorithm that finds all the valid moves on a Scrabble board."""
    def __init__(self):
        """Nothing to instantiate!"""
        pass

    @staticmethod
    @abstractmethod
    def find_all_moves(tiles, board):
        """Finds every move on the board with the given tiles and returns a list of Moves."""
        raise NotImplementedError

