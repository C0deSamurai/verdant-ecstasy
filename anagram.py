"""
This program provides a way of anagramming words very quickly by using
an anagram dictionary. The way this works is by assigning each letter
of the alphabet a prime number (lower prime means more common letter).
Then every set of letters corresponds to a unique number, the product
of each letter's prime in the set. Then this product is precomputed for
every word in the lexicon. Then, anagramming sets of letters is as easy
as looking up the prime product in the anagram table and seeing what words
there are. For example, let's say we want to anagram AET. E has value 2,
T has value 3, and A has value 5, so the product is 2 * 3 * 5 = 30. Then,
we look up what words also have that product: TEA, TAE, EAT, ATE, and ETA.

This file automatically checks for the existence of the necessary
files required for its work and creates them if needed.
"""

from wordlist import wordlist  # the OWL3
from os.path import exists  

# letters are sorted by commonness to keep the products small

LETTER_TO_PRIME = {'e': 2, 't': 3, 'a': 5, 'o': 7, 'i': 11, 'n': 13, 's': 17,
                        'h': 19, 'r': 23, 'd': 29, 'l': 31, 'c': 37, 'u': 41,
                        'm': 43, 'w': 47, 'f': 53, 'g': 59, 'y': 61, 'p': 67,
                        'b': 71, 'v': 73, 'k': 79, 'j': 83, 'x': 89, 'q': 97,
                        'z': 101}

ANAGRAM_DICT_FILENAME = "anagramdictionary.txt"  # to store the dictionary


def number_from_word(string_iterable):
    """Multiplies the value of each letter by each other to produce a
    unique number."""
    product = 1
    for letter in string_iterable:
        product *= LETTER_TO_PRIME[letter.lower()]

    return product


def create_anagram_dictionary(lexicon=wordlist):
    """This function creates the anagram dictionary in RAM and returns it."""
    anagram_dict = {}  # from numbers to list of words

    for word in lexicon:
        product = number_from_word(word)
        if product in anagram_dict:  # word has an anagram already
            # add to existing list if applicable
            anagram_dict[product].append(word)
        else:  # word has no anagrams
            anagram_dict[product] = [word]
    return anagram_dict

"""
The format for the anagram dictionary when it's stored in a .txt file is
as follows: every number is first, followed by a space, followed by the string
"->", followed by a space, followed by any words with spaces between them.
Example excerpt (order ignored)
202 -> ZA
157333990 -> CLAIMED CAMELID DECLAIM DECIMAL MEDICAL
"""


def write_anagram_dictionary_to_file(filename=ANAGRAM_DICT_FILENAME,
                                        lexicon=wordlist):
    """This function writes the anagram dictionary to the specified
    filename with the specified lexicon in the format specified above.
    Returns None."""
    anagram_dict = create_anagram_dictionary(lexicon)

    file = open(filename, "w")
    file.write("\n")  # opening blank line
    for number in anagram_dict:
        line_string = "{} -> {}\n".format(
            number, ' '.join(anagram_dict[number])
        )
        file.write(line_string)


def create_anagram_dictionary_from_file(filename=ANAGRAM_DICT_FILENAME):
    """Returns an anagram dictionary in memory from parsing the file."""
    file = open(filename)

    anagram_dict = {}

    for line in list(file)[1:]:
        line = line.split()  # split by whitespace
        number = int(line[0])  # get the number
        anagram_dict[number] = line[2:]  # ignore the "->" element

    return anagram_dict


def anagram(word):
    """Anagrams a word in O(n) time using a table lookup.
    Assumes that the file at ANAGRAM_DICT_FILENAME is operational.
    """
    try:
        return anagram_dictionary[number_from_word(word)]
    except KeyError:
        return []

#  see if the necessary things are in place and if not, create them

try:
    anagram("TheCodeSamurai")
except (NameError, KeyError):
    if exists(ANAGRAM_DICT_FILENAME):
        write_anagram_dictionary_to_file()
    anagram_dictionary = create_anagram_dictionary_from_file()