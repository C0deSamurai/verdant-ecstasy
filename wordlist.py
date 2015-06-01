"""
This file provides an easy interface to a list of dictionary words and
a tool for searching the dictionary with a regex and checking a word
for inclusion in the dictionary. Note that because of copyright issues,
the OWL2 is used.
"""

import os
from re import findall


FILENAME = "OWL2.txt"

dictionary = open(FILENAME)

wordlist = []
for word in dictionary:
    wordlist.append(word.strip())


def check_validity(word):
    return word.upper() in wordlist

dictionary.seek(0)
dict_string = dictionary.read()

def regex_search(regexp):
    """Searches the dictionary for a particular regular
    expression, whole words only"""
    return [w.strip() for w in findall('\n' + regexp + '\n', dict_string)]
