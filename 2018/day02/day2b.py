import fileinput
import sys

input = []
for line in fileinput.input():
    input.append(line.rstrip())

def stringsDifferInOnePlace(a, b):
    a = list(a)
    b = list(b)
    l = range(len(a))
    foundDifferingCharacter = False
    for i in l:
        if a[i] != b[i]:
            if foundDifferingCharacter:
                return False
            foundDifferingCharacter = True
    return foundDifferingCharacter

def getSimilarCharacters(a, b):
    output = ""
    a = list(a)
    b = list(b)
    return "".join([a[i] for i in range(len(a)) if a[i] == b[i]])

for a in input:
    for b in input:
        if stringsDifferInOnePlace(a, b):
            print(getSimilarCharacters(a, b))
            sys.exit(0)
