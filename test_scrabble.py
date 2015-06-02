"""
This file defines some convenience functions that may be moved to the board
file or some other file and provides a harness for testing Scrabble.
Intended to be run as a file in the interpreter
"""

from board import *
from constants import *
from coordinate import *
from move import Move
from tile import *




def play_word(board, wordstring, wordcoord="8H"):
    """Convenience function that takes a given Board, a given string that is
    the word to play, and a string for the coordinate, and returns the score."""
    move = Move(wordstring, wordcoord)
    score = board.play_move(move)
    print("{} was played for {} points".format(move, score))


b = Board()
c = Coordinate.initialize_from_string("9G")
init = Coordinate.initialize_from_string
play_word(b, "HARPING")
play_word(b, "ZAX", "9G")
play_word(b, "SEQUINS", "10H")
play_word(b, "GARNETS", "11C")
play_word(b, "(N)ATURE", "M10")

print("The board after these plays:\n")
print(b)