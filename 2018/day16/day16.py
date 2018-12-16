import fileinput, re, curses

input = [line.rstrip() for line in fileinput.input()]

samples = []
i = 0
while i  < len(input):
    if input[i][:9] != 'Before: [':
        i += 1
        continue

    sampleInput = input[i][9:-1].split(', ')
    sampleInstruction = input[i + 1].split(' ')
    sampleOutput = input[i + 2][9:-1].split(', ')

    sampleInput = tuple(map(int, sampleInput))
    sampleInstruction = tuple(map(int, sampleInstruction))
    sampleOutput = tuple(map(int, sampleOutput))

    samples.append((sampleInput, sampleInstruction, sampleOutput))

    i += 3

def addr(reg, instr):
    outp = list(reg)
    outp[instr[2]] = reg[instr[0]] + reg[instr[1]]
    return tuple(outp)

def mulr(reg, instr):
    outp = list(reg)
    outp[instr[2]] = reg[instr[0]] * reg[instr[1]]
    return tuple(outp)

def banr(reg, instr):
    outp = list(reg)
    outp[instr[2]] = reg[instr[0]] & reg[instr[1]]
    return tuple(outp)

def ornr(reg, instr):
    outp = list(reg)
    outp[instr[2]] = reg[instr[0]] | reg[instr[1]]
    return tuple(outp)

def setr(reg, instr):
    outp = list(reg)
    outp[instr[2]] = reg[instr[0]]
    return tuple(outp)

def addi(reg, instr):
    outp = list(reg)
    outp[instr[2]] = reg[instr[0]] + instr[1]
    return tuple(outp)

def muli(reg, instr):
    outp = list(reg)
    outp[instr[2]] = reg[instr[0]] * instr[1]
    return tuple(outp)

def bani(reg, instr):
    outp = list(reg)
    outp[instr[2]] = reg[instr[0]] & instr[1]
    return tuple(outp)

def orni(reg, instr):
    outp = list(reg)
    outp[instr[2]] = reg[instr[0]] | instr[1]
    return tuple(outp)

def seti(reg, instr):
    outp = list(reg)
    outp[instr[2]] = instr[0]
    return tuple(outp)

def gtir(reg, instr):
    outp = list(reg)
    outp[instr[2]] = 1 if instr[0] > reg[instr[1]] else 0
    return tuple(outp)

def gtri(reg, instr):
    outp = list(reg)
    outp[instr[2]] = 1 if reg[instr[0]] > instr[1] else 0
    return tuple(outp)

def gtrr(reg, instr):
    outp = list(reg)
    outp[instr[2]] = 1 if reg[instr[0]] > reg[instr[1]] else 0
    return tuple(outp)

def eqir(reg, instr):
    outp = list(reg)
    outp[instr[2]] = 1 if instr[0] == reg[instr[1]] else 0
    return tuple(outp)

def eqri(reg, instr):
    outp = list(reg)
    outp[instr[2]] = 1 if reg[instr[0]] == instr[1] else 0
    return tuple(outp)

def eqrr(reg, instr):
    outp = list(reg)
    outp[instr[2]] = 1 if reg[instr[0]] == reg[instr[1]] else 0
    return tuple(outp)

instructionSet = {
    'addr': { 'executor': addr, 'possible-identifiers': set(range(16)) },
    'mulr': { 'executor': mulr, 'possible-identifiers': set(range(16)) },
    'banr': { 'executor': banr, 'possible-identifiers': set(range(16)) },
    'ornr': { 'executor': ornr, 'possible-identifiers': set(range(16)) },
    'setr': { 'executor': setr, 'possible-identifiers': set(range(16)) },
    'addi': { 'executor': addi, 'possible-identifiers': set(range(16)) },
    'muli': { 'executor': muli, 'possible-identifiers': set(range(16)) },
    'bani': { 'executor': bani, 'possible-identifiers': set(range(16)) },
    'orni': { 'executor': orni, 'possible-identifiers': set(range(16)) },
    'seti': { 'executor': seti, 'possible-identifiers': set(range(16)) },
    'gtir': { 'executor': gtir, 'possible-identifiers': set(range(16)) },
    'gtri': { 'executor': gtri, 'possible-identifiers': set(range(16)) },
    'gtrr': { 'executor': gtrr, 'possible-identifiers': set(range(16)) },
    'eqir': { 'executor': eqir, 'possible-identifiers': set(range(16)) },
    'eqri': { 'executor': eqri, 'possible-identifiers': set(range(16)) },
    'eqrr': { 'executor': eqrr, 'possible-identifiers': set(range(16)) },
}

numberOfAmbiguousSamples = 0
for sample in samples:
    possibleOpcodes = []
    registers, instruction, output = sample
    identifier, a, b, c = instruction

    for opcode in instructionSet:
        match = False
        try:
            if instructionSet[opcode]['executor'](registers, (a, b, c)) == output:
                possibleOpcodes.append(opcode)
                match = True
        except IndexError:
            pass

        if not match and identifier in instructionSet[opcode]['possible-identifiers']:
            instructionSet[opcode]['possible-identifiers'].remove(identifier)

    if len(possibleOpcodes) >= 3:
        numberOfAmbiguousSamples += 1

print("Number of samples with three or more possible opcodes:", numberOfAmbiguousSamples)

identifiersByOpcode = {}
done = False
while not done:
    done = True
    for opcode in instructionSet:
        if opcode in identifiersByOpcode:
            continue

        done = False
        candidates = instructionSet[opcode]['possible-identifiers']

        for knownOpcode, knownIdentifier in identifiersByOpcode.items():
            if knownIdentifier in candidates:
                candidates.remove(knownIdentifier)

        instructionSet[opcode]['possible-identifiers'] = candidates
        if len(candidates) == 1:
            identifiersByOpcode[opcode] = list(candidates)[0]

opcodesByIdentifier = list(identifiersByOpcode.keys())
opcodesByIdentifier.sort(key = lambda opcode: identifiersByOpcode[opcode])

program = input[4 * len(samples) + 2:]
program = [instruction.split(' ') for instruction in program]
program = [tuple(map(int, instruction)) for instruction in program]

registers = (0, 0, 0, 0)

for instruction in program:
    identifier, a, b, c = instruction
    opcode = opcodesByIdentifier[identifier]
    registers = instructionSet[opcode]['executor'](registers, (a, b, c))

print("Contents of register 0 after execution:", registers[0])
