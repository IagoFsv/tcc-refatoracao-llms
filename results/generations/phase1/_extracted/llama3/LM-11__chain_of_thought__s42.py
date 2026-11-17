"""Drawing of the gallows in a hangman game, according to the number of misses.

Public entry point: run(misses). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""


def draw_gallows_head():
    print('_________')
    print('|       |')
    print('|       O')
    print('|')
    print('|')
    print('|')
    print('|')
    print('|')


def draw_gallows_body():
    print('_________')
    print('|       |')
    print('|       O')
    print('|       |')
    print('|')
    print('|')
    print('|')
    print('|')


def draw_gallows_arms():
    print('_________')
    print('|       |')
    print('|       O')
    print('|      /|')
    print('|')
    print('|')
    print('|')
    print('|')


def draw_gallows_legs():
    print('_________')
    print('|       |')
    print('|       O')
    print('|      /|\\')
    print('|')
    print('|')
    print('|')
    print('|')


def draw_gallows_hanged():
    print('_________')
    print('|       |')
    print('|       O')
    print('|      /|\\')
    print('|      / \\')
    print('|')
    print('|')
    print('|')


def print_hangman(guessCount):
    if guessCount == 0:
        print('No gallows to draw')
    elif guessCount == 1:
        draw_gallows_head()
    elif guessCount == 2:
        draw_gallows_head()
    elif guessCount == 3:
        draw_gallows_head()
        draw_gallows_body()
    elif guessCount == 4:
        draw_gallows_head()
        draw_gallows_body()
        draw_gallows_arms()
    elif guessCount == 5:
        draw_gallows_head()
        draw_gallows_body()
        draw_gallows_arms()
        draw_gallows_legs()
    elif guessCount == 6:
        draw_gallows_head()
        draw_gallows_body()
        draw_gallows_arms()
        draw_gallows_legs()
        draw_gallows_hanged()


def run(misses):
    """Prints the gallows for the number of misses. Public entry point of this unit."""
    return print_hangman(misses)
