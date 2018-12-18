import fileinput

input = [line.rstrip() for line in fileinput.input()]

width = len(input[0])
height = len(input)

input = [' ' + line + ' ' for line in input]
emptyRow = ''.join([' ' for i in range(width + 2)])

input.insert(0, emptyRow)
input.append(emptyRow)


def getStringFromInput():
    return ''.join([input[q][p] for q in range(1, height + 1) for p in range(1, width + 1)])


def getResourceValueFromInput():
    acres = [input[q][p] for q in range(1, height + 1) for p in range(1, width + 1)]

    numTrees = len([acre for acre in acres if acre == '|'])
    numLumberyards = len([acre for acre in acres if acre == '#'])

    return numTrees * numLumberyards


def getEnvironment(x, y):
    x += 1
    y += 1

    vicinity = [input[q][p] for p in range(x-1, x+2) for q in range(y-1, y+2) if (p,q) != (x,y)]

    environment = {
        '.': len([acre for acre in vicinity if acre == '.']),
        '|': len([acre for acre in vicinity if acre == '|']),
        '#': len([acre for acre in vicinity if acre == '#']),
    }

    return environment


def getNewCell(p, q):
    environment = getEnvironment(p - 1, q - 1)

    if input[q][p] == '.' and environment['|'] >= 3:
        return '|'
    if input[q][p] == '|' and environment['#'] >= 3:
        return '#'
    if input[q][p] == '#':
        if environment['#'] == 0 or environment['|'] == 0:
            return '.'

    return input[q][p]


def doStep():
    newInput = [emptyRow]

    for q in range(1, height + 1):
        newRow = ' '
        for p in range(1, width + 1):
            newRow += getNewCell(q, p)
        newInput.append(newRow + ' ')

    newInput.append(emptyRow)
    return newInput


inputs = [getStringFromInput()]
resourceValues = [getResourceValueFromInput()]

i = 0
index = None
cycleLength = 0

while index == None:
    input = doStep()
    i += 1

    newInput = getStringFromInput()

    if newInput in inputs:
        index = inputs.index(newInput)
        cycleLength = i - index
        done = True

    inputs.append(newInput)
    resourceValues.append(getResourceValueFromInput())


print("Resource value after ten steps:", resourceValues[10])
print("Resource value after one billion steps:", resourceValues[(1000000000 - index) % cycleLength + index])
