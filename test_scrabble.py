"""
This file defines some convenience functions that may be moved to the board
file or some other file and provides a harness for testing Scrabble.
Intended to be run as a file in the interpreter
"""

from board import *
from constants import *
from coordinate import *
from tile import *

init = Coordinate.initialize_from_string


def play_word(board, wordstring, wordcoord="8H"):
    """Convenience function that takes a given Board, a given string that is
    the word to play, and a string for the coordinate, and returns the score."""
    word = []
    for letter in wordstring:
        word.append(Tile(letter) if letter != " " else None)
    coord = Coordinate.initialize_from_string(wordcoord)
    print("{} was counted for {} points".format(wordstring,
        board.count_word(word, coord)))
    print("{} was played for {}".format(
            "".join([str(t) for t in word]), board.play_word(word, coord)))


b = Board()
c = Coordinate.initialize_from_string("9G")
play_word(b, "HARPING")
play_word(b, "ZAX", "9G")
play_word(b, "SEQUINS", "10H")
play_word(b, "GARNETS", "11C")
play_word(b, " ATURE", "M10")