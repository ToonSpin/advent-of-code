import fileinput

input = [line.rstrip() for line in fileinput.input()]

minX = 10000
maxX = 0
minY = 10000
maxY = 0

field = []
veins = []

for row in input:
    vein = sorted(row.split(', '))

    vein[0] = list(map(int, vein[0][2:].split('..')))
    vein[1] = list(map(int, vein[1][2:].split('..')))

    minX = min(min(vein[0]), minX)
    maxX = max(min(vein[0]), maxX)

    minY = min(min(vein[1]), minY)
    maxY = max(min(vein[1]), maxY)

    if len(vein[0]) == 1:
        vein[0].append(vein[0][0])

    if len(vein[1]) == 1:
        vein[1].append(vein[1][0])

    veins.append(vein)

minY -= 1
field = [['.' for x in range(minX, maxX + 1)] for y in range(minY, maxY + 1)]

for vein in veins:
    x1, x2 = vein[0]
    y1, y2 = vein[1]

    for y in range(y1, y2 + 1):
        for x in range(x1, x2 + 1):
            field[y - minY][x - minX] = '#'

def dropDown(x, y):
    while field[y][x] in ('|', '.'):
        field[y][x] = '|'
        y += 1
    return (x, y - 1)

def isContainedRow(x, y):
    while field[y][x] in ['|', '.'] and field[y + 1][x] not in ['|', '.']:
        x -= 1
    if field[y][x] != '#' or field[y + 1][x] in ['|', '.']:
        return False
    x += 1
    while field[y][x] in ['|', '.'] and field[y + 1][x] not in ['|', '.']:
        x += 1
    if field[y][x] != '#' or field[y + 1][x] in ['|', '.']:
        return False
    return True

def overflowAndGetStreams(x, y):
    points = []
    while field[y][x] in ['|', '.'] and field[y + 1][x] not in ['|', '.']:
        field[y][x] = '|'
        x -= 1
    if field[y][x] != '#' and field[y + 1][x] in ['|', '.']:
        points.append((x, y))
    x += 1
    while field[y][x] in ['|', '.'] and field[y + 1][x] not in ['|', '.']:
        field[y][x] = '|'
        x += 1
    if field[y][x] != '#' and field[y + 1][x] in ['|', '.']:
        points.append((x, y))
    return points

def fillRow(x, y):
    while field[y][x] in ['|', '.']:
        x -= 1
    x += 1
    while field[y][x] in ['|', '.']:
        field[y][x] = '~'
        x += 1

def fillBasin(x, y):
    while isContainedRow(x, y):
        fillRow(x, y)
        y -= 1
    return overflowAndGetStreams(x, y)

memo = set()
def doRun(x, y):
    if (x,y) in memo:
        return

    memo.add((x, y))

    (x, y) = dropDown(x, y)
    nextPoints = fillBasin(x, y)

    for point in nextPoints:
        p, q = point
        try:
            doRun(p, q)
        except IndexError:
            pass

doRun(500 - minX, 0)

numFlowingWater = 0
numStagnantWater = 0

for row in field[1:]:
    numFlowingWater += len([tile for tile in row if tile == '|'])
    numStagnantWater += len([tile for tile in row if tile == '~'])

print("Number of tiles reachable by water:", numStagnantWater + numFlowingWater)
print("Number of water tilesleft after draining:", numStagnantWater)
