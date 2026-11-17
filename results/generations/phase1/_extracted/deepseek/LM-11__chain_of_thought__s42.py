"""Drawing of the gallows in a hangman game, according to the number of misses.

Public entry point: run(misses). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""


def print_gallows_part(guessCount):
    if guessCount == 0:
        print('_________')
        print('|       |')
        print('|')
        print('|')
        print('|')
        print('|')
        print('|')
        print('|')
    elif guessCount == 1:
        print('       O')
    elif guessCount == 2:
        print('       O')
        print('       |')
    elif guessCount == 3:
        print('       O')
        print('      /|')
    elif guessCount == 4:
        print('       O')
        print('      /|\\')
    elif guessCount == 5:
        print('       O')
        print('      /|\\')
        print('       /')
    elif guessCount == 6:
        print('       O')
        print('      /|\\')
        print('       / \\')


def print_hangman(guessCount):
    print('_________')
    print('|       |  ')
    print_gallows_part(guessCount)


def run(misses):
    """Prints the gallows for the number of misses. Public entry point of this unit."""
    return print_hangman(misses)
