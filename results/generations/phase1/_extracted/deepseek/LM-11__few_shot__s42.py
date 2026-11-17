"""Drawing of the gallows in a hangman game, according to the number of misses.

Public entry point: run(misses). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""


def print_gallows(guessCount):
    if guessCount == 0:
        print('_________')
        print('|       |  ')
        print('|       ')
        print('|')
        print('|')
        print('|')
        print('|')
        print('|')
    elif guessCount == 1:
        print('_________')
        print('|       |  ')
        print('|       O')
        print('|')
        print('|')
        print('|')
        print('|')
        print('|')
    elif guessCount == 2:
        print('_________')
        print('|       |  ')
        print('|       O')
        print('|       |  ')
        print('|')
        print('|')
        print('|')
        print('|')
    elif guessCount == 3:
        print('_________')
        print('|       |  ')
        print('|       O')
        print('|       /|')
        print('|')
        print('|')
        print('|')
        print('|')
    elif guessCount == 4:
        print('_________')
        print('|       |  ')
        print('|       O')
        print('|       /|\\')
        print('|')
        print('|')
        print('|')
        print('|')
    elif guessCount == 5:
        print('_________')
        print('|       |  ')
        print('|       O')
        print('|       /|\\')
        print('|       / ')
        print('|')
        print('|')
        print('|')
    elif guessCount == 6:
        print('_________')
        print('|       |  ')
        print('|       O')
        print('|       /|\\')
        print('|       / \\')
        print('|')
        print('|')
        print('|')


def run(misses):
    """Prints the gallows for the number of misses. Public entry point of this unit."""
    return print_gallows(misses)
