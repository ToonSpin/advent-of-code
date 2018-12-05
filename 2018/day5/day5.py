import fileinput

for line in fileinput.input():
    input  = line


def getLengthAfterReaction(polymer):
    foundPair = True

    while foundPair:
        foundPair = False
        position = 0
        currentUnit = polymer[0]
        polymerAfterReaction = []
        polymerLength = len(polymer)

        while position < polymerLength:
            currentUnit = polymer[position]

            if position == polymerLength - 1:
                nextUnit = -1
            else:
                nextUnit = polymer[position + 1]

            if abs(nextUnit - currentUnit) == 32:
                foundPair = True
                position += 2
                continue

            polymerAfterReaction.append(currentUnit)

            currentUnit = nextUnit
            position += 1

        polymer = polymerAfterReaction

    return len(polymer)

polymer = [ord(c) for c in input]
print("Length after reaction: ", getLengthAfterReaction(polymer))

for unit in [ord(c) for c in list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")]:
    strippedPolymer = [c for c in polymer if c != unit and c != unit + 32]
    print("Length after reaction after stripping %c: %d" % (chr(unit), getLengthAfterReaction(strippedPolymer)))
