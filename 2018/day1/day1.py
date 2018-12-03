import fileinput

input = []
for line in fileinput.input():
    input.append(int(line))

print("Sum:", sum(input))

frequenciesSeen = set()
currentFrequency = 0
currentChangeIndex = 0

while currentFrequency not in frequenciesSeen:
    frequenciesSeen.add(currentFrequency)
    currentFrequency += input[currentChangeIndex]
    currentChangeIndex = (currentChangeIndex + 1) % len(input)

print("First frequency to occur twice:", currentFrequency)
