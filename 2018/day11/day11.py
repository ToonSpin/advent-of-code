import fileinput

for line in fileinput.input():
    input = int(line.rstrip())


def getPowerLevel(x, y):
    powerLevel = (x + 10) * y
    powerLevel += input
    powerLevel *= x + 10
    powerLevel = (powerLevel // 100) % 10 - 5
    return powerLevel


memo = {}

def getTotalPowerLevelInSquare(p, q, size):
    if size not in memo:
        memo[size] = {}
    if size - 3 in memo:
        del memo[size - 3]

    if size - 2 in memo:
        total = memo[size - 1][(p, q)] + memo[size - 1][(p + 1, q + 1)] - memo[size - 2][(p + 1, q + 1)]
        total += getPowerLevel(p + size - 1, q)
        total += getPowerLevel(p, q + size - 1)
    else:
        total = 0
        for x in range(p, p + size):
            for y in range(q, q + size):
                total += getPowerLevel(x, y)

    memo[size][(p, q)] = total
    return total


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
