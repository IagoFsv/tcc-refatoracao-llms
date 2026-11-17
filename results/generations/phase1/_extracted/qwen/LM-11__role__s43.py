"""Drawing of the gallows in a hangman game, according to the number of misses.

Public entry point: run(misses). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

def print_hangman_part(miss, part):
    print('_________')
    print('|       |')
    if miss >= 1: print('|       O')
    if miss >= 2: print('|      /|' if miss == 2 else '|      /|\\')
    if miss >= 3: print('|      / \\' if miss == 3 else '|      / \\')
    print('|')

def print_hangman(guessCount):
    if guessCount == 0:
        print_hangman_part(0, 0)
    elif guessCount == 1:
        print_hangman_part(1, 0)
    elif guessCount == 2:
        print_hangman_part(2, 0)
    elif guessCount == 3:
        print_hangman_part(3, 0)
    elif guessCount == 4:
        print_hangman_part(4, 0)
    elif guessCount == 5:
        print_hangman_part(5, 0)
    elif guessCount == 6:
        print_hangman_part(6, 0)

def run(misses):
    """Prints the gallows for the number of misses. Public entry point of this unit."""
    return print_hangman(misses)
