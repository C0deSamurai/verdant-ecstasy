"""
This file details some basic constants: the normal Scrabble bonus square
layout and the tile values and counts in a normal bag.
It also provides a list of all the normal regulation tiles to use
in a bag and a list of every letter in the alphabet and '?'.
"""

from string import ascii_uppercase
import tile as tile_mod

ALPHABET = ascii_uppercase
ALPHABET_WITH_Q_MARK = ascii_uppercase + "?"

# ID's for each bonus square type, NON is a normal square

NON, DLS, DWS, TLS, TWS = 0, 1, 2, 3, 4

BOARD_LAYOUT = [
    [TWS, NON, NON, DLS, NON, NON, NON, TWS, NON, NON, NON, DLS, NON, NON, TWS],
    [NON, DWS, NON, NON, NON, TLS, NON, NON, NON, TLS, NON, NON, NON, DWS, NON],
    [NON, NON, DWS, NON, NON, NON, DLS, NON, DLS, NON, NON, NON, DWS, NON, NON],
    [DLS, NON, NON, DWS, NON, NON, NON, DLS, NON, NON, NON, DWS, NON, NON, DLS],
    [NON, NON, NON, NON, DWS, NON, NON, NON, NON, NON, DWS, NON, NON, NON, NON],
    [NON, TLS, NON, NON, NON, TLS, NON, NON, NON, TLS, NON, NON, NON, TLS, NON],
    [NON, NON, DLS, NON, NON, NON, DLS, NON, DLS, NON, NON, NON, DLS, NON, NON],
    [TWS, NON, NON, DLS, NON, NON, NON, DWS, NON, NON, NON, DLS, NON, NON, TWS],
    [NON, NON, DLS, NON, NON, NON, DLS, NON, DLS, NON, NON, NON, DLS, NON, NON],
    [NON, TLS, NON, NON, NON, TLS, NON, NON, NON, TLS, NON, NON, NON, TLS, NON],
    [NON, NON, NON, NON, DWS, NON, NON, NON, NON, NON, DWS, NON, NON, NON, NON],
    [DLS, NON, NON, DWS, NON, NON, NON, DLS, NON, NON, NON, DWS, NON, NON, DLS],
    [NON, NON, DWS, NON, NON, NON, DLS, NON, DLS, NON, NON, NON, DWS, NON, NON],
    [NON, DWS, NON, NON, NON, TLS, NON, NON, NON, TLS, NON, NON, NON, DWS, NON],
    [TWS, NON, NON, DLS, NON, NON, NON, TWS, NON, NON, NON, DLS, NON, NON, TWS],
]

TILE_VALUES = {}

# initialize tile values

for zero_point_letter in "?":
    TILE_VALUES[zero_point_letter] = 0

for one_point_letter in "AEIOULNSTR":
    TILE_VALUES[one_point_letter] = 1

for two_point_letter in "DG":
    TILE_VALUES[two_point_letter] = 2

for three_point_letter in "BCMP":
    TILE_VALUES[three_point_letter] = 3

for four_point_letter in "FHVWY":
    TILE_VALUES[four_point_letter] = 4

for five_point_letter in "K":
    TILE_VALUES[five_point_letter] = 5

for eight_point_letter in "JX":
    TILE_VALUES[eight_point_letter] = 8

for ten_point_letter in "QZ":
    TILE_VALUES[ten_point_letter] = 10

TILE_COUNTS = {}

# initialize tile counts

for one_count_letter in "KJQXZ":
    TILE_COUNTS[one_count_letter] = 1

for two_count_letter in "BCMPFHVWY?":
    TILE_COUNTS[two_count_letter] = 2

for three_count_letter in "G":
    TILE_COUNTS[three_count_letter] = 3

for four_count_letter in "LSUD":
    TILE_COUNTS[four_count_letter] = 4

for six_count_letter in "NRT":
    TILE_COUNTS[six_count_letter] = 6

for eight_count_letter in "O":
    TILE_COUNTS[eight_count_letter] = 8

for nine_count_letter in "AI":
    TILE_COUNTS[nine_count_letter] = 9

for twelve_count_letter in "E":
    TILE_COUNTS[twelve_count_letter] = 12

TILE_BAG = []

# add tiles based on previous distribution

def make_unique(iterable):
    """Used to remove duplicates from lists with unhashable elements"""
    unique_list = []
    for element in iterable:
        if element not in unique_list:
            unique_list.append(element)
        else:
            continue
    return unique_list

for tile in ALPHABET:
    for i in range(TILE_COUNTS[tile]):
        TILE_BAG.append(tile_mod.Tile(tile))

TILE_BAG_WITH_BLANK = []

for tile in ALPHABET_WITH_Q_MARK:
    for i in range(TILE_COUNTS[tile]):
        TILE_BAG_WITH_BLANK.append(tile_mod.Tile(tile))

TILE_LIST = make_unique(TILE_BAG)

TILE_LIST_WITH_BLANK = make_unique(TILE_BAG)