import fileinput

input = []

for line in fileinput.input():
    input = line.rstrip().split(" ")
input = [int(s) for s in input]


class TreeNode:
    children = []
    metadata = []
    inputSize = 0

    @staticmethod
    def createTree(input):
        numMetadata = input[1]
        children = []
        inputOffset = 2

        for i in range(input[0]):
            child, childInputOffset = TreeNode.createTree(input[inputOffset:])
            children.append(child)
            inputOffset += childInputOffset

        tree = TreeNode(input[inputOffset:inputOffset + numMetadata])
        tree.children = children

        return (tree, inputOffset + numMetadata)

    def __init__(self, metadata):
        self.metadata = metadata

    def getValue(self):
        if len(self.children) == 0:
            return sum(self.metadata)

        sumOfValues = 0
        for reference in self.metadata:
            if reference <= len(self.children):
                sumOfValues += self.children[reference - 1].getValue()
        return sumOfValues

    def getDeepSumOfMetadata(self):
        return sum(self.metadata) + sum([child.getDeepSumOfMetadata() for child in self.children])


tree, inputSize = TreeNode.createTree(input)

print("Sum of all metadata:", tree.getDeepSumOfMetadata())
print("Value:", tree.getValue())
