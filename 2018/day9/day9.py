import fileinput

for line in fileinput.input():
    input = line.split(" ")
    numPlayers = int(input[0])
    valueOfLastMarble = int(input[6])

class CircleNode:
    nextNode = None
    prevNode = None

    def __init__(self, value):
        self.value = value
        self.nextNode = self
        self.prevNode = self

    def getNodeAtOffset(self, offset):
        current = self
        while offset < 0:
            current = current.prevNode
            offset += 1
        while offset > 0:
            current = current.nextNode
            offset -= 1
        return current

    def eliminateNextNode(self):
        eliminatedNode = self.nextNode
        self.nextNode.nextNode.prevNode = self
        self.nextNode = self.nextNode.nextNode
        eliminatedNode.nextNode = None
        eliminatedNode.prevNode = None

    def insertValueAfter(self, value):
        newNode = CircleNode(value)

        newNode.nextNode = self.nextNode
        self.nextNode.prevNode = newNode

        newNode.prevNode = self
        self.nextNode = newNode

currentMarble = CircleNode(0)
scores = [0 for i in range(numPlayers)]
part1Done = False

turn = 1
while turn <= valueOfLastMarble * 100:
    if turn == valueOfLastMarble and not part1Done:
        print("Score of the winning elf:", max(scores))
        part1Done = True

    if turn % 23 == 0:
        scores[turn % numPlayers] += turn

        extraMarble = currentMarble.getNodeAtOffset(-7)
        scores[turn % numPlayers] += extraMarble.value

        currentMarble = extraMarble.prevNode
        currentMarble.eliminateNextNode()
        currentMarble = currentMarble.nextNode
    else:
        currentMarble = currentMarble.getNodeAtOffset(1)
        currentMarble.insertValueAfter(turn)
        currentMarble = currentMarble.nextNode

    turn += 1

print("Score of the winning elf if the winning marble were 100 times as large:", max(scores))
