import fileinput

margin = 100

input = []
gotDepth = False
depth = None
target = None
for line in fileinput.input():
    if not gotDepth:
        depth = int(line.rstrip().split(': ')[1])
        gotDepth = True
    else:
        coordinates = line.rstrip().split(': ')[1]
        width, height = map(int, coordinates.split(','))
        target = (width, height)
        width += margin
        height += margin
        break

geologicIndices = {}

for x in range(width + 1):
    geologicIndices[(x, 0)] = 16807 * x

for y in range(height + 1):
    geologicIndices[(0, y)] = 48271 * y

erosionLevels = {point: (index + depth) % 20183 for point, index in geologicIndices.items()}
erosionLevels[target] = 0

def getErosionLevel(p, q):
    if (p, q) in erosionLevels:
        return erosionLevels[(p, q)]

    geologicIndex = 1
    geologicIndex *= erosionLevels[(p - 1, q)]
    geologicIndex *= erosionLevels[(p, q - 1)]

    erosionLevel = (geologicIndex + depth) % 20183

    geologicIndices[(p, q)] = geologicIndex
    erosionLevels[(p, q)] = erosionLevel

    return erosionLevel

totalRisk = 0
for y in range(target[1] + 1):
    for x in range(target[0] + 1):
        totalRisk += getErosionLevel(x, y) % 3

print("Total risk:", totalRisk)

# give terrain and disallowed tools the same value 
neither = rocky = 0
torch = wet = 1
climbingGear = narrow = 2

nodes = {}

class Node:
    def __init__(self, x, y, tool, nodeType, minimalPathLength):
        # see if having the tool in this node type is allowed
        assert(tool != nodeType)

        self.x = x
        self.y = y
        self.tool = tool
        self.nodeType = nodeType
        self.minimalPathLength = minimalPathLength
        self.neighbors = {}
        self.via = None

    def addNeighbor(self, node):
        # only move to adjacent nodes
        assert(abs(node.x - self.x) + abs(node.y - self.y) == 1)

        # if switching to the tool is not allowed, this node is inaccessible
        if self.nodeType == node.tool:
            return

        cost = 1
        if self.tool != node.tool:
            cost += 7

        self.neighbors[(node.x, node.y, node.tool)] = cost

    def getCoordinates(self):
        return (self.x, self.y, self.tool)

initialPathLength = (height + width) * 8 * 1000

for y in range(height):
    for x in range(width):
        nodeType = getErosionLevel(x, y) % 3
        for tool in [0, 1, 2]:
            if tool != nodeType:
                node = Node(x, y, tool, nodeType, initialPathLength)
                nodes[(x, y, tool)] = node

for y in range(height):
    for x in range(width):
        for tool in [0, 1, 2]:
            if (x, y, tool) in nodes:
                node = nodes[(x, y, tool)]
                for otherTool in [0, 1, 2]: 
                    if (x - 1, y, otherTool) in nodes:
                        node.addNeighbor(nodes[x - 1, y, otherTool])
                    if (x + 1, y, otherTool) in nodes:
                        node.addNeighbor(nodes[x + 1, y, otherTool])
                    if (x, y - 1, otherTool) in nodes:
                        node.addNeighbor(nodes[x, y - 1, otherTool])
                    if (x, y + 1, otherTool) in nodes:
                        node.addNeighbor(nodes[x, y + 1, otherTool])

targetNode = (target[0], target[1], torch)
visitedNodes = set()
nodes[(0, 0, torch)].minimalPathLength = 0
currentNodes = [(0, 0, torch)]

while currentNodes[0] != targetNode:
    currentCoordinates = currentNodes[0]
    currentNode = nodes[currentCoordinates]

    for neighborCoordinates, cost in currentNode.neighbors.items():
        neighbor = nodes[neighborCoordinates]
    
        if neighborCoordinates not in visitedNodes:
            if neighborCoordinates not in currentNodes:
                currentNodes.append(neighborCoordinates)
            
            if currentNode.minimalPathLength + cost < neighbor.minimalPathLength:
                neighbor.minimalPathLength = currentNode.minimalPathLength + cost
                neighbor.via = currentCoordinates

    visitedNodes.add(currentCoordinates)
    currentNodes = currentNodes[1:]
    currentNodes.sort(key=lambda coordinates: nodes[coordinates].minimalPathLength)

print("Shortest time to get to target:", currentNode.minimalPathLength)
