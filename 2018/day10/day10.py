import fileinput, re

lightRegex = re.compile("position=< *(-?\\d+), *(-?\\d+)> velocity=< *(-?\\d+), *(-?\\d+)>")
input = []

for line in fileinput.input():
    line = line.rstrip()
    light = lightRegex.match(line).groups()
    light = [int(s) for s in light]
    input.append(light)

numSeconds = 0

while True:
    numSeconds += 1

    minRows = maxRows = input[0][1]
    minColumns = maxColumns = input[0][0]

    for i, light in enumerate(input):
        px, py, vx, vy = light

        px += vx
        py += vy

        input[i] = [px, py, vx, vy]

        minRows = min(minRows, py)
        minColumns = min(minColumns, px)
        maxRows = max(maxRows, py)
        maxColumns = max(maxColumns, px)

    if maxRows - minRows <= 10:
        break

matrix = [["  " for x in range(minColumns, maxColumns + 1)] for y in range(minRows, maxRows + 1)]
for px, py, vx, vy in input:
    matrix[py - minRows][px - minColumns] = "##"

for row in matrix:
    print("".join(row))

print()

print("Message appeared after %d seconds." % (numSeconds))
