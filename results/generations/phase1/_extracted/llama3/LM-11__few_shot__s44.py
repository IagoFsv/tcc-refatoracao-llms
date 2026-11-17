"""Drawing of the gallows in a hangman game, according to the number of misses.

Public entry point: run(misses). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""


def _print_head():
    print('_________')
    print('|       |')


def _print_body(guessCount):
    if guessCount == 1:
        print('|       O')
    elif guessCount == 2:
        print('|       O')
    elif guessCount == 3:
        print('|       O')
        print('|      /|')
    elif guessCount == 4:
        print('|       O')
        print('|      /|\\')
    elif guessCount == 5:
        print('|       O')
        print('|      /|\\')
        print('|      /')
    elif guessCount == 6:
        print('|       O')
        print('|      /|\\')
        print('|      / \\')


def _print_legs(guessCount):
    if guessCount >= 3:
        print('|      /')
        print('|      / \\')


def run(misses):
    """Prints the gallows for the number of misses. Public entry point of this unit."""
    _print_head()
    _print_body(misses)
    _print_legs(misses)
