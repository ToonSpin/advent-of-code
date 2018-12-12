import fileinput

margin = 250
numGenerations = 20

input = [line.rstrip() for line in fileinput.input()]
initialState = list(margin * '.' + input[0][15:] + margin * '.')

rules = {}

for ruleInput in input[2:]:
    rule, offspring = ruleInput.split(' => ')
    rules[rule] = offspring

def processRules(state):
    newState = list('.' * (len(state)))
    for i in range(len(state) - 4):
        rule = "".join(state[i:i+5])
        newState[i + 2] = rules[rule]
    return newState

def getScore(state):
    return sum([position - margin for position, plant in enumerate(state) if plant == '#'])

def getSignature(state):
    begin = 0
    end = len(state)
    while state[begin] == '.':
        begin += 1
    while state[end - 1] == '.':
        end -= 1
    return "".join(state[begin:end])

state = initialState
generation = 0
while generation < numGenerations:
    state = processRules(state)
    generation += 1

print("Total after %d generations: %d" % (numGenerations, getScore(state)))

oldSignature = getSignature(state)
while True:
    generation += 1
    state = processRules(state)
    signature = getSignature(state)
    if signature == oldSignature:
        break
    oldSignature = signature

score = getScore(state)
nextScore = getScore(processRules(state))

score = (nextScore - score) * (5000000000 - generation) + score

print("Total after 50 billion generations:", score)
