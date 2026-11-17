"""Drawing of the gallows in a hangman game, according to the number of misses.

Public entry point: run(misses). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""


def print_hangman(guessCount):
    if guessCount == 0:
        print('_________')
        print('|       |  ')
        print('|        ')
        print('|        ')
        print('|        ')
        print('|        ')
        print('|        ')
        print('|        ')
    elif guessCount == 1:
        print('_________')
        print('|       |  ')
        print('|       O')
        print('|        ')
        print('|        ')
        print('|        ')
        print('|        ')
        print('|        ')
    else:
        draw_man(guessCount)


def draw_man(guessCount):
    print('_________')
    print('|       |  ')
    print('|       O')
    print('|      ', end='')
    print('/' if guessCount >= 3 else ' ', end='')
    print('|', end='')
    print('\\' if guessCount >= 4 else ' ', end='')
    print('/', end='')
    print('|', end='')
    print('\\' if guessCount >= 5 else ' ', end='')
    print('/', end='')
    print('\\' if guessCount >= 6 else ' ', end='')
    print('  ')


def run(misses):
    """Prints the gallows for the number of misses. Public entry point of this unit."""
    return print_hangman(misses)
