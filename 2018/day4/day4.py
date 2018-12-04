import fileinput, re

regex = re.compile(r"^\[(\d+)-(\d+)-(\d+) (\d+):(\d+)\] (.*)$")
input = []
for line in fileinput.input():
    line = regex.match(line.rstrip())
    input.append(line)
input = sorted(input, key=lambda line: line.group(0))

minuteTalliesPerGuard = {}
for line in input:
    minute = int(line.group(5))
    words = line.group(6).split(" ")

    if words[1][0] == "#":
        currentGuard = int(words[1][1:])
        if currentGuard not in minuteTalliesPerGuard:
            minuteTalliesPerGuard[currentGuard] = [0 for i in range(60)]

    if words[0] == "falls":
        sleepStart = minute

    if words[0] == "wakes":
        for i in range(sleepStart, minute):
            minuteTalliesPerGuard[currentGuard][i] += 1

minuteTotals = [[guard, sum(tallies)] for guard, tallies in minuteTalliesPerGuard.items()]
sleepiestGuard = sorted(minuteTotals, key=lambda totals: totals[1])[-1][0]
sleepiestGuardTalliesWithMinute = [[i, tally] for i, tally in enumerate(minuteTalliesPerGuard[sleepiestGuard])]
sleepiestMinute = sorted(sleepiestGuardTalliesWithMinute, key=lambda tally: tally[1])[-1][0]

print("Guard ID times sleepiest minute:", sleepiestGuard * sleepiestMinute)

minuteMaximums = []
for guard, tallies in minuteTalliesPerGuard.items():
    tallies = [[minute, tally] for minute, tally in enumerate(tallies)]
    minuteMaximums.append([guard, sorted(tallies, key=lambda tally: tally[1])[-1]])
mostRegularGuards = sorted(minuteMaximums, key=lambda max: max[1][1])
mostRegularGuard = mostRegularGuards[-1]

print("Guard ID times most regular minute:", mostRegularGuard[0] * mostRegularGuard[1][0])
