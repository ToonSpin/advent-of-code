#include <stdio.h>

#define abs(x) ((x) < 0? -(x): (x))
#define POLYMER_LENGTH 50000

struct polymer
{
    int unit;
    struct polymer *prev;
    struct polymer *next;
};

int getPolymerLength(struct polymer *polymer)
{
    int length = 0;
    while (polymer) {
        polymer = polymer->next;
        length++;
    }
    return length;
}

void resetPolymer(struct polymer *polymerPtr)
{
    int i;
    struct polymer *prevUnit = NULL;

    for (i = 0; i < POLYMER_LENGTH - 1; i++) {
        polymerPtr->prev = prevUnit;
        prevUnit = polymerPtr++;
        prevUnit->next = polymerPtr;
    }
    polymerPtr->next = NULL;
}

void fillPolymerFromStdin(struct polymer *polymerPtr)
{
    int c, i;
    struct polymer *prevUnit = NULL;

    while (i < POLYMER_LENGTH && (c = fgetc(stdin)) != EOF) {
        polymerPtr->unit = c;
        polymerPtr->next = NULL;
        if (i++) {
            polymerPtr->prev = prevUnit;
            prevUnit->next = polymerPtr;
        }

        prevUnit = polymerPtr++;
    }
}

struct polymer *react(struct polymer *inputPolymer)
{
    struct polymer *currentUnit = inputPolymer;

    while (currentUnit->next) {
        while (abs(currentUnit->unit - currentUnit->next->unit) == 32) {
            if (currentUnit->prev) {
                currentUnit->prev->next = currentUnit->next->next;
                if (currentUnit->next->next) {
                    currentUnit->next->next->prev = currentUnit->prev;
                }
                currentUnit = currentUnit->prev;
            } else {
                currentUnit = currentUnit->next->next;
                currentUnit->prev = NULL;
                inputPolymer = currentUnit;
            }
        }
        currentUnit = currentUnit->next;
    }
    return inputPolymer;
}

struct polymer *stripCharacter(struct polymer *inputPolymer, char c)
{
    struct polymer *currentUnit = inputPolymer;

    c = c < 'a'? c: c - 32;

    while (currentUnit) {
        while (currentUnit->unit == c || currentUnit->unit == c + 32) {
            if (currentUnit->prev) {
                currentUnit->prev->next = currentUnit->next;
                if (currentUnit->next) {
                    currentUnit->next->prev = currentUnit->prev;
                }
                currentUnit = currentUnit->prev;
            } else {
                currentUnit = currentUnit->next;
                currentUnit->prev = NULL;
                inputPolymer = currentUnit;
            }
        }
        currentUnit = currentUnit->next;
    }
    return inputPolymer;
}

int main(void)
{
    struct polymer inputPolymer[POLYMER_LENGTH], *newPolymer;
    char *alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ", letter;

    fillPolymerFromStdin(inputPolymer);

    printf("Length before reaction: %d\n", getPolymerLength(inputPolymer));
    newPolymer = react(inputPolymer);
    printf("Length after reaction: %d\n", getPolymerLength(newPolymer));

    while (letter = *alphabet++) {
        resetPolymer(inputPolymer);
        newPolymer = stripCharacter(inputPolymer, letter);
        printf("Length after reaction after stripping %c: %d\n", letter, getPolymerLength(react(newPolymer)));
    }

    return 0;
}
