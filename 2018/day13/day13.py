import fileinput, re

input = [line.rstrip() for line in fileinput.input()]
regex = re.compile(r'[<>^v]')

left = 0
straight = 1
right = 2

carts = []

newDirectionsByDirection = {
    '<': ['v', '<', '^'],
    '>': ['^', '>', 'v'],
    '^': ['<', '^', '>'],
    'v': ['>', 'v', '<'],
}

deltasByDirection = {
    '<': [ -1,  0],
    '>': [  1,  0],
    '^': [  0, -1],
    'v': [  0,  1],
}

newDirectionsByCorner = {
    '/': {
        '<': 'v',
        '>': '^',
        '^': '>',
        'v': '<',
    },
    '\\': {
        '<': '^',
        '>': 'v',
        '^': '<',
        'v': '>',
    }
}

for y in range(len(input)):
    cartMatches = re.finditer(regex, input[y])
    for match in cartMatches:
        direction = match[0]
        x = match.start()
        carts.append([direction, int(x), int(y), left])
        if direction == '<' or direction == '>':
            input[y] = input[y][:x] + '-' + input[y][x+1:]
        if direction == '^' or direction == 'v':
            input[y] = input[y][:x] + '|' + input[y][x+1:]


firstCollisionFound = False
while len(carts) > 1:
    carts.sort(key=lambda cart: cart[2] * len(input[0]) + cart[1])

    currentCart = 0
    while currentCart < len(carts):
        direction, x, y, turnType = carts[currentCart]
        track = input[y][x]

        if track == '+':
            direction = newDirectionsByDirection[direction][turnType]
            turnType = (turnType + 1) % 3

        if track == '/' or track == '\\':
            direction = newDirectionsByCorner[track][direction]

        x += deltasByDirection[direction][0]
        y += deltasByDirection[direction][1]

        carts[currentCart] = [direction, x, y, turnType]

        collisionFound = False

        for i in range(len(carts)):
            if i == currentCart:
                continue
            if (carts[i][1], carts[i][2]) == (x, y):
                collisionFound = True

                if not firstCollisionFound:
                    print("The first collision happens at %d,%d." % (x, y))
                    firstCollisionFound = True

                if i < currentCart:
                    currentCart -= 1

                a, b = (min(currentCart, i), max(currentCart, i))
                carts = carts[:b] + carts[b+1:]
                carts = carts[:a] + carts[a+1:]

                break

        if not collisionFound:
            currentCart += 1

print("The last remaining cart ends up at %d,%d." % (carts[0][1], carts[0][2]))
