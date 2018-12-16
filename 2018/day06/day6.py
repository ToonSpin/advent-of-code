import fileinput

width = height = 400
totalDistanceThreshold = 10000
input = []

for line in fileinput.input():
    x, y = line.rstrip().split(", ")
    input.append((int(x), int(y)))

nearDistanceCount = 0
pointCounts = [0 for point in input]
infinitePoints = set()

for y in range(height):
    for x in range(width):
        minDistance = 10000
        totalDistance = 0
        closestPoint = -1

        for i, point in enumerate(input):
            distance = abs(point[0] - x) + abs(point[1] - y)
            totalDistance += distance

            if distance == minDistance:
                closestPoint = -1
            elif distance < minDistance:
                minDistance = distance
                closestPoint = i

        if closestPoint > -1:
            pointCounts[closestPoint] += 1
            if y == 0 or y == height - 1 or x == 0 or x == width - 1:
                infinitePoints.add(closestPoint)

        if totalDistance < totalDistanceThreshold:
            nearDistanceCount += 1


pointCounts = [count for i, count in enumerate(pointCounts) if i not in infinitePoints]
print("Biggest area that isn't infinite:", max(pointCounts))

print("Size of region with total distance below %d: %d" % (totalDistanceThreshold, nearDistanceCount))
