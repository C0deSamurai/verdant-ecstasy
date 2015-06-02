"""
This file defines some convenience functions that may be moved to the board
file or some other file and provides a harness for testing Scrabble.
Intended to be run as a file in the interpreter
"""

from board import *
from constants import *
from coordinate import *
from move import Move
import squarebysquaremovefinder
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

test_board = 0
test_move_finder = 1

if test_board:
    play_word(b, "HARPING")
    play_word(b, "ZAX", "9G")
    play_word(b, "SEQUINS", "10H")
    play_word(b, "GARNETS", "11C")
    play_word(b, "(N)ATURE", "M10")

    print("The board after these plays:\n")
    print(b)

if test_move_finder:
    s = squarebysquaremovefinder
    play_word(b, "MANTEAU", "H8")
    word = "PORTMANTEAUX"
    row = (
            [[Tile(x) for x in word]] * 7 +
            [Tile(x) for x in "MANTEAU"] +
            [[Tile(x) for x in word]] * 1
            )
    index = 7
    col = 3
    print('\n'.join([str(x) for x in row]))
    print(s.create_move(word, index, col, row, b))
