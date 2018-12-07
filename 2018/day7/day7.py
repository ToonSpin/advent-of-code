import fileinput

numWorkers = 5
baseTime = 61

input = []

for line in fileinput.input():
    input.append((line[5], line[36]))

allSteps = set()

for x in input:
    allSteps.add(x[0])
    allSteps.add(x[1])

allDependencies = {token: set() for token in allSteps}
for x in input:
    allDependencies[x[1]].add(x[0])

stepsDone = []
stepsLeft = allSteps

currentWork = [" " for i in range(numWorkers)]
nextFreeTimestamp = [0 for i in range(numWorkers)]
currentTimestamp = 0

while len(stepsLeft):
    for worker in [worker for worker, timestamp in enumerate(nextFreeTimestamp) if timestamp == currentTimestamp]:
        if currentWork[worker] != " ":
            stepsLeft.remove(currentWork[worker])
            currentWork[worker] = " "

    dependencies = {step: deps for step, deps in allDependencies.items() if step in stepsLeft}
    for step in dependencies:
        dependencies[step] = dependencies[step].intersection(stepsLeft)

    candidates = sorted([step for step, deps in dependencies.items() if len(deps) == 0 and step not in currentWork])
    availableWorkers = sorted([worker for worker, timestamp in enumerate(nextFreeTimestamp) if timestamp <= currentTimestamp])

    while len(availableWorkers) and len(candidates):
        candidate = candidates[0]
        worker = availableWorkers[0]

        candidates = candidates[1:]
        availableWorkers = availableWorkers[1:]

        currentWork[worker] = candidate
        nextFreeTimestamp[worker] = currentTimestamp + ord(candidate) - 65 + baseTime

        stepsDone.append(candidate)

    currentTimestamp += 1

print("Steps in order:", "".join(stepsDone))
print("Time taken:", currentTimestamp - 1)
