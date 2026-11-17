"""Drawing of the gallows in a hangman game, according to the number of misses.

Public entry point: run(misses). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""


def print_head(guessCount):
    print('_________')
    print('|       |')
    print('|')
    print('|')
    print('|')
    print('|')
    print('|')
    print('|')


def print_body(guessCount):
    if guessCount > 0:
        print('|       O')
    if guessCount > 1:
        print('|       |')
    if guessCount > 2:
        if guessCount == 3:
            print('|      /|')
        elif guessCount == 4:
            print('|      /|\\')
        elif guessCount > 4:
            print('|      /|\\')
            print('|      /')


def print_foot(guessCount):
    if guessCount > 5:
        print('|      / \\')
    print('|')


def print_hangman(guessCount):
    print_head(guessCount)
    print_body(guessCount)
    print_foot(guessCount)


def run(misses):
    """Prints the gallows for the number of misses. Public entry point of this unit."""
    return print_hangman(misses)
