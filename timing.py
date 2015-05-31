from timeit import Timer

timeit1 = Timer(stmt="aapm('R*R', 'LITERARY')", setup="from wordtools import anagram_and_pattern_match as aapm")
timeit2 = Timer(stmt="slow_aapm('R*R', 'LITERARY')", setup="from wordtools import slow_aapm")

