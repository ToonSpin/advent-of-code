import fileinput

for line in fileinput.input():
    input = int(line.rstrip())


memo = {}

def getTotalPowerLevelInSquare(p, q, size):
    if (p, q, size - 2) in memo:
        total = memo[(p, q, size - 1)] + memo[(p + 1, q + 1, size - 1)] - memo[(p + 1, q + 1, size - 2)]
        total += powerLevels[(p + size - 1, q)]
        total += powerLevels[(p, q + size - 1)]
    else:
        total = 0
        for x in range(p, p + size):
            for y in range(q, q + size):
                total += powerLevels[(x, y)]

    memo[(p, q, size)] = total
    return total


powerLevels = {(x, y): 0 for x in range(1, 301) for y in range(1, 301)}

for x in range(1, 301):
    for y in range(1, 301):
        powerLevel = (x + 10) * y
        powerLevel += input
        powerLevel *= x + 10
        powerLevel = (powerLevel // 100) % 10 - 5
        powerLevels[(x, y)] = powerLevel


mostPowerfulSquares = []

for size in range(1, 301):
    maxPowerLevel = getTotalPowerLevelInSquare(1, 1, size)
    mostPowerfulSquare = (1, 1, size, maxPowerLevel)

    for y in range(1, 301 - size + 1):
        for x in range(1, 301 - size + 1):
            totalPowerLevel = getTotalPowerLevelInSquare(x, y, size)

            if totalPowerLevel > maxPowerLevel:
                mostPowerfulSquare = (x, y, size, totalPowerLevel)
                maxPowerLevel = totalPowerLevel

    mostPowerfulSquares.append(mostPowerfulSquare)


x, y, r, p = mostPowerfulSquares[2]
print("the X,Y identifier of the 3 x 3 square with the largest total power is: %d,%d" % (x, y))

mostPowerfulSquareOfAnySize = sorted(mostPowerfulSquares, key=lambda square: square[3], reverse=True)[0]
x, y, r, p = mostPowerfulSquareOfAnySize
print("The X,Y,size identifier of the square with the largest total power is: %d,%d,%d" % (x, y, r))
