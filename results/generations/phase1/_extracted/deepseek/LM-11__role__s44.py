"""Drawing of the gallows in a hangman game, according to the number of misses.

Public entry point: run(misses). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""


def print_hangman(guessCount):
    if guessCount == 0:
        print_gallows(0)
    elif guessCount == 1:
        print_gallows(1)
    elif guessCount == 2:
        print_gallows(2)
    elif guessCount == 3:
        print_gallows(3)
    elif guessCount == 4:
        print_gallows(4)
    elif guessCount == 5:
        print_gallows(5)
    elif guessCount == 6:
        print_gallows(6)


def print_gallows(guessCount):
    print('_________')
    print('|       |  ')
    if guessCount >= 1:
        print('|       O  ')
    if guessCount >= 2:
        print('|       |')
    if guessCount >= 3:
        print('|      /|')
    if guessCount >= 4:
        print('|      /|\\')
    if guessCount >= 5:
        print('|      /')
    if guessCount == 6:
        print('|')
    print('|')
    print('|')


def run(misses):
    """Prints the gallows for the number of misses. Public entry point of this unit."""
    return print_hangman(misses)
