"""Drawing of the gallows in a hangman game, according to the number of misses.

Public entry point: run(misses). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""


def print_gallows_base():
    print('_________')
    print('|       |')


def print_gallows_head(guessCount):
    if guessCount >= 1:
        print('|       O')
    else:
        print('|')


def print_gallows_body(guessCount):
    if guessCount >= 2:
        print('|       |  ')
    else:
        print('|')


def print_gallows_arms(guessCount):
    if guessCount >= 3:
        print('|       /|')
    else:
        print('|')


def print_gallows_legs(guessCount):
    if guessCount >= 4:
        print('|       /|\\')
    else:
        print('|')


def print_gallows_tail(guessCount):
    if guessCount >= 5:
        print('|       /')
    else:
        print('|')

    if guessCount >= 6:
        print('|       \\')
    else:
        print('|')


def print_hangman(guessCount):
    print_gallows_base()
    print_gallows_head(guessCount)
    print_gallows_body(guessCount)
    print_gallows_arms(guessCount)
    print_gallows_legs(guessCount)
    print_gallows_tail(guessCount)


def run(misses):
    """Prints the gallows for the number of misses. Public entry point of this unit."""
    return print_hangman(misses)
