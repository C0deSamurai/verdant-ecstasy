"""
This class provides functions to work with strings that are oriented
towards Scrabble: hooks, subanagrams, pattern matches, etc.
"""

import base_anagram
import wordlist
from constants import ALPHABET


"""
******************************************************************************
ALL of these functions take ? as a blank. Some take * as any number of blanks.
******************************************************************************
"""

def powerset(lst):
    """Returns every subset of every size of the list"""
    result = [[]]
    for x in lst:
        result.extend([subset + [x] for subset in result])
    return result

def back_hooks(word):
    """
    Returns a list of every word created by adding a letter after
    this one, e.g., "RATE" -> ["RATED", "RATEL", "RATER", "RATES"]
    """
    hooks = []
    if '?' in word:
        for letter in ALPHABET:
            hooks += back_hooks(word.replace('?', letter, 1))
    else:
        for letter in ALPHABET:
            if wordlist.check_validity(word + letter):
                hooks.append(word + letter)
    return hooks

def front_hooks(word):
    """
    Returns a list of every word created by adding a letter in front of
    this one, e.g., "EARN" -> ["LEARN", "YEARN"]
    """
    hooks = []
    if '?' in word:
        for letter in ALPHABET:
            hooks += front_hooks(word.replace('?', letter, 1))
    else:
        for letter in ALPHABET:
            if wordlist.check_validity(letter + word):
                hooks.append(letter + word)
    return hooks

def subanagrams(word):
    """
    Returns every word that can be made with the combination of any of the
    letters inside the word. Example:
    "MOCK" -> ["MOCK", "MOC", "MO", "OM"]
    """
    subs = []
    if '?' in word:
        for letter in ALPHABET:
            subs += subanagrams(word.replace('?', letter, 1))
    else:
        for subset in powerset(word):  # gets every subset
            subs += anagram(''.join(subset))
    return subs

def anagram(word):
    """
    Anagrams a word, including blanks represented by '?':
    Example:
    "AEIRSTX?" -> "MATRIXES", "SEXTARII"
    """
    if '?' in word:  # blank needs to be replaced
        anagrams = []  # to store all the anagrams
        for letter in ALPHABET:
            anagrams += anagram(word.replace('?', letter, 1))
        return list(set(anagrams))  # remove repeats with the same set of blanks
    else:
        return base_anagram.anagram_without_blanks(word)

def pattern_match(pattern):
    """
    Matches an exact pattern, with ? representing a single blank letter
    and * representing any number (even 0) of any tile. Examples:
    "C?RN" -> ["CARN", "CORN", "CURN"]
    "*NJUNCTION" -> ["CONJUNCTION", "INJUNCTION"]
    """
    q_mark_regex = "[A-Z]"  # matches exactly one letter
    
    asterisk_regex = "[A-Z]*"  # matches any number of letters
    
    search_regex = pattern.replace('?', q_mark_regex)
    search_regex = search_regex.replace('*', asterisk_regex)
    return wordlist.regex_search(search_regex)

def anagram_and_pattern_match(pattern, tileset):
    """
    Finds all anagrams of the tileset that match the pattern.
    Examples:
    "S*A", "SATINES" -> "SESTINA"
    "D*", "SATIRED" -> "DISRATE", "DIASTER", "DIASTRE"
    Faster than simply doing both computations and taking the intersection.
    """
    if '?' in tileset:  # need to do a recursive search with blanks
        sols = []  # to count solutions
        for letter in ALPHABET:
            sols += anagram_and_pattern_match(pattern,
                                                tileset.replace('?', letter, 1))
        return sols
    
    
    letter_regex = '[' + ''.join(tileset) + ']'  # matches a letter 
       
    asterisk_regex = letter_regex + '*'  # matches any number of letters
    
    search_regex = pattern.replace('?', letter_regex)
    search_regex = search_regex.replace('*', asterisk_regex)
    
    return [x for x in wordlist.regex_search(search_regex) if x in
                anagram(tileset)]

def subanagram_and_pattern_match(pattern, tileset):
    """Quickly f inds all subanagrams of the tileset that match the pattern.
    Can be slow with blanks in the tileset."""
    if '?' in tileset:  # need to do a recursive search with blanks
        sols = []  # to count solutions
        for letter in ALPHABET:
            sols += subanagram_and_pattern_match(pattern,
                                                tileset.replace('?', letter, 1))
        return sols
    
    
    letter_regex = '[' + ''.join(tileset) + ']'  # matches a letter 
       
    asterisk_regex = letter_regex + '*'  # matches any number of letters
    
    search_regex = pattern.replace('?', letter_regex)
    search_regex = search_regex.replace('*', asterisk_regex)
    
    return [x for x in wordlist.regex_search(search_regex) if x in
                subanagrams(tileset)]
