"""
This file creates the Coordinate class for dealing with Scrabble
coordinates. It provides an interface between the A7 notation
and array indices and direction. Note that A8 means the left-middle
TWS square and a word going horizontally, but 8A means a word going from
that square going vertically. Also note that A-O signifies column and
1-15 signifies row.
"""

HORIZONTAL, VERTICAL = 0, 1  # for representing direction
LETTERS = "ABCDEFGHIJKLMNO"  # for translating between A-O and 0-14


class Coordinate:
    """
    A class for dealing with Scrabble coordinates, with interface
    between the array indices used for programming and the A8 notation
    used for Scrabble in the real world. See the file doc for information
    on how the A8 system works. Note that all operations with Coordinate
    return new coordinates instead of changing the existing one.
    """

    def __init__(self, col, row, direction):
        """
        Takes two integers col and row from 0-14 that signify
        column and row respectively, and direction that is either
        horizontal (0) or vertical (1).
        """
        if not (0 <= col <= 14 and
                0 <= row <= 14 and
                0 <= direction <= 1):  # invalid coordinate
            raise ValueError("Coordinate values out of bounds")

        self.__col = col
        self.__row = row
        self.__direction = direction

    @classmethod
    def initialize_from_string(cls, coord_string):
        """
        Takes one string of the form letter + number or number + letter,
        between A-O and 1-15, like "O15" or "8A", with letter signifying
        column and number signifying row, and returns a Coordinate.
        """
        if coord_string[0] in LETTERS:  # signifies vertical direction
            direction = VERTICAL
            col = LETTERS.find(coord_string[0])
            row = int(coord_string[1:])
        else:
            direction = HORIZONTAL
            col = LETTERS.find(coord_string[-1])
            # if invalid letter was passed, this will raise ValueError
            try:
                row = int(coord_string[:-1])
            except ValueError:
                raise ValueError("Invalid letter value or improper syntax")

        try:
            return cls(col, row-1, direction)

        except (TypeError, ValueError):  # bad coordinates
            raise ValueError("Coordinate values out of bounds")
        # account for difference in 0-14 vs 1-15 numbering with row-1

    def is_horizontal(self):
        """Returns True if horizontal and False otherwise."""
        return self.__direction is HORIZONTAL

    def get_col(self):
        """Returns the column value from 0-14"""
        return self.__col

    def get_row(self):
        """Returns the row value from 0-14"""
        return self.__row

    def flip(self):
        """
        Returns the Coordinate with reversed direction and row-column
        "A7" -> "1G"
        "9F" -> "I6"
        """
        return Coordinate(self.__row, self.__col, 1 - self.__direction)
        
    
    def increment(self):
        """
        Returns a new Coordinate moved one step in the direction of the
        coordinate and the same direction as self, e.g., A8 -> A9, 8A -> 8B.
        Returns ValueError if the new coordinate would be invalid.
        """
        try:
            if self.__direction is HORIZONTAL:
                return Coordinate(self.__col + 1, self.__row, self.__direction)
            else:
                return Coordinate(self.__col, self.__row + 1, self.__direction)
        except ValueError:
            raise ValueError("Incremented coordinate from" +
                                " {} out of bounds!".format(str(self)))

    def safe_increment(self):
        """
        Like Increment, but returns None instead of raising ValueError
        """
        try:
            if self.__direction is HORIZONTAL:
                return Coordinate(self.__col + 1, self.__row, self.__direction)
            else:
                return Coordinate(self.__col, self.__row + 1, self.__direction)
        except ValueError:
            return None

    def __repr__(self):
        """Returns human-readable coordinate output."""
        if self.is_horizontal():
            return str(self.__row + 1) + LETTERS[self.__col]
        else:
            return LETTERS[self.__col] + str(self.__row + 1)

    def __str__(self):
        """
        Returns human-readable coordinate output.
        >>> str(Coordinate(0, 7, 0))
        "8A"
        >>> str(Coordinate.initialize_from_string("8A"))
        "A8"
        """
        if self.is_horizontal():
            return str(self.__row + 1) + LETTERS[self.__col]
        else:
            return LETTERS[self.__col] + str(self.__row + 1)

    def move_up(self):
        """
        Returns the Coordinate moved up by 1 space, throws ValueError if
        the coordinate is out of bounds. Keeps the current direction.
        """
        try:
            return Coordinate(self.__col, self.__row - 1, self.__direction)
        except ValueError:
            return ValueError("Moved a Coordinate past the first row!")

    def move_down(self):
        """
        Returns the Coordinate moved down by 1 space, throws ValueError if
        the coordinate is out of bounds. Keeps the current direction.
        """
        try:
            return Coordinate(self.__col, self.__row + 1, self.__direction)
        except ValueError:
            return ValueError("Moved a Coordinate past the last row!")

    def move_right(self):
        """
        Returns the Coordinate moved right by 1 space, throws ValueError if
        the coordinate is out of bounds. Keeps the current direction.
        """
        try:
            return Coordinate(self.__col + 1, self.__row, self.__direction)
        except ValueError:
            return ValueError("Moved a Coordinate past the last column!")

    def move_left(self):
        """
        Returns the Coordinate moved left by 1 space, throws ValueError if
        the coordinate is out of bounds. Keeps the current direction.
        """
        try:
            return Coordinate(self.__col - 1, self.__row, self.__direction)
        except ValueError:
            return ValueError("Moved a Coordinate past the first column!")

    def safe_move_up(self):
        """
        Moves the coordinate up, but returns None instead of
        raising ValueError.
        """
        try:
            return Coordinate(self.__col, self.__row - 1, self.__direction)
        except ValueError:
            return None

    def safe_move_down(self):
        """
        Moves the coordinate down, but returns None instead of
        raising ValueError.
        """
        try:
            return Coordinate(self.__col, self.__row + 1, self.__direction)
        except ValueError:
            return None

    def safe_move_left(self):
        """
        Moves the coordinate left, but returns None instead of
        raising ValueError.
        """
        try:
            return Coordinate(self.__col - 1, self.__row, self.__direction)
        except ValueError:
            return None

    def safe_move_right(self):
        """
        Moves the coordinate right, but returns None instead of
        raising ValueError.
        """
        try:
            return Coordinate(self.__col + 1, self.__row, self.__direction)
        except ValueError:
            return None
