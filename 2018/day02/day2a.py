import fileinput

input = []
for line in fileinput.input():
    input.append(line.rstrip())

twoCount = 0
threeCount = 0

for id in input:
    letters = list(id)
    letters.sort()

    foundThree = False
    foundTwo = False

    currentLetter = None
    currentCount = 0

    for letter in letters:
        if foundTwo and foundThree:
            break

        while currentCount > 3 and currentLetter == letter:
            continue

        if currentLetter != letter:
            if currentCount == 2:
                foundTwo = True
            currentLetter = letter
            currentCount = 0
        currentCount += 1

        if currentCount == 3:
            foundThree = True

    # does not trigger in the loop if the two count is at the end: check again
    if currentCount == 2:
        foundTwo = True

    if foundTwo:
        twoCount += 1
    if foundThree:
        threeCount += 1

print("Checksum: ", twoCount * threeCount)
