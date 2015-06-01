from timeit import Timer

timeit1 = Timer(stmt="a('???SATINE')", setup="from wordtools import anagram as a")
timeit2 = Timer(stmt="a('????SATINE')", setup="from wordtools import anagram as a")
timeit3 = Timer(stmt="a('?????SATINE')", setup="from wordtools import anagram as a")

print(timeit1.repeat(3, number=3))
print(timeit2.repeat(3, number=3))
print(timeit3.repeat(3, number=3))

print("Dunzo!")