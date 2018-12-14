import fileinput

for line in fileinput.input():
    strInput = line.rstrip()
    input = int(strInput)

elf1 = 0
elf2 = 1
recipes = "37"
count = 2
countBeforeMatch = 0

while count < input + 10 or countBeforeMatch <= 0:
    if countBeforeMatch <= 0:
        if recipes[-len(strInput)-1:-1] == strInput:
            countBeforeMatch = count - len(strInput) - 1
        elif recipes[-len(strInput):] == strInput:
            countBeforeMatch = count - len(strInput)

    recipes = recipes + str(int(recipes[elf1]) + int(recipes[elf2]))
    count = len(recipes)

    elf1 = (elf1 + int(recipes[elf1]) + 1) % count
    elf2 = (elf2 + int(recipes[elf2]) + 1) % count

scoresAfterInputRecipes = "".join([str(i) for i in recipes[input:input+10]])
print("Scores after %d recipes: %s" % (input, scoresAfterInputRecipes))
print("Number of recipes before %s: %d" % (strInput, countBeforeMatch))
