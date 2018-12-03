import fileinput, re

clothWidth = 1000
clothHeight = 1000

claimRegex = re.compile("^#(\\d+) @ (\\d+),(\\d+): (\\d+)x(\\d+)$")
input = []
for line in fileinput.input():
    line = line.rstrip()
    claim = claimRegex.match(line).groups()
    claim = [int(s) for s in claim]
    input.append(claim)

claimsPerRow = [[] for y in range(clothHeight)]
for claim in input:
    claimId, x, y, w, h = claim
    for i in range(y, y + h):
        claimsPerRow[i].append([x, x + w])

claimTallies = []
squaresWithMoreThanOneClaim = 0
for y, row in enumerate(claimsPerRow):
    newRow = [0 for i in range(clothWidth)]
    for claim in row:
        for i in range(claim[0], claim[1]):
            newRow[i] += 1
    squaresWithMoreThanOneClaim += sum([1 for i in newRow if i > 1])
    claimTallies.append(newRow)

print("Squares with more than one claim: ", squaresWithMoreThanOneClaim)

for claim in input:
    claimId, x, y, w, h = claim
    claimRows = claimTallies[y:y+h]
    claimTotals = [sum(row[x:x+w]) for row in claimRows]
    if sum(claimTotals) == w * h:
        print("Claim with no other claim overlapping it: ", claimId)
